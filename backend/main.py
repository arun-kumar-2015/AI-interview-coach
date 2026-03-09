"""
Smart AI Interview & Resume Coach - Backend API
================================================
This application provides a complete backend for interview preparation
and resume improvement using Generative AI and RAG (Retrieval-Augmented Generation).

Key Features:
- Resume PDF upload and text extraction
- Resume embedding and FAISS vector storage for semantic retrieval
- Personalized technical interview question generation
- Answer evaluation with scoring and feedback
- HR/Behavioral question generation
- Resume improvement suggestions (ATS optimization)

Author: AI Interview Coach Team
"""

import os
import json
import uuid
import tempfile
from pathlib import Path
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import os
import sys

# Ensure the backend directory is in the Python path
# This prevents ModuleNotFoundError when running from different directories
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

print("DEBUG: main.py started")
print(f"DEBUG: Python path: {sys.path}")
print(f"DEBUG: Current directory: {os.getcwd()}")
print(f"DEBUG: Environment PORT: {os.getenv('PORT')}")

# FastAPI imports
from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Pydantic models
from pydantic import BaseModel

# Custom imports
# The original try-except block for router imports is removed as they will be imported safely within the function.
# try:
#     from routes.upload import router as upload_router
#     from routes.questions import router as questions_router
#     from routes.evaluate import router as evaluate_router
#     from routes.hr_questions import router as hr_questions_router
#     from routes.improve import router as improve_router
#     from routes.video_interview import router as video_interview_router
# except ImportError as e:
#     print(f"❌ CRITICAL IMPORT ERROR: {e}")
#     # We define dummy routers or handle it to at least allow the health check to pass
#     # but in reality, failure here is a deployment issue.
#     raise e

# Services are accessed lazily via app_state
pass


# Import state and services
from app_state import get_embedding_service, get_vector_store, get_llm_service, resumes_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Simple lifespan to ensure fast port binding.
    """
    print("🚀 AI Interview Coach Backend starting...")
    yield
    print("🛑 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Smart AI Interview Coach API",
    description="Backend API for AI-powered interview preparation",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== Health Check ====================

@app.get("/", tags=["Health Check"])
async def root():
    """Root endpoint - Health check"""
    return {
        "status": "✅ API is running!",
        "message": "Welcome to Smart AI Interview & Resume Coach API",
        "version": "1.1.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """Health check endpoint to verify the service is running."""
    import sys
    import os
    return {
        "status": "healthy", 
        "service": "AI Interview Coach API",
        "python_version": sys.version,
        "cwd": os.getcwd(),
        "port": os.getenv("PORT", "8000")
    }


# ==================== Include Routers (Safe Discovery) ====================

try:
    from routes.upload import router as upload_router
    app.include_router(upload_router, prefix="/api", tags=["Resume Upload"])
    
    from routes.questions import router as questions_router
    app.include_router(questions_router, prefix="/api", tags=["Technical Questions"])
    
    from routes.evaluate import router as evaluate_router
    app.include_router(evaluate_router, prefix="/api", tags=["Answer Evaluation"])
    
    from routes.hr_questions import router as hr_questions_router
    app.include_router(hr_questions_router, prefix="/api", tags=["HR Questions"])
    
    from routes.improve import router as improve_router
    app.include_router(improve_router, prefix="/api", tags=["Resume Improvement"])
    
    from routes.video_interview import router as video_interview_router
    app.include_router(video_interview_router, prefix="/api", tags=["Video Interview"])
    
    print("✅ All routers included successfully")
except Exception as e:
    print(f"⚠️ Warning: Some routers failed to load: {e}")
    # We still want the app to start so health check works



# ==================== Error Handlers ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """General exception handler"""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": str(exc),
            "status_code": 500
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment (Render sets PORT automatically)
    host = "0.0.0.0"
    port = int(os.getenv("PORT", "8000"))
    
    print(f"DEBUG: Internal Uvicorn starting on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=False  # Disable reload in production for stability
    )
