"""
Module 5: Resume Optimization (Stage 6)
Provides targeted optimization suggestions, automated professional summary enhancement,
interactive missing-skill addition (only for skills the candidate actually knows),
and ATS single-column formatting guarantees.
"""

import streamlit as st
from modules.utils import generate_optimized_summary, calculate_ats_match


def render_resume_optimizer():
    """Render the Resume Optimizer interface matching Stage 6."""
    
    st.markdown("## ⚡ Stage 6: Optimize Your Resume")
    st.markdown("Follow the ATS optimization recommendations below to boost your keyword match and readability.")
    
    # Workflow Stage Progress Bar
    st.markdown("""
        <div class="step-container">
            <div class="step-item completed"><div class="step-circle">✓</div>1. Launch</div>
            <div class="step-item completed"><div class="step-circle">✓</div>2. Details</div>
            <div class="step-item completed"><div class="step-circle">✓</div>3. Skills</div>
            <div class="step-item completed"><div class="step-circle">✓</div>4. Job Desc</div>
            <div class="step-item completed"><div class="step-circle">✓</div>5. Analysis</div>
            <div class="step-item active"><div class="step-circle">6</div>6. Optimize</div>
            <div class="step-item"><div class="step-circle">7</div>7. Final PDF</div>
        </div>
    """, unsafe_allow_html=True)
    
    resume_data = st.session_state.get("resume_data", {})
    analysis = st.session_state.get("analysis_result", {})
    target_role = st.session_state.get("target_role", "Python Developer")
    
    # 1. Optimization Suggestions Card (Matching Stage 6 mockup)
    st.markdown("""
        <div class="ats-card">
            <div class="ats-card-header">🎯 Optimization Suggestions</div>
            <div class="checklist-item">
                <span class="checklist-icon">✔</span>
                <div>
                    <strong>Add relevant keywords from the job description:</strong><br>
                    <span style="font-size: 13px; color: #64748b;">
                        Align your listed technical competencies with the target role requirements.
                    </span>
                </div>
            </div>
            <div class="checklist-item">
                <span class="checklist-icon">✔</span>
                <div>
                    <strong>Improve your resume summary:</strong><br>
                    <span style="font-size: 13px; color: #64748b;">
                        Tailor your opening statement with role-specific keywords and proven accomplishments.
                    </span>
                </div>
            </div>
            <div class="checklist-item">
                <span class="checklist-icon">✔</span>
                <div>
                    <strong>Highlight your technical skills:</strong><br>
                    <span style="font-size: 13px; color: #64748b;">
                        Place core languages, frameworks, and databases in a distinct ATS-parseable skills block.
                    </span>
                </div>
            </div>
            <div class="checklist-item">
                <span class="checklist-icon">✔</span>
                <div>
                    <strong>Use an ATS-friendly format (simple, clean layout):</strong><br>
                    <span style="font-size: 13px; color: #64748b;">
                        Avoid multi-column tables, photos, floating text boxes, and non-standard symbols.
                    </span>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 2. Interactive Skill Integration Assistant
    missing_skills = analysis.get("missing_skills", [])
    st.markdown("### 🧩 Add Missing Skills You Genuinely Possess")
    st.markdown(
        "*Note: Only select skills you have actual experience with. "
        "ATS Resumer upholds ethical integrity and never invents unverified qualifications.*"
    )
    
    selected_skills_to_add = []
    if missing_skills:
        st.write("Check the skills below that you know and would like to incorporate into your resume:")
        cols = st.columns(3)
        for i, skill in enumerate(missing_skills):
            col_idx = i % 3
            with cols[col_idx]:
                if st.checkbox(f"Add **{skill}**", key=f"opt_skill_{skill}"):
                    selected_skills_to_add.append(skill)
    else:
        st.info("No missing skills detected! Your resume already encompasses all key keywords from the job description.")
        
    st.markdown("---")
    
    # 3. Optimized Professional Summary Generator
    st.markdown("### 📝 AI-Assisted Professional Summary Enhancer")
    st.markdown(f"Generate a tailored summary aligned with the **{target_role}** requirements:")
    
    matched_skills = analysis.get("matched_skills", [])
    combined_skills = list(set(matched_skills + selected_skills_to_add))
    suggested_summary = generate_optimized_summary(resume_data, target_role, combined_skills)
    
    col_sum1, col_sum2 = st.columns([3, 1])
    with col_sum1:
        custom_summary = st.text_area(
            "Review and customize the improved summary:",
            value=suggested_summary,
            height=120,
            key="optimized_summary_text"
        )
    with col_sum2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        st.caption("This summary emphasizes your core competencies and passes ATS semantic screening.")
        
    st.markdown("---")
    
    # 4. Apply Suggestions Button
    btn_col1, btn_col2 = st.columns([1.5, 2])
    with btn_col1:
        if st.button("✨ Apply Suggestions & Update Resume", type="primary", use_container_width=True):
            # 1. Update summary
            resume_data["summary"] = custom_summary
            
            # 2. Add selected missing skills
            tech_skills = resume_data.setdefault("technical_skills", [])
            for sk in selected_skills_to_add:
                if sk not in tech_skills:
                    tech_skills.append(sk)
                    
            # 3. Recalculate ATS score
            jd_text = st.session_state.get("job_description", "")
            new_analysis = calculate_ats_match(resume_data, jd_text, target_role)
            st.session_state["analysis_result"] = new_analysis
            st.session_state["resume_data"] = resume_data
            
            st.success(f"Optimized resume! New ATS match score: {new_analysis['score']}%")
            st.session_state["nav_selection"] = "My Resumes"
            st.rerun()
            
    with btn_col2:
        if st.button("Skip Optimization & View Final Resume ➡️", use_container_width=True):
            st.session_state["nav_selection"] = "My Resumes"
            st.rerun()
