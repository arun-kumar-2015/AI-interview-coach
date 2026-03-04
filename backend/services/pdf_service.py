"""
PDF Extraction Service
======================
This service handles PDF text extraction using pypdf.
It also provides text preprocessing and cleaning functionality.

Author: AI Interview Coach Team
"""

import io
from typing import Optional, List
from pypdf import PdfReader


class PDFService:
    """
    Service for extracting and processing text from PDF files.
    """
    
    @staticmethod
    def extract_text_from_pdf(file_content: bytes) -> str:
        """
        Extract text from PDF file content.
        
        Args:
            file_content: Raw PDF file bytes
            
        Returns:
            Extracted text as string
        """
        try:
            # Create a BytesIO object from the file content
            pdf_file = io.BytesIO(file_content)
            
            # Create PDF reader
            reader = PdfReader(pdf_file)
            
            # Extract text from all pages
            text_parts = []
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    text_parts.append(text)
            
            full_text = "\n\n".join(text_parts)
            
            return full_text
            
        except Exception as e:
            raise ValueError(f"Failed to extract text from PDF: {str(e)}")
    
    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean and preprocess extracted text.
        
        This includes:
        - Removing excessive whitespace
        - Fixing common PDF extraction issues
        - Normalizing line breaks
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        import re
        
        # Replace multiple whitespace with single space
        text = re.sub(r'\s+', ' ', text)
        
        # Replace multiple newlines with double newline (paragraph separator)
        text = re.sub(r'\n\s*\n', '\n\n', text)
        
        # Remove page numbers (common pattern at bottom of pages)
        text = re.sub(r'\n\s*Page\s*\d+\s*of\s*\d+\s*\n', '\n', text, flags=re.IGNORECASE)
        
        # Remove header/footer patterns (simple heuristics)
        lines = text.split('\n')
        cleaned_lines = []
        
        for i, line in enumerate(lines):
            # Skip lines that are just page numbers
            if re.match(r'^Page\s*\d+$', line.strip(), re.IGNORECASE):
                continue
            cleaned_lines.append(line)
        
        text = '\n'.join(cleaned_lines)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    @staticmethod
    def split_into_sections(text: str) -> List[dict]:
        """
        Split resume text into logical sections.
        
        This helps with better embedding and retrieval.
        Common sections: Contact Info, Summary, Experience, Education, Skills
        
        Args:
            text: Full resume text
            
        Returns:
            List of dictionaries with section name and content
        """
        import re
        
        # Common section headers in resumes
        section_patterns = [
            (r'(?i)^(contact\s*info|contact|personal\s*info).*?', 'Contact Info'),
            (r'(?i)^(summary|objective|profile|professional\s*summary).*?', 'Summary'),
            (r'(?i)^(experience|work\s*experience|employment\s*history|professional\s*experience).*?', 'Experience'),
            (r'(?i)^(education|academic\s*background|qualifications).*?', 'Education'),
            (r'(?i)^(skills|technical\s*skills|core\s*competencies|competencies).*?', 'Skills'),
            (r'(?i)^(projects|project\s*experience|key\s*projects).*?', 'Projects'),
            (r'(?i)^(certifications|certificates|licenses).*?', 'Certifications'),
            (r'(?i)^(publications|presentations).*?', 'Publications'),
        ]
        
        sections = []
        lines = text.split('\n')
        current_section = 'Other'
        current_content = []
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check if line matches a section header
            is_section_header = False
            for pattern, section_name in section_patterns:
                if re.match(pattern, line):
                    # Save previous section if has content
                    if current_content:
                        sections.append({
                            'name': current_section,
                            'content': '\n'.join(current_content)
                        })
                    
                    current_section = section_name
                    current_content = []
                    is_section_header = True
                    break
            
            if not is_section_header:
                current_content.append(line)
        
        # Add the last section
        if current_content:
            sections.append({
                'name': current_section,
                'content': '\n'.join(current_content)
            })
        
        return sections
    
    @staticmethod
    def get_text_preview(text: str, max_length: int = 500) -> str:
        """
        Get a preview of the text.
        
        Args:
            text: Full text
            max_length: Maximum length of preview
            
        Returns:
            Text preview
        """
        if len(text) <= max_length:
            return text
        
        return text[:max_length] + "..."
