"""
HR & Behavioral Questions Routes
=================================

This module handles the generation of HR and behavioral interview questions
focused on leadership, teamwork, communication, and other soft skills.

Author: AI Interview Coach Team
"""

from typing import Optional, List
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Import prompts
from prompts.hr_questions import (
    HR_QUESTION_SYSTEM_PROMPT,
    create_hr_question_user_prompt,
    LEADERSHIP_QUESTION_SYSTEM_PROMPT,
    create_leadership_question_user_prompt
)

# Import services and prompts
pass


router = APIRouter()


# ==================== Request/Response Models ====================

class HRQuestionGenerationRequest(BaseModel):
    """Request model for generating HR questions"""
    session_id: str
    num_questions: int = 10
    focus_areas: Optional[str] = ""


class HRQuestion(BaseModel):
    """Individual HR question model"""
    question: str
    category: str
    experience_level: str
    what_it_tests: str
    sample_structure: str


class HRQuestionsResponse(BaseModel):
    """Response model for generated HR questions"""
    session_id: str
    questions: List[HRQuestion]
    total_questions: int


class LeadershipQuestionsResponse(BaseModel):
    """Response model for leadership questions"""
    session_id: str
    questions: List[HRQuestion]
    total_questions: int


# ==================== Routes ====================

@router.post("/generate_hr_questions", response_model=HRQuestionsResponse)
async def generate_hr_questions(request: HRQuestionGenerationRequest):
    """
    Generate HR and behavioral interview questions.
    
    This endpoint generates behavioral questions focusing on:
    - Leadership & Mentorship
    - Teamwork & Collaboration
    - Communication Skills
    - Problem Solving & Decision Making
    - Adaptability & Growth
    - Conflict Resolution
    - Time Management
    - Cultural Fit
    
    Questions are tailored to the candidate's experience level based
    on their resume content.
    
    Args:
        request: HRQuestionGenerationRequest with session and preferences
        
    Returns:
        HRQuestionsResponse with list of behavioral questions
    """
    from app_state import resumes_db, get_llm_service
    
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
        
        print(f"🎯 Generating {request.num_questions} HR/behavioral questions...")
        
        # Create prompt for HR questions
        user_prompt = create_hr_question_user_prompt(
            resume_text=resume_text,
            num_questions=request.num_questions,
            focus_areas=request.focus_areas
        )
        
        # Generate questions using LLM
        # Using medium temperature (0.5-0.7) for diverse but relevant questions
        response = llm_service.generate_json(
            system_prompt=HR_QUESTION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.6,
            max_tokens=3000
        )
        
        # Parse response
        questions_data = response if isinstance(response, list) else response.get('questions', [])
        
        # Convert to HRQuestion objects
        questions = [HRQuestion(**q) for q in questions_data[:request.num_questions]]
        
        print(f"✅ Generated {len(questions)} HR questions")
        
        return HRQuestionsResponse(
            session_id=request.session_id,
            questions=questions,
            total_questions=len(questions)
        )
        
    except Exception as e:
        print(f"❌ Error generating HR questions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate HR questions: {str(e)}"
        )


@router.post("/generate_leadership_questions", response_model=LeadershipQuestionsResponse)
async def generate_leadership_questions(
    session_id: str,
    num_questions: int = 5
):
    """
    Generate leadership-focused behavioral questions.
    
    This endpoint specifically focuses on:
    - Team leadership and management experience
    - Decision making under pressure
    - Mentoring and developing others
    - Handling conflicts
    - Strategic thinking
    - Taking initiative
    
    Args:
        session_id: Unique session identifier
        num_questions: Number of leadership questions to generate
        
    Returns:
        LeadershipQuestionsResponse with leadership-focused questions
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
        
        print(f"👔 Generating {num_questions} leadership questions...")
        
        # Create prompt for leadership questions
        user_prompt = create_leadership_question_user_prompt(
            resume_text=resume_text,
            num_questions=num_questions
        )
        
        # Generate questions
        response = llm_service.generate_json(
            system_prompt=LEADERSHIP_QUESTION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.5,
            max_tokens=2000
        )
        
        # Parse response
        questions_data = response if isinstance(response, list) else response.get('questions', [])
        
        # Convert to HRQuestion objects
        questions = [HRQuestion(**q) for q in questions_data[:num_questions]]
        
        print(f"✅ Generated {len(questions)} leadership questions")
        
        return LeadershipQuestionsResponse(
            session_id=session_id,
            questions=questions,
            total_questions=len(questions)
        )
        
    except Exception as e:
        print(f"❌ Error generating leadership questions: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate leadership questions: {str(e)}"
        )


@router.get("/behavioral_tips")
async def get_behavioral_tips():
    """
    Get tips for answering behavioral interview questions.
    
    This endpoint provides guidance on:
    - STAR method
    - Common behavioral themes
    - How to structure answers
    
    Returns:
        Tips for behavioral interviews
    """
    return {
        "star_method": {
            "description": "Use the STAR method to structure your responses",
            "situation": "Describe the context and setting",
            "task": "Explain your responsibility in that situation",
            "action": "Detail the specific actions you took",
            "result": "Share the outcomes of your actions"
        },
        "common_themes": [
            "Leadership and initiative",
            "Teamwork and collaboration",
            "Conflict resolution",
            "Problem solving",
            "Time management",
            "Adaptability and learning",
            "Communication",
            "Failure and learning"
        ],
        "tips": [
            "Be specific with examples from your experience",
            "Quantify achievements when possible",
            "Focus on your individual contributions",
            "Be honest about challenges and what you learned",
            "Practice telling stories from your past",
            "Keep answers concise but detailed enough"
        ]
    }
