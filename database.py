"""
Database module for ATS Resumer.
Handles SQLite database connection, table initialization, user authentication,
secure password hashing, and user-associated resume persistence.
"""

import os
import sqlite3
import hashlib
import json
from typing import Dict, List, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "ats_resumer.db")


def get_connection() -> sqlite3.Connection:
    """Get a SQLite database connection with row factory enabled."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def hash_password(password: str, salt: str = "ats_resumer_salt_2026") -> str:
    """Hash password securely using SHA-256 with salt."""
    salted = f"{password}{salt}".encode("utf-8")
    return hashlib.sha256(salted).hexdigest()


def init_db():
    """Initialize database tables and create default demo user if not present."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            full_name TEXT NOT NULL,
            auth_provider TEXT DEFAULT 'local',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 2. Resumes Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            candidate_name TEXT NOT NULL,
            target_role TEXT NOT NULL,
            ats_score INTEGER DEFAULT 0,
            resume_data TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)
    conn.commit()
    
    # Pre-seed demo user (M. Katamaiah) if not exists
    cursor.execute("SELECT id FROM users WHERE email = ?", ("katamaiah@example.com",))
    demo_user = cursor.fetchone()
    if not demo_user:
        hashed = hash_password("password123")
        cursor.execute(
            "INSERT INTO users (email, password_hash, full_name, auth_provider) VALUES (?, ?, ?, ?)",
            ("katamaiah@example.com", hashed, "M. Katamaiah", "local")
        )
        conn.commit()
        
    conn.close()


def create_user(email: str, password: str, full_name: str, auth_provider: str = "local") -> Tuple[bool, str, Optional[Dict]]:
    """Register a new user in SQLite database."""
    email_clean = email.strip().lower()
    name_clean = full_name.strip()
    
    if not email_clean or not name_clean:
        return False, "Email and full name are required.", None
        
    if auth_provider == "local" and (not password or len(password) < 6):
        return False, "Password must be at least 6 characters long.", None
        
    conn = get_connection()
    cursor = conn.cursor()
    try:
        pw_hash = hash_password(password) if password else None
        cursor.execute(
            "INSERT INTO users (email, password_hash, full_name, auth_provider) VALUES (?, ?, ?, ?)",
            (email_clean, pw_hash, name_clean, auth_provider)
        )
        conn.commit()
        user_id = cursor.lastrowid
        user_record = {
            "id": user_id,
            "email": email_clean,
            "full_name": name_clean,
            "auth_provider": auth_provider
        }
        return True, "Account created successfully!", user_record
    except sqlite3.IntegrityError:
        return False, "An account with this email already exists.", None
    finally:
        conn.close()


def authenticate_user(email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
    """Authenticate user with email and password."""
    email_clean = email.strip().lower()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email_clean,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        return False, "No account found with this email address.", None
        
    if user["auth_provider"] == "google" and not user["password_hash"]:
        return False, "This account is registered with Google. Please use 'Continue with Google'.", None
        
    hashed = hash_password(password)
    if user["password_hash"] != hashed:
        return False, "Incorrect password. Please try again.", None
        
    user_record = {
        "id": user["id"],
        "email": user["email"],
        "full_name": user["full_name"],
        "auth_provider": user["auth_provider"]
    }
    return True, f"Welcome back, {user['full_name']}!", user_record


def authenticate_google_user(email: str, full_name: str) -> Tuple[bool, str, Dict]:
    """Find or create user via Google Authentication."""
    email_clean = email.strip().lower()
    name_clean = full_name.strip() or "Google User"
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email_clean,))
    user = cursor.fetchone()
    
    if user:
        user_record = {
            "id": user["id"],
            "email": user["email"],
            "full_name": user["full_name"],
            "auth_provider": user["auth_provider"]
        }
        conn.close()
        return True, f"Signed in with Google as {user['full_name']}", user_record
        
    # Register new user from Google
    cursor.execute(
        "INSERT INTO users (email, password_hash, full_name, auth_provider) VALUES (?, NULL, ?, 'google')",
        (email_clean, name_clean)
    )
    conn.commit()
    user_id = cursor.lastrowid
    user_record = {
        "id": user_id,
        "email": email_clean,
        "full_name": name_clean,
        "auth_provider": "google"
    }
    conn.close()
    return True, f"Google account linked: Welcome, {name_clean}!", user_record


# ==========================================================
# RESUME PERSISTENCE FUNCTIONS
# ==========================================================

def save_user_resume(user_id: int, candidate_name: str, target_role: str, ats_score: int, resume_data: Dict) -> int:
    """Save or insert a resume record under the specific user's account."""
    conn = get_connection()
    cursor = conn.cursor()
    resume_json = json.dumps(resume_data)
    cursor.execute(
        """
        INSERT INTO resumes (user_id, candidate_name, target_role, ats_score, resume_data)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, candidate_name, target_role, ats_score, resume_json)
    )
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return resume_id


def get_user_resumes(user_id: int) -> List[Dict]:
    """Fetch all saved resumes for a specific user, sorted newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, user_id, candidate_name, target_role, ats_score, resume_data, created_at FROM resumes WHERE user_id = ? ORDER BY created_at DESC",
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    resumes = []
    for r in rows:
        try:
            data = json.loads(r["resume_data"])
        except Exception:
            data = {}
        resumes.append({
            "id": r["id"],
            "name": r["candidate_name"],
            "role": r["target_role"],
            "score": r["ats_score"],
            "date": r["created_at"][:16] if r["created_at"] else "Recently",
            "data": data
        })
    return resumes


def delete_user_resume(resume_id: int, user_id: int) -> bool:
    """Delete a specific resume belonging to the user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM resumes WHERE id = ? AND user_id = ?", (resume_id, user_id))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0
