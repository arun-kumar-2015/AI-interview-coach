"""
Answer Evaluation Routes
========================

This module handles the evaluation of interview answers, including:
- Scoring based on multiple criteria
- Strengths and improvements feedback
- Structured JSON responses

Prompt Engineering:
- Uses low temperature (0.0-0.2) for consistent evaluation
- Evaluates: relevance, technical accuracy, depth, communication, STAR

Author: AI Interview Coach Team
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Import prompts
from prompts.answer_evaluator import (
    ANSWER_EVALUATION_SYSTEM_PROMPT,
    create_evaluation_user_prompt,
    FOLLOWUP_SYSTEM_PROMPT,
    create_followup_user_prompt
)

# Import services
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


router = APIRouter()


# ==================== Request/Response Models ====================

class EvaluationRequest(BaseModel):
    """Request model for answer evaluation"""
    session_id: str
    question: str
    answer: str
    category: str = "Technical"
    include_resume_context: bool = False


class EvaluationBreakdown(BaseModel):
    """Score breakdown by category"""
    relevance: float
    technical_accuracy: float
    depth: float
    communication: float
    star_format: float


class EvaluationResponse(BaseModel):
    """Response model for answer evaluation"""
    session_id: str
    score: float
    breakdown: EvaluationBreakdown
    strengths: list[str]
    improvements: list[str]
    suggested_answer: str
    overall_feedback: str


class FollowUpResponse(BaseModel):
    """Response model for follow-up questions"""
    follow_up_question: str
    reason: str


# ==================== Routes ====================

@router.post("/evaluate_answer", response_model=EvaluationResponse)
async def evaluate_answer(request: EvaluationRequest):
    """
    Evaluate a candidate's answer to an interview question.
    
    This endpoint evaluates the answer based on multiple criteria:
    - Relevance (0-2): Does it answer the question?
    - Technical Accuracy (0-3): Is the technical content correct?
    - Depth (0-2): Shows deep vs surface understanding
    - Communication (0-2): Clear, structured communication
    - STAR Format (0-1): For behavioral questions
    
    Total: 10 points maximum
    
    Uses low temperature (0.0-0.2) for consistent, fair evaluation.
    
    Args:
        request: EvaluationRequest with question, answer, and optional context
        
    Returns:
        EvaluationResponse with score, breakdown, and feedback
    """
    from main import resumes_db, llm_service
    
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
        # Get resume context if requested
        resume_context = ""
        if request.include_resume_context:
            resume_data = resumes_db[request.session_id]
            resume_context = resume_data['cleaned_text'][:1000]  # Limit context
        
        print(f"📝 Evaluating answer for question: {request.question[:50]}...")
        
        # Create evaluation prompt
        user_prompt = create_evaluation_user_prompt(
            question=request.question,
            answer=request.answer,
            category=request.category,
            resume_context=resume_context
        )
        
        # Generate evaluation using LOW temperature for consistency
        response = llm_service.generate_json(
            system_prompt=ANSWER_EVALUATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.2,  # Low temperature for consistent evaluation
            max_tokens=1500
        )
        
        # Parse response
        score = float(response.get('score', 0))
        breakdown_data = response.get('breakdown', {})
        
        breakdown = EvaluationBreakdown(
            relevance=float(breakdown_data.get('relevance', 0)),
            technical_accuracy=float(breakdown_data.get('technical_accuracy', 0)),
            depth=float(breakdown_data.get('depth', 0)),
            communication=float(breakdown_data.get('communication', 0)),
            star_format=float(breakdown_data.get('star_format', 0))
        )
        
        print(f"✅ Answer evaluated: {score}/10")
        
        return EvaluationResponse(
            session_id=request.session_id,
            score=score,
            breakdown=breakdown,
            strengths=response.get('strengths', []),
            improvements=response.get('improvements', []),
            suggested_answer=response.get('suggested_answer', ''),
            overall_feedback=response.get('overall_feedback', '')
        )
        
    except Exception as e:
        print(f"❌ Error evaluating answer: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to evaluate answer: {str(e)}"
        )


@router.post("/generate_followup", response_model=FollowUpResponse)
async def generate_followup_question(request: EvaluationRequest):
    """
    Generate a follow-up question based on the candidate's answer.
    
    This helps simulate a real interview by:
    1. Digging deeper into their response
    2. Testing depth of knowledge
    3. Clarifying any vague points
    
    Args:
        request: Original question and answer
        
    Returns:
        FollowUpResponse with question and reasoning
    """
    from main import llm_service
    
    if not llm_service:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="LLM service not available."
        )
    
    try:
        print(f"🔄 Generating follow-up question...")
        
        # Create follow-up prompt
        user_prompt = create_followup_user_prompt(
            question=request.question,
            answer=request.answer,
            category=request.category
        )
        
        # Generate follow-up
        response = llm_service.generate_json(
            system_prompt=FOLLOWUP_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.4,
            max_tokens=500
        )
        
        return FollowUpResponse(
            follow_up_question=response.get('follow_up_question', ''),
            reason=response.get('reason', '')
        )
        
    except Exception as e:
        print(f"❌ Error generating follow-up: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate follow-up: {str(e)}"
        )


@router.get("/answer_tips/{category}")
async def get_answer_tips(category: str):
    """
    Get tips for answering questions in a specific category.
    
    Args:
        category: Question category (Technical, Behavioral, etc.)
        
    Returns:
        Tips for answering questions in that category
    """
    tips = {
        "Technical": [
            "Start with a high-level approach, then dive into specifics",
            "Explain your reasoning step by step",
            "Consider edge cases and optimizations",
            "If stuck, think out loud and ask clarifying questions",
            "Use appropriate data structures and algorithms"
        ],
        "Behavioral": [
            "Use the STAR method (Situation, Task, Action, Result)",
            "Be specific with examples from your experience",
            "Quantify your achievements when possible",
            "Focus on your individual contributions, not just team efforts",
            "Be honest about challenges and what you learned"
        ],
        "System Design": [
            "Clarify requirements and constraints first",
            "Start with a high-level architecture",
            "Identify key components and their interactions",
            "Consider scalability, reliability, and trade-offs",
            "Don't over-engineer - keep it simple first"
        ],
        "Problem Solving": [
            "Understand the problem fully before coding",
            "Think of multiple approaches and their trade-offs",
            "Start with a brute force solution, then optimize",
            "Test your solution with examples",
            "Explain time and space complexity"
        ]
    }
    
    category_tips = tips.get(category, tips["Technical"])
    
    return {
        "category": category,
        "tips": category_tips
    }
