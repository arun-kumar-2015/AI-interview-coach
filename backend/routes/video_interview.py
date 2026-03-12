from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import ast
import json

# Services are loaded lazily
pass

router = APIRouter()

class VideoInterviewRequest(BaseModel):
    role: str
    question: str
    answer: str

class VideoInterviewResponse(BaseModel):
    confidence: int
    clarity: int
    technical_accuracy: int
    feedback: str
    improvement_tips: str

@router.post("/video-interview", response_model=VideoInterviewResponse)
async def evaluate_video_interview(request: VideoInterviewRequest):
    """
    Evaluates a user's answer to a live video interview question and
    returns structured JSON feedback.
    """
    try:
        # Use the global lazy-loading LLM service from app_state
        from app_state import get_llm_service
        llm = get_llm_service()
        
        system_prompt = f"""
You are a highly critical professional corporate employer conducting a real-time job interview for a {request.role} position.
Your task is to provide an honest, accurate, and rigorous evaluation of the candidate's answer.

## Scoring Rubric (1-10):
- **1-3 (Poor)**: Vague, incorrect, or extremely brief. Shows lack of preparation or knowledge.
- **4-6 (Average)**: Basic understanding but lacks depth, examples, or clear structure.
- **7-8 (Good)**: Good understanding, clear communication, and relevant examples.
- **9-10 (Expert)**: Exceptional depth, perfect technical accuracy, highly confident, and structured (STAR method).

Evaluate based on:
1. **Confidence**: Tone (if implied by text), assertiveness, and lack of hesitation markers.
2. **Clarity**: How easy it is to understand the explanation.
3. **Technical Accuracy**: Correctness of technologies, concepts, and logic mentioned.

Output your evaluation strictly as a JSON object.
{{
  "confidence": <integer from 1 to 10>,
  "clarity": <integer from 1 to 10>,
  "technical_accuracy": <integer from 1 to 10>,
  "feedback": "<An honest, professional paragraph providing specific feedback on their answer>",
  "improvement_tips": "<Specific, actionable advice on how they can improve their response>"
}}
"""
        
        import time
        t1 = time.time()
        print(f"⏱️ [TIMING] Starting LLM Video Evaluation...")
        
        user_prompt = f"Question: {request.question}\nCandidate's Answer: {request.answer}"
        
        # Use generate_json for robust parsing and correct method call
        # Removed 'await' because generate_json is synchronous
        evaluation = llm.generate_json(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.2
        )
        
        t2 = time.time()
        print(f"⏱️ [TIMING] Video Evaluation took {t2 - t1:.2f} seconds")

        # Helper to get keys case-insensitively
        def get_val(data, target_key, default):
            for k, v in data.items():
                if k.lower() == target_key.lower():
                    return v
            return default
        
        return VideoInterviewResponse(
            confidence=int(get_val(evaluation, "confidence", 5)),
            clarity=int(get_val(evaluation, "clarity", 5)),
            technical_accuracy=int(get_val(evaluation, "technical_accuracy", 5)),
            feedback=get_val(evaluation, "feedback", "No specific feedback generated."),
            improvement_tips=get_val(evaluation, "improvement_tips", "No specific tips generated.")
        )

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from LLM: {response_text}")
        raise HTTPException(status_code=500, detail="Failed to parse structured feedback from AI model.")
    except Exception as e:
        print(f"Error evaluating answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
