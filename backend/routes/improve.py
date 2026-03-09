"""
Resume Improvement Routes
=========================

This module handles resume improvement suggestions, including:
- ATS optimization analysis
- Content improvements
- Quantification suggestions
- Formatting recommendations

Author: AI Interview Coach Team
"""

from typing import Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

# Import prompts
from prompts.resume_improver import (
    RESUME_IMPROVEMENT_SYSTEM_PROMPT,
    create_resume_improvement_user_prompt,
    ATS_CHECK_SYSTEM_PROMPT,
    create_ats_check_user_prompt
)

# Import services and prompts
pass


router = APIRouter()


# ==================== Request/Response Models ====================

class ResumeImprovementRequest(BaseModel):
    """Request model for resume improvement"""
    session_id: str
    target_role: str = "Software Engineer"
    industry: str = "Technology"


class ContentImprovement(BaseModel):
    """Content improvement suggestion"""
    section: str
    issue: str
    suggestion: str
    example: str


class QuantificationSuggestion(BaseModel):
    """Quantified bullet suggestion"""
    original: str
    improved: str
    impact: str


class ATSAnalysis(BaseModel):
    """ATS analysis results"""
    score: float
    issues: list[str]
    suggestions: list[str]
    keywords_found: list[str]
    keywords_missing: list[str]


class ResumeImprovementResponse(BaseModel):
    """Response model for resume improvement"""
    session_id: str
    overall_score: float
    ats_analysis: ATSAnalysis
    content_improvements: list[ContentImprovement]
    quantification_suggestions: list[QuantificationSuggestion]
    overall_feedback: str
    priority_actions: list[str]


class ATSCheckResponse(BaseModel):
    """Response model for ATS check"""
    ats_score: float
    parseability: dict
    keyword_analysis: dict
    format_compliance: dict
    overall_ats_readiness: str
    specific_recommendations: list[str]


# ==================== Routes ====================

@router.post("/improve_resume", response_model=ResumeImprovementResponse)
async def improve_resume(request: ResumeImprovementRequest):
    """
    Analyze and improve a resume.
    
    This endpoint provides comprehensive resume improvement suggestions:
    1. ATS Optimization:
       - Keyword analysis
       - Format compliance
       - Parseability check
       
    2. Content Improvements:
       - Section-by-section analysis
       - Action verb usage
       - Quantification suggestions
       
    3. Formatting Suggestions:
       - ATS-friendly formatting
       - Section organization
       - Length recommendations
    
    Args:
        request: ResumeImprovementRequest with session and target role
        
    Returns:
        ResumeImprovementResponse with detailed improvement suggestions
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
        
        print(f"📊 Analyzing resume for improvements...")
        
        # Create improvement prompt
        user_prompt = create_resume_improvement_user_prompt(
            resume_text=resume_text,
            target_role=request.target_role,
            industry=request.industry
        )
        
        # Generate improvement analysis
        response = llm_service.generate_json(
            system_prompt=RESUME_IMPROVEMENT_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.3,
            max_tokens=3000
        )
        
        # Parse response
        ats_data = response.get('ats_analysis', {})
        
        ats_analysis = ATSAnalysis(
            score=float(ats_data.get('score', 0)),
            issues=ats_data.get('issues', []),
            suggestions=ats_data.get('suggestions', []),
            keywords_found=ats_data.get('keywords_found', []),
            keywords_missing=ats_data.get('keywords_missing', [])
        )
        
        # Parse content improvements
        content_improvements = [
            ContentImprovement(**imp) 
            for imp in response.get('content_improvements', [])
        ]
        
        # Parse quantification suggestions
        quantification_suggestions = [
            QuantificationSuggestion(**q)
            for q in response.get('quantification_suggestions', [])
        ]
        
        print(f"✅ Resume analysis complete")
        
        return ResumeImprovementResponse(
            session_id=request.session_id,
            overall_score=float(response.get('overall_score', 0)),
            ats_analysis=ats_analysis,
            content_improvements=content_improvements,
            quantification_suggestions=quantification_suggestions,
            overall_feedback=response.get('overall_feedback', ''),
            priority_actions=response.get('priority_actions', [])
        )
        
    except Exception as e:
        print(f"❌ Error improving resume: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to improve resume: {str(e)}"
        )


@router.post("/check_ats", response_model=ATSCheckResponse)
async def check_ats_compatibility(session_id: str):
    """
    Check ATS (Applicant Tracking System) compatibility.
    
    This endpoint simulates how an ATS would parse and evaluate the resume:
    - Parseability: Can the ATS read the content?
    - Keyword Analysis: Are relevant keywords present?
    - Format Compliance: Does it follow ATS-friendly formatting?
    - Section Analysis: Are sections clearly defined?
    
    Args:
        session_id: Unique session identifier
        
    Returns:
        ATSCheckResponse with ATS compatibility analysis
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
        
        print(f"🔍 Running ATS compatibility check...")
        
        # Create ATS check prompt
        user_prompt = create_ats_check_user_prompt(resume_text)
        
        # Run ATS analysis
        response = llm_service.generate_json(
            system_prompt=ATS_CHECK_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            temperature=0.1,  # Low temperature for consistent analysis
            max_tokens=1500
        )
        
        print(f"✅ ATS check complete")
        
        return ATSCheckResponse(
            ats_score=float(response.get('ats_score', 0)),
            parseability=response.get('parseability', {}),
            keyword_analysis=response.get('keyword_analysis', {}),
            format_compliance=response.get('format_compliance', {}),
            overall_ats_readiness=response.get('overall_ats_readiness', ''),
            specific_recommendations=response.get('specific_recommendations', [])
        )
        
    except Exception as e:
        print(f"❌ Error checking ATS: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check ATS compatibility: {str(e)}"
        )


@router.get("/ats_tips")
async def get_ats_tips():
    """
    Get tips for ATS-friendly resumes.
    
    Returns:
        Tips for optimizing resumes for ATS
    """
    return {
        "general_tips": [
            "Use standard section headings (Experience, Education, Skills)",
            "Avoid tables, columns, and graphics",
            "Use standard file formats (PDF or Word .docx)",
            "Include keywords from the job description",
            "Don't hide text in headers or footers"
        ],
        "keyword_strategies": [
            "Include both spelled-out terms and acronyms",
            "Use keywords from the job posting naturally",
            "Focus on hard skills and technical abilities",
            "Include relevant certifications",
            "Add industry-specific terminology"
        ],
        "formatting_tips": [
            "Use standard fonts (Arial, Calibri, Times New Roman)",
            "Keep font size between 10-12 points",
            "Use consistent formatting throughout",
            "Avoid special characters and symbols",
            "Use bullet points for lists"
        ],
        "common_mistakes": [
            "Using tables or columns",
            "Including images or graphics",
            "Using headers and footers for important info",
            "Using non-standard section names",
            "Including confidential information"
        ]
    }
