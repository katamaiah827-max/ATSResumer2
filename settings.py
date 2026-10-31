"""
Settings and Configurations Module.
Allows managing application preferences, ATS scoring sensitivity, and taxonomy inspection.
"""

import streamlit as st
from modules.utils import TECH_KEYWORDS


def render_settings():
    """Render the application configuration and settings page."""
    st.markdown("## ⚙️ Application Settings & Preferences")
    
    st.markdown("""
        <div class="ats-card">
            <div class="ats-card-header">🛠️ ATS Scanner Configuration</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.selectbox(
            "ATS Scoring Engine Sensitivity:",
            ["Standard (Recommended - 50% Hard Skills, 25% Experience, 25% Format)", 
             "Strict (Exact Match Only)", 
             "Comprehensive (Includes Fuzzy Match)"],
            index=0
        )
        st.selectbox("Default PDF Page Size:", ["US Letter (8.5 x 11 in)", "A4 (210 x 297 mm)"], index=0)
        
    with col2:
        st.checkbox("Enable Automated Keyword Synonyms Matching", value=True)
        st.checkbox("Strict Single-Column ATS Formatting Enforcement", value=True)
        st.checkbox("Show Detailed Section Weightings in Analysis", value=True)
        
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Keyword Taxonomy Explorer
    with st.expander("📚 Explore Built-in Skill & Keyword Taxonomy", expanded=False):
        st.write(f"The built-in ATS dictionary indexes **{len(TECH_KEYWORDS)}** industry-standard competencies:")
        unique_canonical = sorted(list(set(TECH_KEYWORDS.values())))
        st.write(", ".join(unique_canonical))
        
    # College Mini-Project About Box
    st.markdown("""
        <div class="ats-card">
            <div class="ats-card-header">🎓 About ATS Resumer Mini-Project</div>
            <p style="font-size: 14px; color: #475569; line-height: 1.6;">
                <strong>Project Title:</strong> ATS Resumer – Resume Builder and Optimizer<br>
                <strong>Domain:</strong> Natural Language Processing, Web Application & Information Retrieval<br>
                <strong>Architecture:</strong> Streamlit Multi-Stage Architecture with ReportLab PDF Rendering Engine<br>
                <strong>Purpose:</strong> Developed for academic demonstration to assist candidates in passing Applicant Tracking Systems.
            </p>
        </div>
    """, unsafe_allow_html=True)
