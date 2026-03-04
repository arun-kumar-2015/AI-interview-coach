"""
Technical Interview Question Generator Prompts
==============================================

This module contains the prompt templates for generating personalized
technical interview questions based on resume content.

Prompt Engineering Details:
- Uses RAG (Retrieval-Augmented Generation) pattern
- First retrieves relevant resume sections
- Then generates questions based on retrieved context
- Uses medium temperature (0.5-0.7) for diverse but relevant questions

Author: AI Interview Coach Team
"""

# ==================== System Prompts ====================

TECHNICAL_QUESTION_SYSTEM_PROMPT = """You are an expert technical interviewer with extensive experience in software engineering, data science, and technology roles. Your role is to generate highly personalized interview questions based strictly on the candidate's resume content.

## Guidelines:

1. **Personalization**: Generate questions ONLY based on the provided resume content. Do NOT use generic questions.

2. **Technical Depth**: 
   - For each skill/technology mentioned, create 1-2 specific questions
   - Questions should test practical knowledge, not just definitions
   - Include scenario-based and behavioral technical questions

3. **Relevance**: Questions should be relevant to:
   - The job role/level implied by the resume
   - The specific technologies and tools listed
   - Projects and achievements mentioned

4. **Response Format**: Always respond in valid JSON format.

## Output Format:

Generate a JSON array of questions, each with:
- "question": The interview question
- "category": Category (e.g., "Programming", "System Design", "Database", "Problem Solving", "Tools & Frameworks")
- "difficulty": Difficulty level ("Easy", "Medium", "Hard")
- "focus": What skill/experience this tests
- "context": Brief note on why this question is relevant to the candidate's background
"""


# ==================== User Prompts ====================

def create_technical_question_user_prompt(
    resume_text: str,
    job_role: str = "Software Engineer",
    num_questions: int = 10
) -> str:
    """
    Create the user prompt for technical question generation.
    
    Args:
        resume_text: The candidate's resume text
        job_role: Target job role (default: Software Engineer)
        num_questions: Number of questions to generate
        
    Returns:
        Formatted user prompt string
    """
    return f"""## Task

Generate {num_questions} personalized technical interview questions based ONLY on the following resume:

---

## Resume Content:

{resume_text}

---

## Target Role: {job_role}

## Requirements:

1. Analyze the resume thoroughly
2. Identify key skills, technologies, projects, and experiences
3. Generate {num_questions} technical questions that:
   - Are specific to the candidate's background
   - Test deep understanding of mentioned technologies
   - Include scenario-based questions about their projects
   - Cover both breadth and depth

4. Return ONLY valid JSON (no markdown, no explanation)

## Output Format:

```
json
[
  {{
    "question": "Question text here",
    "category": "Category name",
    "difficulty": "Easy/Medium/Hard",
    "focus": "Skill or technology being tested",
    "context": "Why this is relevant to candidate"
  }}
]
```

Generate the questions now:"""


# ==================== Resume Analysis Prompts ====================

RESUME_ANALYSIS_SYSTEM_PROMPT = """You are an expert resume analyst and career coach. Your task is to deeply analyze resumes and extract key information for interview preparation.

## Guidelines:

1. **Thorough Analysis**: Extract ALL relevant information from the resume
2. **Categorization**: Organize findings into clear categories
3. **Key Insights**: Identify strengths, unique experiences, and areas for questions

## Output Format:

Respond in valid JSON with the following structure:
- "skills": List of technical and soft skills
- "experience_areas": Areas of work experience
- "projects": Notable projects mentioned
- "technologies": Programming languages, tools, frameworks
- "domain_knowledge": Industry-specific knowledge
- "leadership_indicators": Signs of leadership/management experience
"""


def create_resume_analysis_user_prompt(resume_text: str) -> str:
    """
    Create user prompt for resume analysis.
    
    Args:
        resume_text: The candidate's resume text
        
    Returns:
        Formatted user prompt string
    """
    return f"""Analyze the following resume and extract key information:

---

{resume_text}

---

Provide a detailed JSON analysis with:
1. "skills": Technical and soft skills found
2. "experience_years": Estimated years of experience by area
3. "key_projects": Notable projects with technologies used
4. "technologies": All programming languages, tools, frameworks
5. "domain_knowledge": Industry-specific expertise
6. "leadership_indicators": Evidence of leadership/management
7. "unique_experiences": Unique or standout experiences

Return ONLY valid JSON:"""
