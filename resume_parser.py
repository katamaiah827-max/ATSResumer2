"""
Resume parsing module.
Extracts text from uploaded PDF or TXT files and identifies core fields using regex.
Supports pypdf with fallback to PyMuPDF (fitz) or pdfplumber if available.
"""

import io
import re
from typing import Dict, List, Optional
from modules.utils import TECH_KEYWORDS, extract_keywords_from_text


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract plain text from PDF file bytes."""
    text_content = ""
    
    # 1. Primary extractor: pypdf (always available)
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text_content += t + "\n"
        if text_content.strip():
            return text_content.strip()
    except Exception:
        pass

    # 2. Secondary fallback: PyMuPDF (fitz)
    try:
        import fitz
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        for page in doc:
            t = page.get_text()
            if t:
                text_content += t + "\n"
        if text_content.strip():
            return text_content.strip()
    except Exception:
        pass

    # 3. Tertiary fallback: pdfplumber
    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    text_content += t + "\n"
        if text_content.strip():
            return text_content.strip()
    except Exception:
        pass

    return text_content.strip()


def parse_resume_content(raw_text: str) -> Dict:
    """
    Parse unstructured resume text into a structured resume dictionary.
    Extracts email, phone, names, technical skills, education degrees, etc.
    """
    resume_data = {
        "personal": {
            "full_name": "",
            "target_role": "Software Professional",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": ""
        },
        "summary": "",
        "education": [],
        "technical_skills": [],
        "soft_skills": [],
        "experience": [],
        "projects": [],
        "certifications": []
    }
    
    if not raw_text:
        return resume_data
        
    lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
    
    # 1. Extract Email
    email_match = re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', raw_text)
    if email_match:
        resume_data["personal"]["email"] = email_match.group(0)
        
    # 2. Extract Phone
    phone_match = re.search(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3,5}\)?[-.\s]?\d{3,5}[-.\s]?\d{3,5}', raw_text)
    if phone_match:
        resume_data["personal"]["phone"] = phone_match.group(0).strip()
        
    # 3. Extract Links
    linkedin_match = re.search(r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+', raw_text, re.IGNORECASE)
    if linkedin_match:
        resume_data["personal"]["linkedin"] = linkedin_match.group(0)
        
    github_match = re.search(r'(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+', raw_text, re.IGNORECASE)
    if github_match:
        resume_data["personal"]["github"] = github_match.group(0)
        
    # 4. Guess Candidate Name (usually first clean line without numbers or email)
    for line in lines[:5]:
        if not re.search(r'[@\+\d]', line) and len(line.split()) in [2, 3, 4] and not any(w in line.lower() for w in ['resume', 'curriculum', 'vitae', 'page']):
            resume_data["personal"]["full_name"] = line
            break
            
    # 5. Extract Skills using keyword taxonomy
    extracted_skills = extract_keywords_from_text(raw_text)
    resume_data["technical_skills"] = extracted_skills[:12]
    
    # Common soft skills check
    soft_list = ["Problem Solving", "Communication", "Team Collaboration", "Time Management", "Analytical Thinking"]
    found_soft = [s for s in soft_list if re.search(rf'\b{re.escape(s.lower())}\b', raw_text.lower())]
    resume_data["soft_skills"] = found_soft if found_soft else ["Problem Solving", "Communication"]
    
    # 6. Extract Summary (look for summary / profile / objective header)
    summary_match = re.search(r'(?:summary|profile|about me|objective)[:\s\n]+(.*?)(?=\n[A-Z\s]{4,}|\Z)', raw_text, re.IGNORECASE | re.DOTALL)
    if summary_match:
        cand_summary = summary_match.group(1).strip()
        # Keep under 400 chars
        resume_data["summary"] = re.sub(r'\s+', ' ', cand_summary)[:400]
    else:
        # Fallback summary based on extracted role
        resume_data["summary"] = f"Motivated professional with expertise in {', '.join(extracted_skills[:4])}. Dedicated to building robust solutions and driving engineering excellence."

    # 7. Extract Education (B.Tech, M.Tech, BS, MS, etc.)
    edu_match = re.search(r'\b(b\.?tech|m\.?tech|b\.?e|m\.?e|bca|mca|b\.?sc|m\.?sc|bachelor|master|phd)\b[^\n,.]*', raw_text, re.IGNORECASE)
    if edu_match:
        degree_found = edu_match.group(0).strip()
        resume_data["education"].append({
            "degree": degree_found,
            "field": "Computer Science & Engineering",
            "university": "University / Institute",
            "passing_year": "2022",
            "grade": "First Class"
        })
    else:
        resume_data["education"].append({
            "degree": "B.Tech",
            "field": "Computer Science & Engineering",
            "university": "University / Institute",
            "passing_year": "2022",
            "grade": "8.0 CGPA"
        })
        
    return resume_data
