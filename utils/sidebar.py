"""
Sidebar utility for OptiMind
Centralized sidebar functionality for all pages
"""

import streamlit as st
from utils.auth import logout

def clear_chat_cache():
    """Limpa todo o cache relacionado ao chat e pipeline de processamento"""
    keys_to_clear = [
        'chat_messages',
        'meaning_agent',
        'researcher_agent',
        'problem_ready',
        'final_problem_data',
        'refined_problem_data',
        'pipeline_stage',
        'pipeline_complete',
        'current_job_id',
        'processing_complete',
        'optimization_results'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

def create_sidebar():
    """Creates the sidebar with user management - reusable across all pages"""
    
    # Recupera o usuário logado
    username = st.session_state.get("username")
    
    # Custom CSS for sidebar - clean and minimalist
    st.markdown("""
    <style>
    .sidebar-header {
        text-align: center;
        padding: 1.5rem 0;
        margin-bottom: 2rem;
        border-bottom: 1px solid #e0e0e0;
    }
    .user-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        text-align: center;
        border: 1px solid #e0e0e0;
    }
    .sidebar-section {
        margin: 1rem 0;
        padding: 0.5rem 0;
    }
    .sidebar-section h4 {
        font-size: 0.9rem;
        color: #666;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar header - clean
    st.sidebar.markdown("""
    <div class="sidebar-header">
        <h2 style="margin: 0; color: #1f77b4;">🧠 OptiMind</h2>
        <p style="font-size: 0.8rem; color: #888; margin: 0.5rem 0 0 0;">AI-Powered Optimization</p>
    </div>
    """, unsafe_allow_html=True)
    
    # User management button (admin only)
    if username == "admin":
        if st.sidebar.button("👤 User Management", use_container_width=True):
            st.switch_page("pages/c_UserManagement.py")
        if st.sidebar.button("🛠️ Admin Tools", use_container_width=True):
            st.switch_page("pages/b_AdminTools.py")
    
    # Navigation buttons - clean
    if st.sidebar.button("🏠 Home", use_container_width=True, type="primary"):
        st.switch_page("pages/a_Home.py")
    
    if st.sidebar.button("🚀 New Job", use_container_width=True):
        # Limpar cache antes de navegar para novo job
        clear_chat_cache()
        st.switch_page("pages/d_NewJob.py")
    
    if st.sidebar.button("📊 Results", use_container_width=True):
        st.switch_page("pages/e_Results.py")
    
    if st.sidebar.button("📜 History", use_container_width=True):
        st.switch_page("pages/f_History.py")
    
    # Logout button - clean
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout", use_container_width=True, type="secondary"):
        logout()
    
    # Sidebar footer - clean
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; font-size: 0.7rem; color: #999;">
        <p style="margin: 0.2rem 0;">Powered by Mirow & Co.</p>
        <p style="margin: 0.2rem 0;">© 2025 OptiMind</p>
    </div>
    """, unsafe_allow_html=True) 