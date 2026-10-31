"""
Module 2: Resume Creation (Stages 2 & 3)
Allows users to enter personal information, educational qualifications, 
technical skills, work experience, projects, and certifications.
Supports optional PDF upload to parse and auto-populate fields.
"""

import copy
import streamlit as st
from modules.sample_data import DEFAULT_RESUME
from modules.resume_parser import extract_text_from_pdf, parse_resume_content


def render_resume_builder():
    """Render the full interactive Resume Builder interface."""
    
    st.markdown("## 📝 Create Your Resume")
    st.markdown("Fill in your details below or upload an existing resume to automatically parse your information.")
    
    # Quick Actions Row
    q1, q2, q3 = st.columns([1.5, 1.5, 1])
    with q1:
        if st.button("📋 Load Sample Data (M. Katamaiah)", use_container_width=True):
            st.session_state["resume_data"] = copy.deepcopy(DEFAULT_RESUME)
            st.session_state["target_role"] = "Python Developer"
            st.success("Loaded demo resume data!")
            st.rerun()
            
    with q2:
        if st.button("🗑️ Reset All Fields", use_container_width=True):
            st.session_state["resume_data"] = {
                "personal": {"full_name": "", "target_role": "Python Developer", "email": "", "phone": "", "location": "", "linkedin": "", "github": ""},
                "summary": "",
                "education": [{"degree": "B.Tech", "field": "Computer Science", "university": "", "passing_year": "2024", "grade": ""}],
                "technical_skills": [],
                "soft_skills": [],
                "experience": [],
                "projects": [],
                "certifications": []
            }
            st.info("Resume fields cleared.")
            st.rerun()

    # Optional PDF Upload parsing
    with st.expander("📄 Or Import From Existing Resume (PDF / TXT)", expanded=False):
        uploaded_file = st.file_uploader("Upload resume file", type=["pdf", "txt"], key="resume_uploader")
        if uploaded_file is not None:
            if st.button("Extract and Auto-Fill"):
                with st.spinner("Extracting resume details..."):
                    if uploaded_file.name.endswith(".pdf"):
                        raw_text = extract_text_from_pdf(uploaded_file.read())
                    else:
                        raw_text = uploaded_file.read().decode("utf-8", errors="ignore")
                    
                    parsed = parse_resume_content(raw_text)
                    st.session_state["resume_data"] = parsed
                    st.success("Extracted details from your resume! Review and edit the fields below.")
                    st.rerun()

    resume_data = st.session_state["resume_data"]
    personal = resume_data.setdefault("personal", {})
    
    # ==========================================================
    # STAGE 2: PERSONAL & EDUCATIONAL DETAILS
    # ==========================================================
    st.markdown("""
        <div class="step-container">
            <div class="step-item completed"><div class="step-circle">✓</div>1. App Open</div>
            <div class="step-item active"><div class="step-circle">2</div>2. Personal & Edu</div>
            <div class="step-item"><div class="step-circle">3</div>3. Skills & Exp</div>
            <div class="step-item"><div class="step-circle">4</div>4. Job Desc</div>
            <div class="step-item"><div class="step-circle">5</div>5. Analysis</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 👤 Personal Information")
    with st.container():
        p1, p2, p3 = st.columns([1.2, 1.2, 1])
        with p1:
            personal["full_name"] = st.text_input("Full Name *", value=personal.get("full_name", "M. Katamaiah"))
            personal["email"] = st.text_input("Email *", value=personal.get("email", "katamaiah@example.com"))
        with p2:
            personal["target_role"] = st.text_input("Target Job Role *", value=personal.get("target_role", "Python Developer"))
            personal["phone"] = st.text_input("Phone Number *", value=personal.get("phone", "+91 9876543210"))
        with p3:
            personal["location"] = st.text_input("Location", value=personal.get("location", "Hyderabad, India"))
            personal["linkedin"] = st.text_input("LinkedIn Profile", value=personal.get("linkedin", "linkedin.com/in/mkatamaiah"))
            
        personal["github"] = st.text_input("GitHub / Portfolio URL", value=personal.get("github", "github.com/mkatamaiah"))

    st.markdown("---")
    
    # Professional Summary
    st.markdown("### 📄 Professional Summary")
    resume_data["summary"] = st.text_area(
        "Brief overview of your experience and career objectives (ATS-friendly summary):",
        value=resume_data.get("summary", ""),
        height=100
    )

    st.markdown("---")
    
    # Educational Qualifications
    st.markdown("### 🎓 Educational Qualifications")
    education_list = resume_data.setdefault("education", [])
    if not education_list:
        education_list.append({"degree": "B.Tech", "field": "Computer Science and Engineering", "university": "JNTU Hyderabad", "passing_year": "2020", "grade": "8.4 CGPA"})
    
    for idx, edu in enumerate(education_list):
        e1, e2, e3, e4 = st.columns([1, 1.2, 1, 0.8])
        with e1:
            edu["degree"] = st.text_input(f"Degree * (Entry #{idx+1})", value=edu.get("degree", "B.Tech"), key=f"edu_deg_{idx}")
        with e2:
            edu["university"] = st.text_input("University / College *", value=edu.get("university", "JNTU Hyderabad"), key=f"edu_uni_{idx}")
        with e3:
            edu["field"] = st.text_input("Field / Branch", value=edu.get("field", "CSE"), key=f"edu_field_{idx}")
        with e4:
            edu["passing_year"] = st.text_input("Passing Year *", value=edu.get("passing_year", "2020"), key=f"edu_yr_{idx}")
            edu["grade"] = st.text_input("CGPA / %", value=edu.get("grade", "8.4 CGPA"), key=f"edu_gr_{idx}")

    edu_btn_col1, edu_btn_col2 = st.columns([1, 4])
    with edu_btn_col1:
        if st.button("➕ Add Another Degree"):
            education_list.append({"degree": "", "field": "", "university": "", "passing_year": "", "grade": ""})
            st.rerun()

    st.markdown("---")
    
    # ==========================================================
    # STAGE 3: SKILLS, EXPERIENCE AND PROJECTS
    # ==========================================================
    st.markdown("### 🛠️ Technical Skills & Core Competencies")
    
    current_skills = resume_data.setdefault("technical_skills", [])
    
    # Render skill badges
    if current_skills:
        skill_badges_html = "<div>"
        for s in current_skills:
            skill_badges_html += f'<span class="skill-tag">{s}</span>'
        skill_badges_html += "</div>"
        st.markdown(skill_badges_html, unsafe_allow_html=True)
    else:
        st.caption("No technical skills added yet.")
        
    sk_col1, sk_col2 = st.columns([3, 1])
    with sk_col1:
        new_skill = st.text_input("Add a skill (e.g. Python, Django, SQL, React, AWS):", key="new_skill_input")
    with sk_col2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("➕ Add Skill", use_container_width=True):
            if new_skill and new_skill.strip():
                clean_s = new_skill.strip()
                if clean_s not in current_skills:
                    current_skills.append(clean_s)
                    st.rerun()
                    
    # Quick add skill shortcuts
    st.markdown("**Quick Add Recommendations for " + personal.get("target_role", "Developer") + ":**")
    quick_suggestions = ["Python", "Django", "Flask", "SQL", "JavaScript", "MySQL", "REST APIs", "Git", "Pandas", "Problem Solving", "Communication"]
    q_cols = st.columns(6)
    for i, qs in enumerate(quick_suggestions[:6]):
        with q_cols[i]:
            if st.button(f"+ {qs}", key=f"quick_sk_{qs}"):
                if qs not in current_skills:
                    current_skills.append(qs)
                    st.rerun()

    st.markdown("---")
    
    # Work Experience
    st.markdown("### 💼 Work Experience & Internships")
    experiences = resume_data.setdefault("experience", [])
    if not experiences:
        experiences.append({
            "company": "ABC Technologies",
            "designation": "Software Developer",
            "duration": "2021 - 2023",
            "location": "Hyderabad, India",
            "responsibilities": (
                "Developed scalable backend web applications and RESTful APIs using Python and Django.\n"
                "Designed and optimized SQL database schemas, reducing query response times by 30%.\n"
                "Collaborated with agile engineering teams to deploy microservices and implement automated testing."
            )
        })
        
    for idx, exp in enumerate(experiences):
        with st.expander(f"🏢 Experience #{idx+1}: {exp.get('designation', 'Role')} at {exp.get('company', 'Company')}", expanded=True):
            we1, we2, we3 = st.columns([1.2, 1.2, 1])
            with we1:
                exp["company"] = st.text_input("Company Name *", value=exp.get("company", ""), key=f"exp_comp_{idx}")
                exp["location"] = st.text_input("Location", value=exp.get("location", ""), key=f"exp_loc_{idx}")
            with we2:
                exp["designation"] = st.text_input("Designation / Title *", value=exp.get("designation", ""), key=f"exp_desig_{idx}")
            with we3:
                exp["duration"] = st.text_input("Duration * (e.g. 2021 - 2023)", value=exp.get("duration", ""), key=f"exp_dur_{idx}")
                
            exp["responsibilities"] = st.text_area(
                "Responsibilities & Achievements (one bullet per line):",
                value=exp.get("responsibilities", ""),
                height=90,
                key=f"exp_resp_{idx}"
            )
            
            if st.button(f"🗑️ Remove Experience #{idx+1}", key=f"rm_exp_{idx}"):
                experiences.pop(idx)
                st.rerun()

    if st.button("➕ Add Another Work Experience"):
        experiences.append({"company": "", "designation": "", "duration": "", "location": "", "responsibilities": ""})
        st.rerun()

    st.markdown("---")
    
    # Projects
    st.markdown("### 🚀 Projects & Achievements")
    projects = resume_data.setdefault("projects", [])
    if not projects:
        projects.append({
            "title": "ATS Resumer – Resume Builder and Optimizer",
            "technologies": "Python, Streamlit, Pandas, ReportLab",
            "description": "Engineered an automated ATS resume optimizer that analyzes job descriptions, calculates keyword match scores, and compiles clean, single-column ATS-friendly PDFs."
        })
        
    for idx, proj in enumerate(projects):
        with st.expander(f"💻 Project #{idx+1}: {proj.get('title', 'Project')}", expanded=True):
            pr1, pr2 = st.columns([1.5, 1.5])
            with pr1:
                proj["title"] = st.text_input("Project Title *", value=proj.get("title", ""), key=f"proj_title_{idx}")
            with pr2:
                proj["technologies"] = st.text_input("Technologies Used *", value=proj.get("technologies", ""), key=f"proj_tech_{idx}")
                
            proj["description"] = st.text_area(
                "Project Description & Key Contributions:",
                value=proj.get("description", ""),
                height=80,
                key=f"proj_desc_{idx}"
            )
            
            if st.button(f"🗑️ Remove Project #{idx+1}", key=f"rm_proj_{idx}"):
                projects.pop(idx)
                st.rerun()

    if st.button("➕ Add Another Project"):
        projects.append({"title": "", "technologies": "", "description": ""})
        st.rerun()

    st.markdown("---")
    
    # Certifications
    st.markdown("### 📜 Certifications")
    certs = resume_data.setdefault("certifications", [])
    cert_text = "\n".join(certs) if certs else "Python Certified Associate Programmer (PCAP)\nDatabase Design & SQL Specialist Certificate"
    new_cert_text = st.text_area("Enter Certifications (one per line):", value=cert_text, height=70)
    resume_data["certifications"] = [c.strip() for c in new_cert_text.splitlines() if c.strip()]

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Navigation to Next Stage
    nav_col1, nav_col2 = st.columns([1, 2])
    with nav_col1:
        if st.button("Next: Enter Job Description ➡️", type="primary", use_container_width=True):
            st.session_state["nav_selection"] = "Analyze Resume"
            st.rerun()
