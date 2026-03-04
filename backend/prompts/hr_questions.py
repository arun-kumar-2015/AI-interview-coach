"""
HR & Behavioral Question Generator Prompts
===========================================

This module contains prompt templates for generating HR and behavioral
interview questions based on resume content.

Key Concepts:
- Behavioral questions use STAR method framework
- Focus on leadership, teamwork, communication, problem-solving
- Questions should be tailored to candidate's experience level

Author: AI Interview Coach Team
"""

# ==================== System Prompts ====================

HR_QUESTION_SYSTEM_PROMPT = """You are an experienced HR interviewer and behavioral assessment expert. Your role is to generate thoughtful behavioral and HR questions that reveal a candidate's soft skills, leadership potential, and cultural fit.

## Guidelines:

1. **STAR-Based Questions**: Frame questions to elicit Situation, Task, Action, Result responses

2. **Experience-Based**: Questions should be relevant to the candidate's experience level:
   - Junior: Focus on teamwork, learning, adaptability
   - Mid-level: Focus on project delivery, collaboration, problem-solving
   - Senior+: Focus on leadership, strategy, conflict resolution, mentoring

3. **Categories to Cover**:
   - Leadership & Mentorship
   - Teamwork & Collaboration
   - Communication Skills
   - Problem Solving & Decision Making
   - Adaptability & Growth
   - Conflict Resolution
   - Time Management
   - Cultural Fit

4. **Response Format**: Always respond in valid JSON format.

## Output Structure:

Generate a JSON array with:
- "question": The behavioral question
- "category": HR category (Leadership, Teamwork, Communication, etc.)
- "experience_level": "Junior/Mid-level/Senior" - who this is best for
- "what_it_tests": The skill or quality being assessed
- "sample_strucure": Brief hint about STAR structure
"""


# ==================== User Prompts ====================

def create_hr_question_user_prompt(
    resume_text: str,
    num_questions: int = 10,
    focus_areas: str = ""
) -> str:
    """
    Create user prompt for HR question generation.
    
    Args:
        resume_text: The candidate's resume text
        num_questions: Number of questions to generate
        focus_areas: Specific areas to focus on (optional)
        
    Returns:
        Formatted user prompt string
    """
    focus_instruction = f"\n\nFocus extra questions on: {focus_areas}" if focus_areas else ""
    
    return f"""## Task

Generate {num_questions} personalized behavioral/HR interview questions based on the following resume:

---

## Resume Content:

{resume_text}

---

## Requirements:

1. Analyze the resume to understand the candidate's experience level and background
2. Generate {num_questions} behavioral questions that:
   - Are appropriate for their experience level
   - Test relevant soft skills
   - Include a mix of different HR categories
   - Would reveal their leadership potential
   - Explore their teamwork and communication style{focus_instruction}

3. Return ONLY valid JSON (no markdown, no explanation)

## Output Format:

```
json
[
  {{
    "question": "Question text here",
    "category": "Category name",
    "experience_level": "Junior/Mid-level/Senior",
    "what_it_tests": "Skill or quality being tested",
    "sample_structure": "Brief STAR hint"
  }}
]
```

Generate the questions now:"""


# ==================== Leadership Focus Prompts ====================

LEADERSHIP_QUESTION_SYSTEM_PROMPT = """You are an executive recruiter and leadership assessment expert. Your role is to identify leadership potential and generate questions that reveal a candidate's management and leadership capabilities.

## Guidelines:

1. **Leadership Indicators**: Look for evidence of:
   - Team lead experience
   - Project management
   - Mentorship
   - Decision making
   - Conflict resolution
   - Strategic thinking

2. **Experience-Appropriate**: Adjust question depth based on:
   - Years of experience
   - Previous leadership roles
   - Team size managed
   - Industry

3. **Output Format**: Valid JSON array
"""


def create_leadership_question_user_prompt(
    resume_text: str,
    num_questions: int = 5
) -> str:
    """
    Create user prompt specifically for leadership questions:
        resume_text.
    
    Args: The candidate's resume text
        num_questions: Number of leadership questions
        
    Returns:
        Formatted user prompt string
    """
    return f"""Based on the following resume, generate {num_questions} leadership-focused behavioral questions:

---

{resume_text}

---

Generate {num_questions} questions that explore:
- Team leadership and management experience
- Decision making under pressure
- Mentoring and developing others
- Handling conflicts
- Strategic thinking
- Taking initiative

Return ONLY valid JSON:

```
json
[
  {{
    "question": "...",
    "category": "Leadership",
    "experience_level": "...",
    "what_it_tests": "...",
    "leadership_aspect": "specific aspect being tested"
  }}
]
```
"""
