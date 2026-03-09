"""
Resume Upload Routes
====================

This module handles the resume upload endpoint, including:
- PDF file validation and extraction
- Text preprocessing
- Embedding generation and vector storage

Author: AI Interview Coach Team
"""

import uuid
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from pydantic import BaseModel

# Services are loaded lazily within the routes
pass

# Import main app globals from same package level
pass


router = APIRouter()


# ==================== Request/Response Models ====================

class UploadResponse(BaseModel):
    """Response model for resume upload"""
    session_id: str
    message: str
    text_length: int
    sections_found: int
    preview: str


class SessionResponse(BaseModel):
    """Response for session info"""
    session_id: str
    status: str
    text_length: int


# ==================== Routes ====================

@router.post("/upload_resume", response_model=UploadResponse)
async def upload_resume(
    file: UploadFile = File(..., description="PDF resume file"),
    job_role: Optional[str] = "Software Engineer"
):
    """
    Upload and process a resume PDF.
    
    This endpoint:
    1. Validates the uploaded file is a PDF
    2. Extracts text from the PDF
    3. Cleans and preprocesses the text
    4. Splits into logical sections
    5. Generates embeddings for semantic search
    6. Stores embeddings in FAISS vector database
    
    Returns:
        UploadResponse: Session ID and processing details
        
    Raises:
        HTTPException: If file processing fails
    """
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are accepted. Please upload a PDF resume."
        )
    
    # Generate unique session ID
    session_id = str(uuid.uuid4())
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Check file size (max 10MB)
        if len(file_content) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File too large. Maximum size is 10MB."
            )
        
        # Extract text from PDF
        print(f"📄 Extracting text from PDF: {file.filename}")
        from services.pdf_service import PDFService
        raw_text = PDFService.extract_text_from_pdf(file_content)
        
        if not raw_text or len(raw_text.strip()) < 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not extract sufficient text from PDF. Please ensure the PDF contains readable text."
            )
        
        # Clean and preprocess text
        print(f"🧹 Cleaning and preprocessing text...")
        cleaned_text = PDFService.clean_text(raw_text)
        
        # Split into sections
        sections = PDFService.split_into_sections(cleaned_text)
        
        # Get global services from main app
        # Note: In production, use proper dependency injection
        # Get global services from app_state
        from app_state import get_vector_store, get_embedding_service, resumes_db
        
        vector_store = get_vector_store()
        embedding_service = get_embedding_service()
        
        if not vector_store or not embedding_service:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Services not initialized. Please restart the server."
            )
        
        # Create vector index for this session
        print(f"📦 Creating vector index for session: {session_id}")
        vector_store.create_index(session_id)
        
        # Add texts to vector store
        # We'll add both individual sections and combined text
        texts_to_embed = []
        
        # Add each section separately
        for section in sections:
            if section['content'].strip():
                texts_to_embed.append(f"{section['name']}: {section['content']}")
        
        # Also add the full cleaned text
        texts_to_embed.append(cleaned_text)
        
        # Add to vector store
        vector_store.add_texts(session_id, texts_to_embed)
        
        # Store resume data in memory
        resumes_db[session_id] = {
            'filename': file.filename,
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'sections': sections,
            'job_role': job_role,
            'uploaded_at': str(uuid.uuid4())  # Timestamp placeholder
        }
        
        # Get preview
        preview = PDFService.get_text_preview(cleaned_text, max_length=500)
        
        print(f"✅ Resume processed successfully for session: {session_id}")
        
        return UploadResponse(
            session_id=session_id,
            message="Resume uploaded and processed successfully!",
            text_length=len(cleaned_text),
            sections_found=len(sections),
            preview=preview
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error processing resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process resume: {str(e)}"
        )


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session_info(session_id: str):
    """
    Get information about an uploaded resume session.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        SessionResponse: Session details
    """
    from app_state import resumes_db
    
    if session_id not in resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found. Please upload a resume first."
        )
    
    session_data = resumes_db[session_id]
    
    return SessionResponse(
        session_id=session_id,
        status="active",
        text_length=len(session_data['cleaned_text'])
    )


@router.delete("/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete a resume session and its associated data.
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        Success message
    """
    from app_state import resumes_db, get_vector_store
    vector_store = get_vector_store()
    
    if session_id not in resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    
    # Delete from database
    del resumes_db[session_id]
    
    # Delete vector index
    if vector_store:
        vector_store.delete_index(session_id)
    
    return {"message": f"Session {session_id} deleted successfully."}
