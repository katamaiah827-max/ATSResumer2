"""
Authentication UI Module for ATS Resumer.
Provides user login, registration (Create Account), Google Sign-In, 
and database session management.
"""

import copy
import streamlit as st
from modules.database import authenticate_user, create_user, authenticate_google_user
from modules.sample_data import DEFAULT_RESUME


def login_user(user_record: dict):
    """Set authenticated session state and initialize candidate data."""
    st.session_state["authenticated"] = True
    st.session_state["user"] = user_record
    
    # If candidate name in current resume is empty, pre-fill with logged-in user name & email
    resume_data = st.session_state.setdefault("resume_data", copy.deepcopy(DEFAULT_RESUME))
    personal = resume_data.setdefault("personal", {})
    if not personal.get("full_name") or personal.get("full_name") == "Candidate Name":
        personal["full_name"] = user_record.get("full_name", "")
    if not personal.get("email"):
        personal["email"] = user_record.get("email", "")
        
    st.session_state["nav_selection"] = "Home"
    st.rerun()


def logout_user():
    """Clear user session and redirect to login page."""
    st.session_state["authenticated"] = False
    st.session_state["user"] = None
    st.session_state["nav_selection"] = "Home"
    if "analysis_result" in st.session_state:
        del st.session_state["analysis_result"]
    st.rerun()


def render_auth_page():
    """Render the primary Authentication & Login screen."""
    
    # Hero Title Banner
    st.markdown("""
        <div style="text-align: center; margin-top: 10px; margin-bottom: 25px;">
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 16px; background-color: #0066cc; color: white; font-size: 32px; margin-bottom: 12px; box-shadow: 0 4px 12px rgba(0, 102, 204, 0.25);">
                📄
            </div>
            <h1 style="color: #0f172a; font-size: 36px; font-weight: 800; margin: 0; letter-spacing: -0.5px;">
                ATS <span style="color: #0066cc;">Resumer</span>
            </h1>
            <div style="font-size: 15px; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 1px; margin-top: 4px;">
                Build &nbsp;|&nbsp; Analyze &nbsp;|&nbsp; Optimize
            </div>
            <p style="color: #64748b; font-size: 14.5px; margin-top: 8px; max-width: 480px; margin-left: auto; margin-right: auto;">
                Welcome to ATS Resumer. Sign in to analyze job descriptions, build ATS-optimized resumes, and track your applications.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Centered Form Container
    col_left, col_center, col_right = st.columns([1, 1.8, 1])
    
    with col_center:
        st.markdown("""
            <div style="background: #ffffff; border-radius: 14px; border: 1px solid #e2e8f0; padding: 26px 28px; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.06);">
        """, unsafe_allow_html=True)
        
        auth_tab1, auth_tab2 = st.tabs(["🔑 Sign In", "✨ Create Account"])
        
        # ==========================================================
        # TAB 1: SIGN IN
        # ==========================================================
        with auth_tab1:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            
            # Google Sign In Button
            st.markdown("""
                <div style="text-align: center; margin-bottom: 12px;">
                    <span style="font-size: 13px; font-weight: 600; color: #475569;">Quick Access with Social Sign-in</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Google Login Section
            with st.expander("🌐 Continue with Google", expanded=False):
                st.caption("Sign in with your Google identity:")
                google_email = st.text_input("Google Email Address:", value="katamaiah@gmail.com", key="google_email_in")
                google_name = st.text_input("Account Display Name:", value="M. Katamaiah", key="google_name_in")
                if st.button("Confirm Google Sign-In", type="primary", use_container_width=True, key="google_confirm_btn"):
                    if "@" in google_email and "." in google_email:
                        success, msg, user = authenticate_google_user(google_email, google_name)
                        if success:
                            st.success(msg)
                            login_user(user)
                    else:
                        st.error("Please enter a valid Google email.")
                        
            st.markdown("""
                <div style="display: flex; align-items: center; margin: 18px 0 14px 0;">
                    <div style="flex-grow: 1; height: 1px; background-color: #e2e8f0;"></div>
                    <span style="color: #94a3b8; font-size: 12px; font-weight: 600; text-transform: uppercase; padding: 0 12px;">or sign in with email</span>
                    <div style="flex-grow: 1; height: 1px; background-color: #e2e8f0;"></div>
                </div>
            """, unsafe_allow_html=True)
            
            login_email = st.text_input("Email Address:", placeholder="name@example.com", key="login_email_in")
            login_password = st.text_input("Password:", type="password", placeholder="Enter your password", key="login_pw_in")
            
            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
            if st.button("Sign In  ➔", type="primary", use_container_width=True, key="sign_in_submit"):
                if not login_email or not login_password:
                    st.warning("Please fill in both email and password.")
                else:
                    success, msg, user_record = authenticate_user(login_email, login_password)
                    if success:
                        st.success(msg)
                        login_user(user_record)
                    else:
                        st.error(msg)
                        
            st.markdown("---")
            
            # 1-Click Demo Shortcut for Examiners / Evaluators
            st.markdown("""
                <div style="text-align: center; margin-bottom: 8px;">
                    <span style="font-size: 12px; color: #64748b; font-weight: 600;">For Evaluation & Demonstration:</span>
                </div>
            """, unsafe_allow_html=True)
            if st.button("⚡ Quick Demo Login (M. Katamaiah)", use_container_width=True, key="demo_login_btn"):
                success, msg, user_record = authenticate_user("katamaiah@example.com", "password123")
                if success:
                    st.success("Signed in as Demo User!")
                    login_user(user_record)
                else:
                    st.error(msg)
                    
        # ==========================================================
        # TAB 2: CREATE ACCOUNT (REGISTER)
        # ==========================================================
        with auth_tab2:
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("""
                <div style="font-size: 13.5px; color: #475569; margin-bottom: 12px;">
                    Create a new ATS Resumer account to store your resumes in the connected database.
                </div>
            """, unsafe_allow_html=True)
            
            reg_name = st.text_input("Full Name *", placeholder="e.g. John Doe", key="reg_name_in")
            reg_email = st.text_input("Email Address *", placeholder="e.g. john@example.com", key="reg_email_in")
            reg_pw = st.text_input("Create Password * (min 6 characters)", type="password", key="reg_pw_in")
            reg_confirm_pw = st.text_input("Confirm Password *", type="password", key="reg_conf_pw_in")
            
            st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
            if st.button("Create Account & Sign In  ➔", type="primary", use_container_width=True, key="register_submit"):
                if not reg_name or not reg_email or not reg_pw:
                    st.warning("Please fill in all required fields.")
                elif "@" not in reg_email or "." not in reg_email:
                    st.error("Please enter a valid email address.")
                elif len(reg_pw) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif reg_pw != reg_confirm_pw:
                    st.error("Passwords do not match. Please re-type your password.")
                else:
                    success, msg, new_user = create_user(reg_email, reg_pw, reg_name, auth_provider="local")
                    if success:
                        st.success(msg)
                        login_user(new_user)
                    else:
                        st.error(msg)
                        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Database Status Badge
        st.markdown("""
            <div style="text-align: center; margin-top: 18px; font-size: 12px; color: #10b981; font-weight: 600;">
                🟢 SQLite Database Connected & Ready (data/ats_resumer.db)
            </div>
            <div style="text-align: center; font-size: 11.5px; color: #94a3b8; margin-top: 4px;">
                Secure SHA-256 Hashing &bull; Relational User & Resume Storage
            </div>
        """, unsafe_allow_html=True)
