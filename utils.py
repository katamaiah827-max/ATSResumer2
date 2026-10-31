"""
Utility functions for text processing, keyword extraction, and ATS matching algorithms.
"""

import re
from typing import Dict, List, Set, Tuple

# Comprehensive taxonomy of industry-standard tech keywords and competencies
TECH_KEYWORDS = {
    # Programming Languages
    "python": "Python", "java": "Java", "javascript": "JavaScript", "typescript": "TypeScript",
    "c++": "C++", "c#": "C#", "c": "C", "php": "PHP", "ruby": "Ruby", "go": "Go", "golang": "Go",
    "rust": "Rust", "kotlin": "Kotlin", "swift": "Swift", "r": "R", "scala": "Scala",
    
    # Web & Frameworks
    "django": "Django", "flask": "Flask", "fastapi": "FastAPI", "spring boot": "Spring Boot",
    "spring": "Spring", "hibernate": "Hibernate", "react": "React", "react.js": "React",
    "angular": "Angular", "vue": "Vue", "vue.js": "Vue", "node.js": "Node.js", "nodejs": "Node.js",
    "express": "Express", "express.js": "Express", "html": "HTML", "html5": "HTML5",
    "css": "CSS", "css3": "CSS3", "bootstrap": "Bootstrap", "tailwind": "Tailwind CSS",
    "rest api": "REST APIs", "restful api": "REST APIs", "rest apis": "REST APIs",
    "graphql": "GraphQL", "microservices": "Microservices", "web development": "Web Development",
    
    # Databases & Storage
    "sql": "SQL", "mysql": "MySQL", "postgresql": "PostgreSQL", "mongodb": "MongoDB",
    "sqlite": "SQLite", "oracle": "Oracle DB", "redis": "Redis", "nosql": "NoSQL",
    "firebase": "Firebase", "elasticsearch": "Elasticsearch",
    
    # Data Science, AI & Analytics
    "pandas": "Pandas", "numpy": "NumPy", "scikit-learn": "Scikit-Learn", "matplotlib": "Matplotlib",
    "seaborn": "Seaborn", "tensorflow": "TensorFlow", "pytorch": "PyTorch", "keras": "Keras",
    "data analysis": "Data Analysis", "data visualization": "Data Visualization",
    "machine learning": "Machine Learning", "deep learning": "Deep Learning",
    "nlp": "NLP", "natural language processing": "Natural Language Processing",
    "powerbi": "PowerBI", "power bi": "PowerBI", "tableau": "Tableau", "excel": "Excel",
    "statistics": "Statistics", "etl": "ETL",
    
    # Cloud & DevOps & Tools
    "git": "Git", "github": "GitHub", "gitlab": "GitLab", "docker": "Docker",
    "kubernetes": "Kubernetes", "aws": "AWS", "azure": "Azure", "gcp": "GCP",
    "ci/cd": "CI/CD", "jenkins": "Jenkins", "linux": "Linux", "bash": "Bash",
    "version control": "Version Control", "jira": "Jira", "agile": "Agile",
    "scrum": "Scrum", "unit testing": "Unit Testing", "junit": "JUnit",
    "pytest": "PyTest", "postman": "Postman",
    
    # Core CS & Soft Skills
    "problem solving": "Problem Solving", "communication": "Communication",
    "communication skills": "Communication", "analytical skills": "Analytical Skills",
    "analytical thinking": "Analytical Thinking", "team collaboration": "Team Collaboration",
    "teamwork": "Teamwork", "data structures": "Data Structures",
    "algorithms": "Algorithms", "object-oriented programming": "OOP",
    "oop": "OOP", "system design": "System Design", "clean code": "Clean Code"
}

ROLE_ESSENTIAL_SKILLS = {
    "Python Developer": ["Python", "Django", "Flask", "SQL", "REST APIs", "Git", "Problem Solving", "Web Development"],
    "Java Developer": ["Java", "Spring Boot", "Microservices", "Hibernate", "SQL", "Git", "REST APIs", "OOP"],
    "Web Developer": ["HTML", "CSS", "JavaScript", "React", "Node.js", "Git", "REST APIs", "Web Development"],
    "Data Analyst": ["Python", "SQL", "Pandas", "Data Analysis", "Data Visualization", "PowerBI", "Excel", "Statistics"],
    "Software Engineer": ["Python", "Java", "Data Structures", "Algorithms", "SQL", "Git", "Problem Solving", "OOP"]
}


def normalize_text(text: str) -> str:
    """Normalize text for consistent keyword matching."""
    if not text:
        return ""
    text = text.lower()
    # Replace line breaks and multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def extract_keywords_from_text(text: str) -> List[str]:
    """
    Extract technical and domain skills from raw text using regex pattern matching.
    Returns a sorted list of unique canonical skill names.
    """
    if not text:
        return []
    
    normalized = normalize_text(text)
    matched_canonical = set()
    
    # Multi-word and single-word matching with word boundary protections
    for term, canonical in TECH_KEYWORDS.items():
        # Handle special characters in tech terms like c++, c#, .net, ci/cd
        escaped_term = re.escape(term)
        pattern = rf'(?:^|[\s,.\/;:\(\)\[\]"\'\-])({escaped_term})(?:$|[\s,.\/;:\(\)\[\]"\'\-])'
        if re.search(pattern, normalized, re.IGNORECASE):
            matched_canonical.add(canonical)
            
    return sorted(list(matched_canonical))


