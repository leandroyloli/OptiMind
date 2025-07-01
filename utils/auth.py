"""
Authentication Module for OptiMind
Manages users, passwords and credential validation
"""

import streamlit as st
import streamlit_authenticator as stauth
import bcrypt
from typing import Dict, List, Tuple, Optional
import json
import os
import time
from datetime import datetime, timedelta
import re

class AuthManager:
    """Manages user authentication"""
    
    def __init__(self):
        self.users_file = "users.json"
        self.login_attempts_file = "login_attempts.json"
        self.max_attempts = 5  # Máximo de tentativas por IP
        self.lockout_duration = 300  # 5 minutos de bloqueio
        self.load_users()
        self.load_login_attempts()
    
    def load_users(self):
        """Loads users from JSON file"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users_data = json.load(f)
        else:
            # Default users for development with SECURE passwords
            self.users_data = {
                "usernames": {
                    "admin": {
                        "name": "Administrator",
                        "password": self._hash_password("Opt1M1nd@2024#Admin")
                    },
                    "demo": {
                        "name": "Demo User",
                        "password": self._hash_password("D3m0@Opt1M1nd#2024!")
                    }
                }
            }
            self.save_users()
    
    def load_login_attempts(self):
        """Loads login attempts for rate limiting"""
        if os.path.exists(self.login_attempts_file):
            with open(self.login_attempts_file, 'r') as f:
                self.login_attempts = json.load(f)
        else:
            self.login_attempts = {}
    
    def save_login_attempts(self):
        """Saves login attempts"""
        with open(self.login_attempts_file, 'w') as f:
            json.dump(self.login_attempts, f, indent=2)
    
    def is_ip_blocked(self, ip_address: str) -> bool:
        """Checks if an IP is blocked due to excessive attempts"""
        if ip_address not in self.login_attempts:
            return False
        
        attempts = self.login_attempts[ip_address]
        if len(attempts) >= self.max_attempts:
            # Check if the lockout is still active
            last_attempt = max(attempts)
            if time.time() - last_attempt < self.lockout_duration:
                return True
            else:
                # Reset attempts after lockout period
                self.login_attempts[ip_address] = []
                self.save_login_attempts()
        
        return False
    
    def record_login_attempt(self, ip_address: str, success: bool):
        """Records a login attempt"""
        if ip_address not in self.login_attempts:
            self.login_attempts[ip_address] = []
        
        current_time = time.time()
        
        if success:
            # Reset attempts on success
            self.login_attempts[ip_address] = []
        else:
            # Add failed attempt
            self.login_attempts[ip_address].append(current_time)
            # Keep only the latest attempts
            self.login_attempts[ip_address] = self.login_attempts[ip_address][-self.max_attempts:]
        
        self.save_login_attempts()
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validates password strength"""
        if len(password) < 12:
            return False, "Password must have at least 12 characters"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False, "Password must contain at least one special character"
        
        return True, "Strong password"
    
    def save_users(self):
        """Saves users to JSON file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users_data, f, indent=2)
    
    def _hash_password(self, password: str) -> str:
        """Password hash using bcrypt"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verifies if the password is correct"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    def add_user(self, username: str, name: str, password: str) -> Tuple[bool, str]:
        """Adds new user with password validation"""
        if username in self.users_data["usernames"]:
            return False, "User already exists"
        
        # Validate password strength
        is_strong, message = self.validate_password_strength(password)
        if not is_strong:
            return False, f"Weak password: {message}"
        
        self.users_data["usernames"][username] = {
            "name": name,
            "password": self._hash_password(password)
        }
        self.save_users()
        return True, "User created successfully"
    
    def remove_user(self, username: str) -> bool:
        """Removes user"""
        if username in self.users_data["usernames"]:
            del self.users_data["usernames"][username]
            self.save_users()
            return True
        return False
    
    def get_user_info(self, username: str) -> Optional[Dict]:
        """Returns user information"""
        return self.users_data["usernames"].get(username)
    
    def list_users(self) -> List[str]:
        """Lists all users"""
        return list(self.users_data["usernames"].keys())

def get_client_ip():
    """Gets client IP (simplified for development)"""
    # In production, this would be obtained from the request
    return "127.0.0.1"

def create_authenticator() -> stauth.Authenticate:
    """Creates Streamlit authenticator instance"""
    # Load users from JSON file or use default
    auth_manager = AuthManager()
    
    # Convert to streamlit-authenticator format
    credentials = {
        'usernames': {}
    }
    
    for username, user_data in auth_manager.users_data["usernames"].items():
        credentials['usernames'][username] = {
            'name': user_data['name'],
            'password': user_data['password']
        }
    
    return stauth.Authenticate(
        credentials=credentials,
        cookie_name="optimind_cookie",
        cookie_key="abcdef",  # até v0.4.2 usa-se `cookie_key`
        location="main",
        cookie_expiry_days=30
    )

