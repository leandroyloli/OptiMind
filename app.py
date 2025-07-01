"""
OptiMind - AI-Powered Optimization Platform
Main page with authentication and sidebar
"""

import streamlit as st
from utils.auth import require_auth
from utils.sidebar import create_sidebar

# Page configuration
st.set_page_config(
    page_title="OptiMind - AI-Powered Optimization by Mirow & Co.",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default Streamlit elements
st.markdown("""
<style>
footer {visibility: hidden;}

/* Hide default Streamlit sidebar navigation but keep the sidebar itself */
section[data-testid="stSidebar"] ul[data-testid="stSidebarNav"] {
    display: none !important;
}

/* Hide any other default navigation elements */
[data-testid="stSidebarNav"] {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# Sidebar function is now imported from utils.sidebar

def main():
    """Main page with authentication and sidebar"""
    
    # Check authentication
    try:
        name, username = require_auth()
    except Exception as e:
        # If not authenticated, the require_auth function already shows the login screen
        # and stops execution, so we don't need to do anything here
        return
    
    # If we got here, user is authenticated - create sidebar
    create_sidebar()
    
    # Main content
    st.markdown("""
    <div style="text-align: center; padding: 3rem;">
        <h1>🧠 OptiMind</h1>
        <h2 style="color: #7f8c8d;">AI-Powered Optimization Platform</h2>
        <p style="font-size: 1.2rem; margin-top: 2rem;">
            Welcome to OptiMind! Use the sidebar to navigate through the platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show welcome message instead of redirecting
    # st.success("✅ Welcome to OptiMind! Use the sidebar to navigate through the platform.")

if __name__ == "__main__":
    main() 