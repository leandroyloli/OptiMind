"""
OptiMind - Página Home
"""

import streamlit as st
from utils.auth import require_auth

# Configuração da página
st.set_page_config(
    page_title="OptiMind - Home",
    page_icon="🏠",
    layout="wide"
)

def main():
    """Página Home do OptiMind"""
    
    # Verificar autenticação
    try:
        name, username = require_auth()
    except Exception as e:
        st.error(f"Erro na autenticação: {str(e)}")
        st.stop()
    
    # Header principal
    st.title("🏠 OptiMind - Home")
    st.subheader(f"Bem-vindo, {name}!")
    
    # Descrição do sistema
    st.markdown("""
    ### O que é o OptiMind?
    
    O **OptiMind** é uma plataforma revolucionária que transforma descrições em linguagem natural 
    de problemas de otimização em soluções matemáticas completas, código executável e insights de negócio.
    
    ### 🚀 Como funciona?
    
    1. **Descreva seu problema** em linguagem natural
    2. **Confirme a interpretação** do sistema
    3. **Aguarde o processamento** pelos agentes especializados
    4. **Receba a solução** com insights detalhados
    
    ### 🎯 Exemplos de problemas que você pode resolver:
    
    - **Maximizar lucro** vendendo produtos A e B com limite de produção
    - **Minimizar custos** de transporte entre fábricas e clientes
    - **Otimizar alocação** de recursos em projetos
    - **Encontrar mix ideal** de investimentos
    """)
    
    # Botão para novo job
    st.divider()
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🆕 Criar Novo Job de Otimização", type="primary", use_container_width=True):
            st.info("🚧 Esta funcionalidade será implementada no próximo bloco.")
    
    # Status do sistema
    st.divider()
    st.subheader("📊 Status do Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Status", "🟢 Online")
    
    with col2:
        st.metric("Agentes", "6 Ativos")
    
    with col3:
        st.metric("Jobs Hoje", "0")
    
    with col4:
        st.metric("Tempo Médio", "< 30s")

if __name__ == "__main__":
    main() 