# utils/auth_utils.py
import streamlit as st
import bcrypt
import json
import os
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_DIR

# Path to store user credentials
USERS_DB_PATH = DATA_DIR / "users.json"

def create_users_db_if_not_exists():
    """Create users database if it doesn't exist"""
    if not USERS_DB_PATH.exists():
        # Create default admin user
        default_password = "admin123"
        password_bytes = default_password.encode("utf-8")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt).decode("utf-8")
        
        default_admin = {
            "username": "admin",
            "password_hash": hashed_password,
            "email": "admin@example.com"
        }
        
        with open(USERS_DB_PATH, "w") as f:
            json.dump({"users": [default_admin]}, f)

def load_users():
    """Load users from the JSON database"""
    create_users_db_if_not_exists()
    with open(USERS_DB_PATH, "r") as f:
        return json.load(f)["users"]

def save_users(users):
    """Save users to the JSON database"""
    with open(USERS_DB_PATH, "w") as f:
        json.dump({"users": users}, f)

def authenticate(username, password):
    """Authenticate a user"""
    users = load_users()
    for user in users:
        if user["username"] == username and bcrypt.checkpw(
            password.encode("utf-8"), 
            user["password_hash"].encode("utf-8")
        ):
            return True
    return False

def create_user(username, password, email=None):
    """Create a new user"""
    users = load_users()
    
    # Check if username already exists
    if any(user["username"] == username for user in users):
        return False, "Username already exists"
    
    # Hash the password
    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    
    # Create new user
    new_user = {
        "username": username,
        "password_hash": password_hash,
        "email": email
    }
    
    users.append(new_user)
    save_users(users)
    return True, "User created successfully"

def init_auth():
    """Initialize authentication in the Streamlit session state"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "username" not in st.session_state:
        st.session_state.username = None

def login_page():
    """Display the login page"""
    st.title("Welcome to CodRon")
    
    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])
    
    with login_tab:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with signup_tab:
        new_username = st.text_input("Username", key="signup_username")
        new_password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="confirm_password")
        email = st.text_input("Email (optional)", key="signup_email")
        
        if st.button("Sign Up", key="signup_button"):
            if new_password != confirm_password:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                success, message = create_user(new_username, new_password, email)
                if success:
                    st.success(message)
                    st.info("You can now login with your new account")
                else:
                    st.error(message)

def logout():
    """Log out the current user"""
    st.session_state.authenticated = False
    st.session_state.username = None