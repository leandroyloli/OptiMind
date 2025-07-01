"""
Sidebar utility for OptiMind
Centralized sidebar functionality for all pages
"""

import streamlit as st
from utils.auth import logout

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
    
    # Botão de gestão de usuários (apenas para admin)
    if username == "admin":
        if st.sidebar.button("👤 Gestão de Usuários", use_container_width=True):
            st.switch_page("pages/gestao_usuarios.py")
    
    # Navigation buttons - clean
    if st.sidebar.button("🏠 Home", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Home.py")
    
    if st.sidebar.button("🚀 New Job", use_container_width=True):
        st.info("🔄 Redirecting to optimization interface...")
        # TODO: Implement new job page
    
    if st.sidebar.button("📊 History", use_container_width=True):
        st.info("🔄 Redirecting to history...")
        # TODO: Implement history page
    
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