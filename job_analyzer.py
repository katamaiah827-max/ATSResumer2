"""
Module 3 & 4: Job Description Input & Resume Analysis (Stages 4 & 5)
Allows pasting any job description, selecting target roles, and running 
the ATS matching engine to compute scores, matched skills, missing keywords, and suggestions.
"""

import streamlit as st
from modules.sample_data import SAMPLE_JOB_DESCRIPTIONS
from modules.utils import calculate_ats_match


def render_job_analyzer():
    """Render the Job Description Input & ATS Analysis Results view."""
    
    st.markdown("## 🔍 Job Description & Resume Analysis")
    
    # Workflow Stage Progress Bar
    st.markdown("""
        <div class="step-container">
            <div class="step-item completed"><div class="step-circle">✓</div>1. Launch</div>
            <div class="step-item completed"><div class="step-circle">✓</div>2. Details</div>
            <div class="step-item completed"><div class="step-circle">✓</div>3. Skills</div>
            <div class="step-item active"><div class="step-circle">4</div>4. Job Desc</div>
            <div class="step-item active"><div class="step-circle">5</div>5. Analysis</div>
            <div class="step-item"><div class="step-circle">6</div>6. Optimize</div>
        </div>
    """, unsafe_allow_html=True)
    
    # ==========================================================
    # STAGE 4: ENTER JOB DESCRIPTION
    # ==========================================================
    st.markdown("### 📋 Stage 4: Enter Job Description")
    st.markdown("Paste the target job description or choose from standard industry roles to benchmark your resume.")
    
    c1, c2 = st.columns([1.5, 1])
    roles_list = list(SAMPLE_JOB_DESCRIPTIONS.keys()) + ["Full Stack Developer", "Cloud / DevOps Engineer", "Other Position"]
    
    with c1:
        current_target = st.session_state.get("target_role", "Python Developer")
        default_idx = roles_list.index(current_target) if current_target in roles_list else 0
        selected_role = st.selectbox("Select Target Job Role:", roles_list, index=default_idx)
        st.session_state["target_role"] = selected_role
        
    with c2:
        st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Load Sample Job Description for " + selected_role):
            if selected_role in SAMPLE_JOB_DESCRIPTIONS:
                st.session_state["job_description"] = SAMPLE_JOB_DESCRIPTIONS[selected_role]
                st.rerun()
            else:
                st.session_state["job_description"] = SAMPLE_JOB_DESCRIPTIONS["Python Developer"]
                st.rerun()

    jd_text = st.text_area(
        "Paste the job description below:",
        value=st.session_state.get("job_description", SAMPLE_JOB_DESCRIPTIONS.get("Python Developer", "")),
        height=140,
        placeholder="Paste complete job description, requirements, and responsibilities here..."
    )
    st.session_state["job_description"] = jd_text

    col_btn1, col_btn2 = st.columns([1, 3])
    with col_btn1:
        run_analysis = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)
        
    if run_analysis or "analysis_result" in st.session_state:
        if run_analysis:
            resume_data = st.session_state.get("resume_data", {})
            with st.spinner("Analyzing keyword density, taxonomy matching, and ATS compatibility..."):
                analysis = calculate_ats_match(resume_data, jd_text, selected_role)
                st.session_state["analysis_result"] = analysis
                
        analysis = st.session_state.get("analysis_result")
        if not analysis:
            return
            
        st.markdown("---")
        
        # ==========================================================
        # STAGE 5: RESUME ANALYSIS RESULTS
        # ==========================================================
        st.markdown("### 📊 Stage 5: Resume Analysis Results")
        
        score = analysis["score"]
        matched_skills = analysis["matched_skills"]
        missing_skills = analysis["missing_skills"]
        suggestions = analysis["suggestions"]
        
        # Score banner and Metric Cards
        m1, m2, m3, m4 = st.columns([1.2, 1, 1, 1])
        
        # Donut-like Circular Score Indicator
        with m1:
            score_color = "#10b981" if score >= 75 else ("#f59e0b" if score >= 50 else "#ef4444")
            st.markdown(f"""
                <div class="score-card" style="border-top: 4px solid {score_color};">
                    <div style="font-size: 42px; font-weight: 800; color: {score_color}; line-height: 1.1;">
                        {score}%
                    </div>
                    <div style="font-size: 13px; font-weight: 700; color: #475569; text-transform: uppercase; margin-top: 6px;">
                        ATS Match Score
                    </div>
                    <div style="font-size: 11px; color: #64748b; margin-top: 4px;">
                        {'Excellent match' if score >= 75 else ('Good potential' if score >= 50 else 'Needs keyword enrichment')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        with m2:
            st.metric("Total JD Skills", analysis["total_jd_keywords"])
        with m3:
            st.metric("Matched Keywords", len(matched_skills), delta=f"+{len(matched_skills)} matched")
        with m4:
            st.metric("Missing Keywords", len(missing_skills), delta=f"-{len(missing_skills)} missing", delta_color="inverse")

        st.progress(score / 100.0)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Matched Skills vs Missing Skills Cards
        c_match, c_miss = st.columns(2)
        with c_match:
            st.markdown("""
                <div class="ats-card">
                    <div class="ats-card-header" style="color: #15803d; border-color: #bbf7d0;">
                        ✅ Key Matched Skills ({})
                    </div>
            """.format(len(matched_skills)), unsafe_allow_html=True)
            
            if matched_skills:
                m_html = "<div>"
                for sk in matched_skills:
                    m_html += f'<span class="skill-tag-matched">✔ {sk}</span>'
                m_html += "</div>"
                st.markdown(m_html, unsafe_allow_html=True)
            else:
                st.warning("No direct keyword matches found. Review the job description keywords.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        with c_miss:
            st.markdown("""
                <div class="ats-card">
                    <div class="ats-card-header" style="color: #b45309; border-color: #fde68a;">
                        ⚠️ Missing Keywords ({})
                    </div>
            """.format(len(missing_skills)), unsafe_allow_html=True)
            
            if missing_skills:
                miss_html = "<div>"
                for sk in missing_skills:
                    miss_html += f'<span class="skill-tag-missing">✚ {sk}</span>'
                miss_html += "</div>"
                st.markdown(miss_html, unsafe_allow_html=True)
            else:
                st.success("Outstanding! All primary keywords found in resume.")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Actionable Suggestions
        st.markdown("""
            <div class="ats-card">
                <div class="ats-card-header">💡 Recommendations to Improve ATS Ranking</div>
        """, unsafe_allow_html=True)
        
        for sug in suggestions:
            st.markdown(f"- {sug}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Next Stage Action Button
        st.markdown("<br>", unsafe_allow_html=True)
        s_col1, s_col2 = st.columns([1.2, 2])
        with s_col1:
            if st.button("Optimize Your Resume Now ➡️", type="primary", use_container_width=True):
                st.session_state["nav_selection"] = "Optimize Resume"
                st.rerun()