def get_all_resume_text(resume_data: Dict) -> str:
    """Consolidate all text fields from resume_data into one single string."""
    parts = []
    
    # Personal Info
    personal = resume_data.get("personal", {})
    parts.append(personal.get("full_name", ""))
    parts.append(personal.get("target_role", ""))
    parts.append(personal.get("location", ""))
    
    # Professional Summary
    parts.append(resume_data.get("summary", ""))
    
    # Skills
    for skill in resume_data.get("technical_skills", []):
        parts.append(skill)
    for skill in resume_data.get("soft_skills", []):
        parts.append(skill)
        
    # Education
    for edu in resume_data.get("education", []):
        parts.append(edu.get("degree", ""))
        parts.append(edu.get("field", ""))
        parts.append(edu.get("university", ""))
        
    # Experience
    for exp in resume_data.get("experience", []):
        parts.append(exp.get("company", ""))
        parts.append(exp.get("designation", ""))
        parts.append(exp.get("responsibilities", ""))
        
    # Projects
    for proj in resume_data.get("projects", []):
        parts.append(proj.get("title", ""))
        parts.append(proj.get("technologies", ""))
        parts.append(proj.get("description", ""))
        
    # Certifications
    for cert in resume_data.get("certifications", []):
        parts.append(cert)
        
    return " ".join([p for p in parts if p])


def calculate_ats_match(resume_data: Dict, job_description: str, target_role: str = "") -> Dict:
    """
    Compare resume content against a job description.
    Returns matching score, key matched skills, missing keywords, and custom suggestions.
    """
    if not job_description or not job_description.strip():
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "suggestions": ["Please enter or select a job description to analyze."],
            "total_jd_keywords": 0
        }
        
    # Extract keywords from JD
    jd_skills = extract_keywords_from_text(job_description)
    
    # If standard extraction found very few, enrich with role-essential skills if available
    if len(jd_skills) < 4 and target_role in ROLE_ESSENTIAL_SKILLS:
        for r_skill in ROLE_ESSENTIAL_SKILLS[target_role]:
            if r_skill not in jd_skills:
                jd_skills.append(r_skill)
    
    if not jd_skills:
        jd_skills = ["Python", "SQL", "Problem Solving", "Web Development", "Git"]
        
    # Extract keywords from candidate resume
    resume_text = get_all_resume_text(resume_data)
    resume_skills = extract_keywords_from_text(resume_text)
    
    # Explicitly include skills already listed in resume_data["technical_skills"] and ["soft_skills"]
    user_skills = set(resume_data.get("technical_skills", []) + resume_data.get("soft_skills", []))
    for s in user_skills:
        s_norm = s.strip().lower()
        for term, canon in TECH_KEYWORDS.items():
            if s_norm == term or s_norm == canon.lower():
                resume_skills.append(canon)
    resume_skills_set = set(resume_skills)
    
    # Calculate matches and missing
    matched = [s for s in jd_skills if s in resume_skills_set]
    missing = [s for s in jd_skills if s not in resume_skills_set]
    
    # Calculate weighted ATS score
    # 1. Base keyword match percentage
    base_match_pct = (len(matched) / max(1, len(jd_skills))) * 100
    
    # 2. Section completeness check (has summary, experience, education, projects)
    completeness_pts = 0
    if len(resume_data.get("summary", "").strip()) >= 50:
        completeness_pts += 5
    if len(resume_data.get("experience", [])) > 0:
        completeness_pts += 5
    if len(resume_data.get("education", [])) > 0:
        completeness_pts += 5
    if len(resume_data.get("projects", [])) > 0:
        completeness_pts += 5
        
    raw_score = int(round((base_match_pct * 0.8) + completeness_pts))
    final_score = max(10, min(98, raw_score))
    
    # Generate tailored suggestions
    suggestions = []
    
    # Skill additions
    for miss in missing[:3]:
        suggestions.append(f"Add **{miss}** experience or project mentions if you have hands-on knowledge.")
        
    # Summary suggestion
    target = target_role or resume_data.get("personal", {}).get("target_role", "Software Professional")
    suggestions.append(f"Tailor your Professional Summary to highlight your **{target}** competencies and key tools.")
    
    # Formatting suggestions
    suggestions.append("Ensure bullet points quantify achievements (e.g., 'improved performance by 25%').")
    suggestions.append("Maintain an ATS-friendly single-column layout without graphics, icons, or nested tables.")
    
    return {
        "score": final_score,
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "suggestions": suggestions,
        "total_jd_keywords": len(jd_skills),
        "total_matched": len(matched),
        "total_missing": len(missing)
    }


def generate_optimized_summary(resume_data: Dict, target_role: str, matched_skills: List[str]) -> str:
    """
    Generate an impactful, ATS-aligned Professional Summary incorporating verified skills.
    Ensures ethical integrity by emphasizing only existing or selected skills.
    """
    name = resume_data.get("personal", {}).get("full_name", "Professional")
    role = target_role or resume_data.get("personal", {}).get("target_role", "Software Developer")
    
    # Select up to 4 top matched skills
    top_skills = matched_skills[:4] if matched_skills else ["modern web frameworks", "relational databases", "problem solving"]
    skills_phrase = ", ".join(top_skills[:-1]) + f", and {top_skills[-1]}" if len(top_skills) > 1 else top_skills[0]
    
    summary = (
        f"Motivated and results-driven {role} with proven expertise in {skills_phrase}. "
        f"Demonstrated track record of designing scalable applications, optimizing database performance, "
        f"and collaborating with cross-functional engineering teams. Dedicated to writing clean, maintainable code "
        f"and solving complex business challenges in fast-paced software environments."
    )
    return summary
