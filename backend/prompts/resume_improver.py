"""
Resume Improvement Prompts
=========================

This module contains prompt templates for resume improvement suggestions,
including ATS optimization and content enhancement.

Author: AI Interview Coach Team
"""

# ==================== System Prompts ====================

RESUME_IMPROVEMENT_SYSTEM_PROMPT = """You are an expert resume writer and ATS (Applicant Tracking System) optimization specialist. Your role is to analyze resumes and provide actionable improvement suggestions.

## Areas of Expertise:

1. **ATS Optimization**:
   - Keyword optimization for ATS scanners
   - Proper formatting (no tables, graphics, headers/footers)
   - Standard section headings
   - File format recommendations

2. **Content Improvements**:
   - Quantifying achievements
   - Action verb usage
   - Clear and concise language
   - Removing redundant information

3. **Structure Improvements**:
   - Logical flow
   - Appropriate length
   - Relevance to target role

## Output Format:

Respond in valid JSON with detailed improvement suggestions.
"""


# ==================== User Prompts ====================

def create_resume_improvement_user_prompt(
    resume_text: str,
    target_role: str = "Software Engineer",
    industry: str = "Technology"
) -> str:
    """
    Create user prompt for resume improvement analysis.
    
    Args:
        resume_text: The candidate's resume text
        target_role: Target job role
        industry: Industry sector
        
    Returns:
        Formatted user prompt string
    """
    return f"""## Task

Analyze the following resume and provide comprehensive improvement suggestions:

---

## Resume:

{resume_text}

---

## Target Role: {target_role}
## Industry: {industry}

---

## Output Requirements:

Provide a detailed JSON analysis with the following structure:

```
json
{{
  "overall_score": <1-10>,
  "ats_analysis": {{
    "score": <1-10>,
    "issues": ["Issue 1", "Issue 2"],
    "suggestions": ["Suggestion 1", "Suggestion 2"],
    "keywords_found": ["keyword1", "keyword2"],
    "keywords_missing": ["keyword3", "keyword4"]
  }},
  "content_improvements": [
    {{
      "section": "Experience",
      "issue": "Current issue description",
      "suggestion": "How to improve",
      "example": "Better formatted example"
    }}
  ],
  "quantification_suggestions": [
    {{
      "original": "Original bullet",
      "improved": "Quantified version",
      "impact": "Why this is better"
    }}
  ],
  "action_verbs_analysis": {{
    "current_verbs_used": ["verb1", "verb2"],
    "strong_verbs_to_add": ["verb3", "verb4"],
    "weak_verbs_to_replace": ["weak1 -> strong1"]
  }},
  "formatting_suggestions": {{
    "issues": ["Issue 1"],
    "recommendations": ["Recommendation 1"]
  }},
  "overall_feedback": "Summary of key improvements",
  "priority_actions": ["Action 1", "Action 2", "Action 3"]
}}
```

Analyze the resume now:"""


# ==================== ATS Checker Prompts ====================

ATS_CHECK_SYSTEM_PROMPT = """You are an ATS (Applicant Tracking System) simulation tool. Analyze resumes as ATS software would and provide scoring and feedback.

## ATS Criteria:

1. **Parseability**: Can the ATS read the content?
2. **Keyword Density**: Are relevant keywords present?
3. **Format Compliance**: Does it follow ATS-friendly formatting?
4. **Content Structure**: Are sections clearly defined?

Respond in JSON format.
"""


def create_ats_check_user_prompt(resume_text: str) -> str:
    """
    Create prompt for ATS compatibility check.
    
    Args:
        resume_text: Resume text to check
        
    Returns:
        Formatted prompt string
    """
    return f"""Simulate an ATS scan on this resume:

---

{resume_text}

---

Provide ATS analysis in JSON:

```
json
{{
  "ats_score": <1-100>,
  "parseability": {{
    "score": <1-10>,
    "issues": ["parsing issue if any"]
  }},
  "keyword_analysis": {{
    "technical_keywords": ["found keywords"],
    "missing_keywords": ["keywords that should be added"],
    "keyword_density": "good/medium/poor"
  }},
  "format_compliance": {{
    "score": <1-10>,
    "issues": ["format issue if any"],
    "recommendations": ["format recommendation"]
  }},
  "section_analysis": {{
    "sections_found": ["section1"],
    "missing_sections": ["section if missing"],
    "section_order": "logical/illogical"
  }},
  "overall_ats_readiness": "good/needs_work/poor",
  "specific_recommendations": ["recommendation1"]
}}
```

Run ATS analysis:"""
