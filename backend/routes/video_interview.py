from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import ast
import json

# Assuming we can import the globally initialized llm_service from main
# Alternatively, we could instantiate a service here or pass it in.
# For simplicity, we'll try to get it from the app state or simply re-import it.
from services.llm_service import LLMService

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
        # We can grab a fresh instance or the global one.
        # It's quick to instantiate if we just need the client.
        llm = LLMService()
        
        system_prompt = f"""
You are a professional corporate employer conducting a real-time job interview for a {request.role} position.
Evaluate the candidate's answer based on:
- Confidence
- Clarity
- Technical Accuracy

Output your evaluation strictly as a JSON object with NO OTHER TEXT. DO NOT wrap the JSON in Markdown code blocks (e.g. no ```json).
The JSON MUST have the following structure and precise keys:
{{
  "confidence": <integer from 1 to 10>,
  "clarity": <integer from 1 to 10>,
  "technical_accuracy": <integer from 1 to 10>,
  "feedback": "<A professional paragraph providing specific feedback on their answer>",
  "improvement_tips": "<Actionable advice on how they can improve their response>"
}}
"""
        
        user_prompt = f"Question: {request.question}\nCandidate's Answer: {request.answer}"
        
        response_text = await llm.generate_response(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=0.3
        )
        
        # In a robust implementation, we might use openai function calling, 
        # but parsing stringified dict works for basic models.
        import json
        
        # Clean the response to ensure it's just JSON (sometimes models still add markdown blocks despite instructions)
        clean_text = response_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.startswith("```"):
            clean_text = clean_text[3:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
            
        clean_text = clean_text.strip()
            
        evaluation = json.loads(clean_text)
        
        return VideoInterviewResponse(
            confidence=evaluation.get("confidence", 5),
            clarity=evaluation.get("clarity", 5),
            technical_accuracy=evaluation.get("technical_accuracy", 5),
            feedback=evaluation.get("feedback", "No specific feedback generated."),
            improvement_tips=evaluation.get("improvement_tips", "No specific tips generated.")
        )

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON from LLM: {response_text}")
        raise HTTPException(status_code=500, detail="Failed to parse structured feedback from AI model.")
    except Exception as e:
        print(f"Error evaluating answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
