"""
Module 1: Home Page
Redesigned Page 1 matching the user's updated UI specification:
- Top application navbar with brand logo & user status
- Two-column hero section with headline, badge icon, CTA, and vector resume graphic
- 4 colorful action feature cards (Create Resume, Analyze Resume, Optimize Resume, My Resumes)
- Bottom reassurance feature bar (ATS Friendly, Fast & Easy, Better Opportunities, 100% Free)
"""

import os
import base64
import copy
import streamlit as st
from modules.sample_data import DEFAULT_RESUME


def get_image_base64(filepath: str) -> str:
    """Helper to convert local image to base64 data URI."""
    if os.path.exists(filepath):
        with open(filepath, "rb") as f:
            data = f.read()
            return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    return ""


def render_home_page():
    """Render the redesigned 1st page."""
    
    # Get logged-in user details
    user = st.session_state.get("user", {})
    user_name = user.get("full_name", "Guest")
    auth_prov = f"({user.get('auth_provider', 'local').title()})" if user.get("auth_provider") else ""
    
    # ==========================================================
    # 1. TOP NAVBAR
    # ==========================================================
    st.markdown(f"""
        <div class="top-nav-bar">
            <div class="top-nav-brand">
                <span style="font-size: 24px;">📄</span>
                <span>ATS Resumer</span>
            </div>
            <div class="top-nav-user">
                <span>👤 Welcome, <strong>{user_name}</strong> {auth_prov} ▾</span>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # ==========================================================
    # 2. HERO SECTION (2 COLUMNS)
    # ==========================================================
    hero_col_left, hero_col_right = st.columns([1.15, 0.95], gap="large")
    
    with hero_col_left:
        st.markdown("""
            <div style="padding-top: 10px;">
                <!-- Document Badge Icon -->
                <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 12px;">
                    <div style="width: 58px; height: 58px; border-radius: 14px; border: 3px solid #0066cc; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #ffffff;">
                        <div style="width: 16px; height: 16px; border-radius: 50%; background-color: #0066cc; margin-bottom: 3px;"></div>
                        <div style="width: 28px; height: 10px; border-radius: 5px; background-color: #0066cc;"></div>
                    </div>
                    <div>
                        <div class="hero-title-main">ATS <span class="hero-title-blue">Resumer</span></div>
                        <div class="hero-tagline">Build &nbsp;|&nbsp; Analyze &nbsp;|&nbsp; Optimize</div>
                    </div>
                </div>
                
                <p class="hero-subtext">
                    Create ATS-friendly resumes, analyze job descriptions and get personalized 
                    suggestions to improve your chances of getting hired.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        btn_c1, btn_c2 = st.columns([1.4, 1.4])
        with btn_c1:
            if st.button("Get Started  ➔", type="primary", use_container_width=True, key="hero_get_started"):
                st.session_state["nav_selection"] = "Create Resume"
                st.rerun()
        with btn_c2:
            if st.button("📋 Load Demo Profile", use_container_width=True, key="hero_load_demo"):
                st.session_state["resume_data"] = copy.deepcopy(DEFAULT_RESUME)
                st.session_state["target_role"] = "Python Developer"
                st.session_state["nav_selection"] = "Create Resume"
                st.success("Loaded demo profile for M. Katamaiah!")
                st.rerun()
                
    with hero_col_right:
        # Load and display the illustration
        ill_path = os.path.join(os.path.dirname(__file__), "..", "assets", "hero_illustration.png")
        ill_base64 = get_image_base64(ill_path)
        if ill_base64:
            st.markdown(f"""
                <div style="text-align: center; padding-top: 5px;">
                    <img src="{ill_base64}" style="max-width: 90%; height: auto; border-radius: 12px;" alt="ATS Resume Graphic" />
                </div>
            """, unsafe_allow_html=True)
        else:
            st.image(ill_path, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # 3. FOUR FEATURE ACTION CARDS (4 COLUMNS)
    # ==========================================================
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    
    # Card 1: Create Resume (Blue)
    with c1:
        st.markdown("""
            <div class="feature-card feature-card-blue">
                <div>
                    <div class="feature-icon-badge badge-blue">📄</div>
                    <div class="feature-card-title">Create Resume</div>
                    <div class="feature-card-desc">
                        Build a professional resume with your details, skills and experience.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Get Started  ➔", key="card_btn_create", use_container_width=True):
            st.session_state["nav_selection"] = "Create Resume"
            st.rerun()

    # Card 2: Analyze Resume (Green)
    with c2:
        st.markdown("""
            <div class="feature-card feature-card-green">
                <div>
                    <div class="feature-icon-badge badge-green">🔍</div>
                    <div class="feature-card-title">Analyze Resume</div>
                    <div class="feature-card-desc">
                        Compare your resume with job descriptions and find keyword matches.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Now  ➔", key="card_btn_analyze", use_container_width=True):
            st.session_state["nav_selection"] = "Analyze Resume"
            st.rerun()

    # Card 3: Optimize Resume (Purple)
    with c3:
        st.markdown("""
            <div class="feature-card feature-card-purple">
                <div>
                    <div class="feature-icon-badge badge-purple">⚙️</div>
                    <div class="feature-card-title">Optimize Resume</div>
                    <div class="feature-card-desc">
                        Get smart suggestions to improve your resume and increase your chances.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Optimize Now  ➔", key="card_btn_optimize", use_container_width=True):
            st.session_state["nav_selection"] = "Optimize Resume"
            st.rerun()

    # Card 4: My Resumes (Amber)
    with c4:
        st.markdown("""
            <div class="feature-card feature-card-amber">
                <div>
                    <div class="feature-icon-badge badge-amber">📁</div>
                    <div class="feature-card-title">My Resumes</div>
                    <div class="feature-card-desc">
                        View and manage your saved resumes anytime.
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("View Resumes  ➔", key="card_btn_my_resumes", use_container_width=True):
            st.session_state["nav_selection"] = "My Resumes"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ==========================================================
    # 4. BOTTOM REASSURANCE BANNER
    # ==========================================================
    st.markdown("""
        <div class="bottom-feature-bar">
            <div class="bottom-feature-item">
                <div class="bottom-feature-icon">🛡️</div>
                <div>
                    <div class="bottom-feature-title">ATS Friendly</div>
                    <div class="bottom-feature-sub">Designed to pass ATS scans</div>
                </div>
            </div>
            <div class="bottom-divider"></div>
            <div class="bottom-feature-item">
                <div class="bottom-feature-icon">⚡</div>
                <div>
                    <div class="bottom-feature-title">Fast & Easy</div>
                    <div class="bottom-feature-sub">Create in minutes</div>
                </div>
            </div>
            <div class="bottom-divider"></div>
            <div class="bottom-feature-item">
                <div class="bottom-feature-icon">🎯</div>
                <div>
                    <div class="bottom-feature-title">Better Opportunities</div>
                    <div class="bottom-feature-sub">Improve your chances</div>
                </div>
            </div>
            <div class="bottom-divider"></div>
            <div class="bottom-feature-item">
                <div class="bottom-feature-icon">😊</div>
                <div>
                    <div class="bottom-feature-title">100% Free</div>
                    <div class="bottom-feature-sub">No hidden charges</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
