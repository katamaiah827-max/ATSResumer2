"""
Module 6, 7, 8 & 9: Final Resume Preview, PDF Download, and Database Resume Management
Handles Stages 7, 8, and 9 of the ATS Resumer workflow.
Renders high-fidelity ATS resume preview, provides ReportLab PDF download, 
displays the success celebration screen, and manages the database-backed resume repository.
"""

import json
import time
import streamlit as st
from modules.pdf_generator import generate_ats_resume_pdf
from modules.database import save_user_resume, get_user_resumes, delete_user_resume


def render_my_resumes():
    """Render the Final Resume Review, PDF Download, and Database Resumes Library."""
    
    st.markdown("## 📄 Your Optimized Resume & Downloads")
    
    # Workflow Stage Progress Bar
    st.markdown("""
        <div class="step-container">
            <div class="step-item completed"><div class="step-circle">✓</div>1. Launch</div>
            <div class="step-item completed"><div class="step-circle">✓</div>2. Details</div>
            <div class="step-item completed"><div class="step-circle">✓</div>3. Skills</div>
            <div class="step-item completed"><div class="step-circle">✓</div>4. Job Desc</div>
            <div class="step-item completed"><div class="step-circle">✓</div>5. Analysis</div>
            <div class="step-item completed"><div class="step-circle">✓</div>6. Optimize</div>
            <div class="step-item active"><div class="step-circle">7</div>7. Generate</div>
            <div class="step-item active"><div class="step-circle">8</div>8. Download PDF</div>
            <div class="step-item active"><div class="step-circle">9</div>9. Ready!</div>
        </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📑 Review & Download Resume", "🎉 Completion Status", "📁 My Database Resumes"])
    
    resume_data = st.session_state.get("resume_data", {})
    personal = resume_data.get("personal", {})
    candidate_name = personal.get("full_name", "Candidate")
    target_role = personal.get("target_role", "Developer")
    user = st.session_state.get("user", {})
    user_id = user.get("id", 1)
    
    # ==========================================================
    # TAB 1: STAGE 7 & 8 - PREVIEW & DOWNLOAD AS PDF
    # ==========================================================
    with tab1:
        # Action Buttons Header
        top_col1, top_col2, top_col3 = st.columns([2, 1, 1])
        with top_col1:
            st.markdown(f"### Stage 7 & 8: Resume Review for **{candidate_name}**")
            
        with top_col2:
            # Generate ReportLab PDF on-the-fly
            try:
                pdf_bytes = generate_ats_resume_pdf(resume_data)
                safe_name = "".join([c if c.isalnum() else "_" for c in candidate_name]).strip("_")
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name=f"{safe_name}_ATS_Resume.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
                
        with top_col3:
            if st.button("💾 Save to Database", use_container_width=True):
                score = st.session_state.get("analysis_result", {}).get("score", 82)
                res_id = save_user_resume(user_id, candidate_name, target_role, score, resume_data)
                st.success(f"Saved resume #{res_id} securely to your database account!")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # High-Fidelity Resume Document Card (Matching Stage 7 Layout)
        st.markdown('<div class="resume-paper">', unsafe_allow_html=True)
        
        # Header: Name, Target Role, Contact Row
        st.markdown(f'<div class="resume-name">{candidate_name}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="resume-title">{target_role}</div>', unsafe_allow_html=True)
        
        contact_items = []
        if personal.get("email"):
            contact_items.append(f"✉️ {personal.get('email')}")
        if personal.get("phone"):
            contact_items.append(f"📞 {personal.get('phone')}")
        if personal.get("location"):
            contact_items.append(f"📍 {personal.get('location')}")
        if personal.get("linkedin"):
            contact_items.append(f"🔗 {personal.get('linkedin')}")
            
        st.markdown(f'<div class="resume-contact">{" &nbsp;&nbsp;|&nbsp;&nbsp; ".join(contact_items)}</div>', unsafe_allow_html=True)
        
        # Summary
        summary = resume_data.get("summary", "")
        if summary:
            st.markdown('<div class="resume-section-title">Professional Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 13.5px; color: #1e293b; line-height: 1.6;">{summary}</p>', unsafe_allow_html=True)
            
        # Skills
        tech_skills = resume_data.get("technical_skills", [])
        if tech_skills:
            st.markdown('<div class="resume-section-title">Technical Skills</div>', unsafe_allow_html=True)
            skills_html = "<div>"
            for sk in tech_skills:
                skills_html += f'<span class="skill-tag">{sk}</span>'
            skills_html += "</div>"
            st.markdown(skills_html, unsafe_allow_html=True)
            
        # Work Experience
        exps = resume_data.get("experience", [])
        if exps:
            st.markdown('<div class="resume-section-title">Work Experience</div>', unsafe_allow_html=True)
            for exp in exps:
                c_name = exp.get("company", "")
                desig = exp.get("designation", "")
                dur = exp.get("duration", "")
                loc = exp.get("location", "")
                
                exp_header = f"<strong>{desig}</strong> &mdash; <em>{c_name}</em>"
                exp_meta = f"{dur} | {loc}"
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; margin-top: 6px; font-size: 13.5px;">
                        <div>{exp_header}</div>
                        <div style="color: #64748b; font-size: 12.5px;">{exp_meta}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                bullets = exp.get("responsibilities", "").splitlines()
                for b in bullets:
                    if b.strip():
                        clean_b = b.lstrip("-•* ").strip()
                        st.markdown(f"<li style='font-size: 13px; color: #334155; margin-left: 18px;'>{clean_b}</li>", unsafe_allow_html=True)
                        
        # Projects
        projs = resume_data.get("projects", [])
        if projs:
            st.markdown('<div class="resume-section-title">Projects</div>', unsafe_allow_html=True)
            for proj in projs:
                p_title = proj.get("title", "")
                p_tech = proj.get("technologies", "")
                p_desc = proj.get("description", "")
                
                tech_span = f" <span style='color: #64748b; font-size: 12px;'>({p_tech})</span>" if p_tech else ""
                st.markdown(f"<div style='font-weight: 700; font-size: 13.5px; margin-top: 6px;'>{p_title}{tech_span}</div>", unsafe_allow_html=True)
                for line in p_desc.splitlines():
                    if line.strip():
                        clean_line = line.lstrip("-•* ").strip()
                        st.markdown(f"<li style='font-size: 13px; color: #334155; margin-left: 18px;'>{clean_line}</li>", unsafe_allow_html=True)
                        
        # Education
        edus = resume_data.get("education", [])
        if edus:
            st.markdown('<div class="resume-section-title">Education</div>', unsafe_allow_html=True)
            for edu in edus:
                deg = edu.get("degree", "")
                field = edu.get("field", "")
                uni = edu.get("university", "")
                yr = edu.get("passing_year", "")
                gr = edu.get("grade", "")
                
                st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; margin-top: 6px; font-size: 13.5px;">
                        <div><strong>{deg}</strong> {f'in {field}' if field else ''} &mdash; <span style="color: #475569;">{uni}</span></div>
                        <div style="color: #64748b; font-size: 12.5px;">{yr} {f'| {gr}' if gr else ''}</div>
                    </div>
                """, unsafe_allow_html=True)
                
        st.markdown('</div>', unsafe_allow_html=True)

    # ==========================================================
    # TAB 2: STAGE 9 - COMPLETION STATUS SCREEN
    # ==========================================================
    with tab2:
        st.markdown("""
            <div style="text-align: center; padding: 40px 20px; background-color: #ffffff; border-radius: 12px; border: 1px solid #e2e8f0;">
                <div style="font-size: 64px; color: #10b981; margin-bottom: 12px;">✅</div>
                <h1 style="color: #0f172a; margin-bottom: 8px;">Your Resume is Ready!</h1>
                <p style="font-size: 17px; color: #475569; max-width: 560px; margin: 0 auto 24px auto;">
                    You have successfully created and optimized your resume for ATS screening. 
                    It is formatted for 100% parseability across modern corporate ATS platforms.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        c_act1, c_act2 = st.columns([1, 1])
        with c_act1:
            if st.button("➕ Start New Resume", use_container_width=True, type="primary"):
                st.session_state["nav_selection"] = "Create Resume"
                st.rerun()
        with c_act2:
            try:
                pdf_bytes = generate_ats_resume_pdf(resume_data)
                st.download_button(
                    label="📥 Download ATS PDF",
                    data=pdf_bytes,
                    file_name=f"{candidate_name.replace(' ', '_')}_Resume.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
            except Exception:
                pass

    # ==========================================================
    # TAB 3: DATABASE RESUME LIBRARY (SAVED IN SQLITE)
    # ==========================================================
    with tab3:
        st.markdown(f"### 🗄️ Resumes Saved in Database for **{user.get('full_name', 'You')}**")
        db_resumes = get_user_resumes(user_id)
        
        if not db_resumes:
            st.info("No saved resumes in your database account yet. Click **Save to Database** in the Review tab to store your resumes permanently.")
        else:
            for r in db_resumes:
                r_id = r["id"]
                with st.expander(f"📄 #{r_id}: {r['name']} — {r['role']} (Saved: {r['date']} | Score: {r['score']}%)", expanded=True):
                    sc1, sc2, sc3 = st.columns([1, 1, 1])
                    with sc1:
                        if st.button("🔄 Load into Editor", key=f"load_db_res_{r_id}"):
                            st.session_state["resume_data"] = r["data"]
                            st.session_state["target_role"] = r["role"]
                            st.success(f"Loaded resume #{r_id} into editor!")
                            st.rerun()
                    with sc2:
                        pdf_data = generate_ats_resume_pdf(r["data"])
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_data,
                            file_name=f"{r['name'].replace(' ', '_')}_Resume.pdf",
                            mime="application/pdf",
                            key=f"dl_db_res_{r_id}"
                        )
                    with sc3:
                        if st.button("🗑️ Delete from Database", key=f"del_db_res_{r_id}"):
                            delete_user_resume(r_id, user_id)
                            st.success(f"Deleted resume #{r_id} from database.")
                            st.rerun()
                            
        st.markdown("---")
        # JSON Backup & Restore
        st.markdown("#### 💾 Backup & Export / Import")
        exp_col1, exp_col2 = st.columns(2)
        with exp_col1:
            json_str = json.dumps(resume_data, indent=2)
            st.download_button(
                label="📤 Export Active Resume as JSON",
                data=json_str,
                file_name="resume_backup.json",
                mime="application/json",
                use_container_width=True
            )
        with exp_col2:
            import_file = st.file_uploader("📥 Import Resume from JSON:", type=["json"], key="json_import")
            if import_file is not None:
                if st.button("Load Imported JSON"):
                    try:
                        imported_data = json.load(import_file)
                        st.session_state["resume_data"] = imported_data
                        st.success("Resume loaded successfully from JSON!")
                        st.rerun()
                    except Exception as ex:
                        st.error(f"Error parsing JSON: {ex}")
