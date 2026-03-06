"""
Technical Interview Questions Routes
=====================================

This module handles the generation of personalized technical interview
questions based on resume content using RAG and LLM.

RAG (Retrieval-Augmented Generation) Concept:
1. Retrieve relevant resume sections using vector similarity search
2. Augment the prompt with retrieved context
3. Generate questions using the LLM

Author: AI Interview Coach Team
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Import prompts
from prompts.question_generator import (
    TECHNICAL_QUESTION_SYSTEM_PROMPT,
    create_technical_question_user_prompt,
    create_resume_analysis_user_prompt,
    RESUME_ANALYSIS_SYSTEM_PROMPT
)

# Import services
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


router = APIRouter()


# ==================== Request/Response Models ====================

class QuestionGenerationRequest(BaseModel):
    """Request model for generating technical questions"""
    session_id: str
    job_role: str = "Software Engineer"
    num_questions: int = 10
    focus_areas: Optional[List[str]] = None


class Question(BaseModel):
    """Individual interview question model"""
    question: str
    category: str
    difficulty: str
    focus: str
    context: str


class QuestionsResponse(BaseModel):
    """Response model for generated questions"""
    session_id: str
    job_role: str
    questions: List[Question]
    total_questions: int


class ResumeAnalysisResponse(BaseModel):
    """Response model for resume analysis"""
    session_id: str
    skills: List[str]
    experience_areas: List[str]
    projects: List[dict]
    technologies: List[str]
    domain_knowledge: List[str]
    leadership_indicators: List[str]


# ==================== Routes ====================

@router.post("/generate_questions", response_model=QuestionsResponse)
async def generate_technical_questions(request: QuestionGenerationRequest):
    """
    Generate personalized technical interview questions based on resume.
    
    This endpoint uses RAG (Retrieval-Augmented Generation):
    1. Retrieves relevant sections from resume using vector similarity
    2. Creates a prompt with the retrieved context
    3. Generates questions using LLM with medium temperature (0.5-0.7)
    
    Args:
        request: QuestionGenerationRequest with session_id and preferences
        
    Returns:
        QuestionsResponse with list of personalized questions
        
    Raises:
        HTTPException: If session not found or generation fails
    """
    from app_state import resumes_db, get_vector_store, get_llm_service
    
    vector_store = get_vector_store()
    llm_service = get_llm_service()
    
    # Validate session
    if request.session_id not in resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found. Please upload a resume first."
        )
    
    if not llm_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service not available."
        )
    
    try:
        # Get resume text
        resume_data = resumes_db[request.session_id]
        resume_text = resume_data['cleaned_text']
        
        print(f"🔍 Generating {request.num_questions} technical questions...")
        
        # Create prompt with resume content
        user_prompt = create_technical_question_user_prompt(
            resume_text=resume_text,
            job_role=request.job_role,
            num_questions=request.num_questions
        )
        
        # Generate questions using LLM
        # Using medium temperature (0.5-0.7) for diverse but relevant questions
        response = llm_service.generate_json(
            system_prompt=TECHNICAL_QUESTION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=4000
        )
        
        # Parse response
        questions_data = response if isinstance(response, list) else response.get('questions', [])
        
        # Convert to Question objects
        questions = [Question(**q) for q in questions_data[:request.num_questions]]
        
        print(f"✅ Generated {len(questions)} technical questions")
        
        return QuestionsResponse(
            session_id=request.session_id,
            job_role=request.job_role,
            questions=questions,
            total_questions=len(questions)
        )
        
    except Exception as e:
        print(f"❌ Error generating questions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate questions: {str(e)}"
        )


@router.post("/analyze_resume", response_model=ResumeAnalysisResponse)
async def analyze_resume(session_id: str):
    """
    Analyze a resume and extract key information.
    
    This endpoint:
    1. Retrieves resume text from storage
    2. Uses LLM to analyze and extract key information
    3. Returns structured analysis
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        ResumeAnalysisResponse with structured resume analysis
    """
    from app_state import resumes_db, get_llm_service
    
    llm_service = get_llm_service()
    
    # Validate session
    if session_id not in resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found. Please upload a resume first."
        )
    
    if not llm_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service not available."
        )
    
    try:
        # Get resume text
        resume_data = resumes_db[session_id]
        resume_text = resume_data['cleaned_text']
        
        print(f"🔍 Analyzing resume...")
        
        # Create analysis prompt
        user_prompt = create_resume_analysis_user_prompt(resume_text)
        
        # Generate analysis
        response = llm_service.generate_json(
            system_prompt=RESUME_ANALYSIS_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=2000
        )
        
        print(f"✅ Resume analysis complete")
        
        return ResumeAnalysisResponse(
            session_id=session_id,
            skills=response.get('skills', []),
            experience_areas=response.get('experience_areas', []),
            projects=response.get('projects', []),
            technologies=response.get('technologies', []),
            domain_knowledge=response.get('domain_knowledge', []),
            leadership_indicators=response.get('leadership_indicators', [])
        )
        
    except Exception as e:
        print(f"❌ Error analyzing resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze resume: {str(e)}"
        )


@router.get("/skill_questions/{session_id}")
async def get_skill_questions(
    session_id: str,
    skill: str,
    num_questions: int = 3
):
    """
    Generate questions specific to a particular skill.
    
    Uses vector similarity search to find relevant resume sections
    about the skill, then generates targeted questions.
    
    Args:
        session_id: Unique session identifier
        skill: Specific skill to generate questions for
        num_questions: Number of questions to generate
        
    Returns:
        Questions focused on the specific skill
    """
    from main import resumes_db, get_vector_store, get_llm_service
    
    vector_store = get_vector_store()
    llm_service = get_llm_service()
    
    # Validate session
    if session_id not in resumes_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found."
        )
    
    if not vector_store or not llm_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Services not available."
        )
    
    try:
        # Get relevant context from resume using vector search
        context = vector_store.get_relevant_context(session_id, skill, max_length=1500)
        
        # Create focused prompt
        prompt = f"""Generate {num_questions} technical interview questions about {skill}.

Resume context about {skill}:
{context}

Generate questions that test deep understanding of {skill}.
Return JSON array with question, category, difficulty, focus, context fields."""
        
        response = llm_service.generate_json(
            system_prompt=TECHNICAL_QUESTION_SYSTEM_PROMPT,
            user_prompt=prompt,
            temperature=0.5,
            max_tokens=1500
        )
        
        questions = response if isinstance(response, list) else response.get('questions', [])
        
        return {
            "skill": skill,
            "questions": questions[:num_questions]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate skill questions: {str(e)}"
        )