def check_auth_status() -> Tuple[Optional[str], Optional[str], bool]:
    """
    Checks authentication status using session_state
    Returns: (name, username, authentication_status)
    """
    # Check if already authenticated
    auth_status = st.session_state.get("authentication_status")
    name = st.session_state.get("name")
    username = st.session_state.get("username")
    
    if auth_status == True:
        return name, username, auth_status
    
    # If not authenticated, show custom login screen
    show_login_screen()
    
    # Check status after login attempt
    auth_status = st.session_state.get("authentication_status")
    name = st.session_state.get("name")
    username = st.session_state.get("username")
    
    return name, username, auth_status

def show_status_message(message: str, message_type: str = "info"):
    """Shows a status message aligned with the login container"""
    colors = {
        "error": {"bg": "#fee", "color": "#c53030", "border": "#fed7d7"},
        "warning": {"bg": "#fffbeb", "color": "#c05621", "border": "#fef5e7"},
        "success": {"bg": "#f0fff4", "color": "#2f855a", "border": "#c6f6d5"},
        "info": {"bg": "#ebf8ff", "color": "#2b6cb0", "border": "#bee3f8"}
    }
    
    style = colors.get(message_type, colors["info"])
    
    st.markdown(f"""
    <div style="max-width: 400px; margin: 0 auto;">
        <div style="background: {style['bg']}; color: {style['color']}; padding: 1rem; border-radius: 8px; border: 1px solid {style['border']}; text-align: center; font-weight: 500;">
            {message}
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_login_screen():
    """Shows custom and beautiful login screen"""
    
    # Hide sidebar and default Streamlit elements
    st.markdown("""
    <style>
    section[data-testid="stSidebar"] {display: none !important;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom styles for status messages */
    .status-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid #e0e0e0;
        max-width: 400px;
        margin: 0 auto;
    }
    .status-message {
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 500;
    }
    .status-error {
        background: #fee;
        color: #c53030;
        border: 1px solid #fed7d7;
    }
    .status-warning {
        background: #fffbeb;
        color: #c05621;
        border: 1px solid #fef5e7;
    }
    .status-success {
        background: #f0fff4;
        color: #2f855a;
        border: 1px solid #c6f6d5;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Container principal centralizado
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Header do login
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <h1 style="color: #1f77b4; font-size: 2.5rem; margin: 0; font-weight: 700;">🧠 OptiMind</h1>
            <p style="color: #666; font-size: 1.1rem; margin: 0.5rem 0 0 0;">AI-Powered Optimization Platform</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Welcome message
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 10px; margin-bottom: 2rem; text-align: center;">
            <h3 style="margin: 0 0 0.5rem 0; font-size: 1.3rem;">👋 Welcome!</h3>
            <p style="margin: 0; opacity: 0.9; font-size: 0.95rem;">Access the most advanced optimization platform in the market</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Form container
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 1rem;">
            <h4 style="color: #333; margin: 0; text-align: center;">🔐 System Access</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Status messages container (will be populated by streamlit-authenticator)
        status_container = st.container()
        
        # Formulário de login usando streamlit-authenticator
        authenticator = create_authenticator()
        authenticator.login(
            location="main",
            fields={"Form name": "Login"}
        )
        
        # Close the form container
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add space for status messages that might appear
        st.markdown("""
        <div style="height: 2rem;"></div>
        """, unsafe_allow_html=True)
        

def logout():
    """Performs user logout"""
    # Clear all authentication-related session state
    auth_keys = ['authentication_status', 'name', 'username']
    for key in auth_keys:
        if key in st.session_state:
            del st.session_state[key]
    
    # Show success message
    st.success("✅ Logout successful!")
    
    # Force page reload to show login screen
    st.rerun()

def require_auth():
    """
    Decorator to require authentication
    If not authenticated, stops execution
    """
    name, username, auth_status = check_auth_status()
    
    if auth_status == False:
        show_status_message("❌ Incorrect username/password", "error")
        st.stop()
    elif auth_status == None:
        show_status_message("⚠️ Please enter your credentials", "warning")
        st.stop()
    elif auth_status == True:
        # Successful login
        return name, username
    
    # If we got here, still not authenticated
    st.stop()

def check_openai_rate_limit():
    """
    Permite até 1000 requisições à OpenAI a cada 5 minutos por usuário (session_state).
    Retorna (permitido: bool, tempo_restante_segundos: int)
    """
    import time
    max_requests = 1000
    window_seconds = 5 * 60  # 5 minutos
    now = int(time.time())
    key = "openai_requests"
    if key not in st.session_state:
        st.session_state[key] = []
    # Remove timestamps fora da janela
    st.session_state[key] = [t for t in st.session_state[key] if now - t < window_seconds]
    if len(st.session_state[key]) >= max_requests:
        tempo_restante = window_seconds - (now - st.session_state[key][0])
        return False, tempo_restante
    st.session_state[key].append(now)
    return True, 0 