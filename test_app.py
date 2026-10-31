"""
Automated Test Suite for ATS Resumer Mini-Project.
Validates module imports, SQLite database, user authentication (Password & Google),
ATS scoring engine, PDF generation, and text parsing.
"""

import sys
import os

# Add root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_imports():
    print("[1/8] Testing module imports...")
    import streamlit
    import reportlab
    import pandas
    import pypdf
    from modules.sample_data import DEFAULT_RESUME, SAMPLE_JOB_DESCRIPTIONS
    from modules.database import init_db, create_user, authenticate_user, authenticate_google_user
    from modules.utils import calculate_ats_match, extract_keywords_from_text, generate_optimized_summary
    from modules.pdf_generator import generate_ats_resume_pdf
    from modules.resume_parser import extract_text_from_pdf, parse_resume_content
    print("  -> All modules and third-party dependencies imported successfully.")


def test_database_and_auth():
    print("[2/8] Testing SQLite database initialization and authentication...")
    from modules.database import (
        init_db, create_user, authenticate_user, authenticate_google_user,
        save_user_resume, get_user_resumes, delete_user_resume, DB_PATH
    )
    init_db()
    assert os.path.exists(DB_PATH), f"Database file not created at {DB_PATH}"
    
    # Test 1: Pre-seeded demo user
    success, msg, user = authenticate_user("katamaiah@example.com", "password123")
    assert success, f"Demo login failed: {msg}"
    assert user["full_name"] == "M. Katamaiah"
    
    # Test 2: Invalid password check
    fail_success, fail_msg, _ = authenticate_user("katamaiah@example.com", "wrongpassword")
    assert not fail_success, "Expected login failure for wrong password"
    
    # Test 3: Create a new account
    test_email = "tester_demo@example.com"
    reg_success, reg_msg, new_user = create_user(test_email, "securepass123", "Demo Tester")
    assert reg_success or "already exists" in reg_msg, f"User registration failed: {reg_msg}"
    
    # Test 4: Google Authentication
    g_success, g_msg, g_user = authenticate_google_user("google_user@gmail.com", "Google Candidate")
    assert g_success, f"Google authentication failed: {g_msg}"
    assert g_user["auth_provider"] == "google"
    print(f"  -> SQLite Database verified at {DB_PATH}")
    print("  -> Local email/password authentication & Google Sign-In passed.")


def test_resume_database_persistence():
    print("[3/8] Testing Resume database persistence per user...")
    from modules.database import save_user_resume, get_user_resumes, delete_user_resume
    from modules.sample_data import DEFAULT_RESUME
    
    user_id = 1
    res_id = save_user_resume(user_id, "M. Katamaiah", "Python Developer", 82, DEFAULT_RESUME)
    assert res_id > 0, "Failed to insert resume into database"
    
    resumes = get_user_resumes(user_id)
    assert len(resumes) > 0, "No resumes returned from database"
    assert resumes[0]["name"] == "M. Katamaiah"
    
    # Test resume deletion
    del_ok = delete_user_resume(res_id, user_id)
    assert del_ok, "Failed to delete test resume"
    print("  -> Resume insertion, query, and deletion in SQLite passed.")


def test_sample_data():
    print("[4/8] Validating sample data...")
    from modules.sample_data import DEFAULT_RESUME, SAMPLE_JOB_DESCRIPTIONS
    assert DEFAULT_RESUME["personal"]["full_name"] == "M. Katamaiah"
    assert DEFAULT_RESUME["personal"]["target_role"] == "Python Developer"
    assert len(DEFAULT_RESUME["technical_skills"]) >= 5
    assert len(SAMPLE_JOB_DESCRIPTIONS) >= 5
    print("  -> Sample candidate data and 5 role descriptions validated.")


def test_keyword_extraction():
    print("[5/8] Testing keyword extraction...")
    from modules.utils import extract_keywords_from_text
    sample_text = "Looking for a Python Developer with Django, Flask, SQL, REST APIs, and Docker experience."
    keywords = extract_keywords_from_text(sample_text)
    expected = ["Docker", "Django", "Flask", "Python", "REST APIs", "SQL"]
    for exp in expected:
        assert exp in keywords, f"Expected keyword '{exp}' was not extracted"
    print(f"  -> Successfully extracted {len(keywords)} keywords: {keywords}")


def test_ats_match_scoring():
    print("[6/8] Testing ATS score calculation against benchmark...")
    from modules.sample_data import DEFAULT_RESUME, SAMPLE_JOB_DESCRIPTIONS
    from modules.utils import calculate_ats_match
    jd = SAMPLE_JOB_DESCRIPTIONS["Python Developer"]
    result = calculate_ats_match(DEFAULT_RESUME, jd, "Python Developer")
    assert result["score"] >= 70, f"Expected ATS score >= 70, got {result['score']}"
    assert len(result["matched_skills"]) > 0
    assert len(result["missing_skills"]) > 0
    print(f"  -> ATS Match Score: {result['score']}%")
    print(f"  -> Matched Skills ({len(result['matched_skills'])}): {result['matched_skills']}")
    print(f"  -> Missing Keywords ({len(result['missing_skills'])}): {result['missing_skills']}")


def test_pdf_generation_and_parsing():
    print("[7/8] Testing ReportLab PDF generation and round-trip parsing...")
    from modules.sample_data import DEFAULT_RESUME
    from modules.pdf_generator import generate_ats_resume_pdf
    from modules.resume_parser import extract_text_from_pdf
    
    pdf_bytes = generate_ats_resume_pdf(DEFAULT_RESUME)
    assert len(pdf_bytes) > 1000, "Generated PDF is too small or empty"
    print(f"  -> ReportLab PDF generated: {len(pdf_bytes)} bytes.")
    
    extracted_text = extract_text_from_pdf(pdf_bytes)
    assert "M. Katamaiah" in extracted_text, "Candidate name missing from parsed PDF"
    assert "Python Developer" in extracted_text, "Target role missing from parsed PDF"
    assert "JNTU Hyderabad" in extracted_text, "University name missing from parsed PDF"
    print("  -> PDF parse round-trip verified successfully (Candidate name, role, and university found).")


def test_summary_optimization():
    print("[8/8] Testing AI/Rule-based summary optimization...")
    from modules.sample_data import DEFAULT_RESUME
    from modules.utils import generate_optimized_summary
    opt_sum = generate_optimized_summary(DEFAULT_RESUME, "Python Developer", ["Python", "Django", "SQL", "Flask"])
    assert "Python Developer" in opt_sum
    assert "Django" in opt_sum
    print("  -> Summary optimization passed.")


if __name__ == "__main__":
    print("=" * 60)
    print("ATS Resumer Mini-Project - Automated Test Suite")
    print("=" * 60)
    try:
        test_imports()
        test_database_and_auth()
        test_resume_database_persistence()
        test_sample_data()
        test_keyword_extraction()
        test_ats_match_scoring()
        test_pdf_generation_and_parsing()
        test_summary_optimization()
        print("=" * 60)
        print("ALL TESTS PASSED! (8/8 Test Cases Succeeded)")
        print("=" * 60)
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
