"""
OptiMind - Plataforma de Otimização Assistida por IA
Página principal com autenticação
"""

import streamlit as st
from utils.auth import require_auth

# Configuração da página
st.set_page_config(
    page_title="OptiMind - Login",
    page_icon="🧠",
    layout="wide"
)

def main():
    """Página principal com autenticação"""
    
    # Verificar autenticação
    try:
        name, username = require_auth()
    except Exception as e:
        st.error(f"Erro na autenticação: {str(e)}")
        st.stop()
    
    # Se chegou aqui, usuário está autenticado
    st.success(f"✅ Autenticação bem-sucedida! Bem-vindo, {name}!")
    
    # Redirecionar para a página Home
    st.switch_page("pages/1_Home.py")

if __name__ == "__main__":
    main() 