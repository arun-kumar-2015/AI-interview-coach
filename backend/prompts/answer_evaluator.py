"""
Answer Evaluation Prompts
=========================

This module contains prompt templates for evaluating interview answers.

Prompt Engineering:
- Uses low temperature (0.0-0.2) for consistent, fair evaluation
- Evaluates based on: relevance, depth, structure, examples
- Provides constructive feedback

Author: AI Interview Coach Team
"""

# ==================== System Prompts ====================

ANSWER_EVALUATION_SYSTEM_PROMPT = """You are an expert technical interviewer evaluating a candidate's answer to an interview question. Your role is to provide fair, constructive, and detailed feedback.

## Evaluation Criteria:

1. **Relevance** (0-2 points): Does the answer address the question?
2. **Technical Accuracy** (0-3 points): Is the technical content correct?
3. **Depth of Understanding** (0-2 points): Shows deep vs surface understanding
4. **Communication** (0-2 points): Clear, structured, concise communication
5. **STAR Format** (0-1 points): For behavioral questions, follows STAR

Total: 10 points maximum

## Feedback Structure:

For each answer, provide:
- Overall score (0-10)
- Strengths: What the candidate did well
- Improvements: Specific areas to improve
- Suggested approach: How to improve the answer

## Important:
- Be constructive and encouraging
- Provide specific, actionable feedback
- Focus on helping the candidate improve

Respond in valid JSON format.
"""


# ==================== User Prompts ====================

def create_evaluation_user_prompt(
    question: str,
    answer: str,
    category: str = "Technical",
    resume_context: str = ""
) -> str:
    """
    Create user prompt for answer evaluation.
    
    Args:
        question: The interview question asked
        answer: The candidate's answer
        category: Question category (Technical, Behavioral, etc.)
        resume_context: Optional resume context for personalization
        
    Returns:
        Formatted user prompt string
    """
    context_note = f"\n\nCandidate's Background:\n{resume_context}" if resume_context else ""
    
    return f"""## Task

Evaluate the following interview answer:

---

## Question:
{question}

## Candidate's Answer:
{answer}

## Category: {category}{context_note}

---

## Output Requirements:

Provide a detailed evaluation in JSON format:

```
json
{{
  "score": <0-10>,
  "breakdown": {{
    "relevance": <0-2>,
    "technical_accuracy": <0-3>,
    "depth": <0-2>,
    "communication": <0-2>,
    "star_format": <0-1> (0 if not applicable)
  }},
  "strengths": [
    "Strength 1",
    "Strength 2"
  ],
  "improvements": [
    "Improvement suggestion 1",
    "Improvement suggestion 2"
  ],
  "suggested_answer": "Brief overview of a better approach",
  "overall_feedback": "Summary comment for the candidate"
}}
```

Evaluate now:"""


# ==================== Follow-up Question Generator ====================

FOLLOWUP_SYSTEM_PROMPT = """You are an expert interviewer. Based on a candidate's answer, generate a thoughtful follow-up question that:
1. Digs deeper into their response
2. Tests their depth of knowledge
3. Clarifies any vague points

Respond in JSON format with the follow-up question.
"""


def create_followup_user_prompt(
    question: str,
    answer: str,
    category: str = "Technical"
) -> str:
    """
    Create prompt for generating follow-up questions.
    
    Args:
        question: Original interview question
        answer: Candidate's answer
        category: Question category
        
    Returns:
        Formatted prompt string
    """
    return f"""Based on this interview Q&A, generate ONE insightful follow-up question:

Question: {question}

Answer: {answer}

Category: {category}

Generate a follow-up that:
- Tests deeper understanding
- Explores edge cases
- Asks for specific examples

Return JSON:
```
json
{{
  "follow_up_question": "The follow-up question",
  "reason": "Why this follow-up is valuable"
}}
```
"""
