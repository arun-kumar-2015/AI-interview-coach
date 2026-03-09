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

print("DEBUG: main.py started")
import sys
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
from routes.upload import router as upload_router
from routes.questions import router as questions_router
from routes.evaluate import router as evaluate_router
from routes.hr_questions import router as hr_questions_router
from routes.improve import router as improve_router
from routes.video_interview import router as video_interview_router

# Services are accessed lazily via app_state
pass


# Import state and services
from app_state import get_embedding_service, get_vector_store, get_llm_service, resumes_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager.
    Starts immediately to avoid Render timeouts.
    Warm up services in the background.
    """
    import threading
    
    def warm_up():
        print("🔥 Warming up services in background...")
        try:
            get_embedding_service()
            get_llm_service()
            print("✨ Services warmed up successfully!")
        except Exception as e:
            print(f"⚠️ Warm-up warning: {e}")

    # Start warm-up in a separate thread so it doesn't block Port Scan
    threading.Thread(target=warm_up, daemon=True).start()
    
    print("🚀 Smart AI Interview Coach Backend is READY!")
    yield
    print("🛑 Shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Smart AI Interview & Resume Coach API",
    description="""
    ## 🎯 Overview
    
    This API provides a comprehensive interview preparation and resume improvement 
    system using Generative AI and RAG (Retrieval-Augmented Generation).
    
    ### 🔑 Key Features
    
    1. **Resume Processing**: Upload PDF resumes, extract text, and create embeddings
    2. **Vector Storage**: Store resume embeddings in FAISS for semantic retrieval
    3. **Technical Questions**: Generate personalized technical questions from resume
    4. **Answer Evaluation**: Evaluate answers with scoring and feedback
    5. **HR Questions**: Generate behavioral/HR questions
    6. **Resume Improvement**: Get ATS and content improvement suggestions
    
    ### 🏗️ Architecture
    
    - **RAG Pattern**: Combines LLM capabilities with semantic search over resume content
    - **Prompt Engineering**: Structured prompts with system/user role separation
    - **Vector Embeddings**: Sentence-transformers for semantic similarity
    
    ### 📝 Note
    
    All endpoints return JSON responses. Check individual endpoint documentation 
    for request/response schemas.
    """,
    version="1.0.0",
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

# Optional: Add a catch-all origin handler if needed, or stick to the above for security
# For now, let's keep it specific so allow_credentials works.


# ==================== Health Check ====================

@app.get("/", tags=["Health Check"])
async def root():
    """
    Root endpoint - Health check
    """
    return {
        "status": "✅ API is running!",
        "message": "Welcome to Smart AI Interview & Resume Coach API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "message": "API is responding"
    }


# ==================== Include Routers ====================

app.include_router(upload_router, prefix="/api", tags=["Resume Upload"])
app.include_router(questions_router, prefix="/api", tags=["Technical Questions"])
app.include_router(evaluate_router, prefix="/api", tags=["Answer Evaluation"])
app.include_router(hr_questions_router, prefix="/api", tags=["HR Questions"])
app.include_router(improve_router, prefix="/api", tags=["Resume Improvement"])
app.include_router(video_interview_router, prefix="/api", tags=["Video Interview"])


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
