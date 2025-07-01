import streamlit as st
from utils.auth import AuthManager, require_auth
from utils.sidebar import create_sidebar

st.set_page_config(page_title="Gestão de Usuários - OptiMind", page_icon="👤", layout="wide")

# Autenticação obrigatória
name, username = require_auth()

# Só admin pode acessar
if username != "admin":
    st.error("Acesso restrito: apenas o administrador pode acessar esta página.")
    st.stop()

create_sidebar()

st.title("👤 Gestão de Usuários")
st.write("Adicione ou remova usuários do sistema. Apenas o admin pode acessar esta página.")

# Instancia o gerenciador de usuários
auth_manager = AuthManager()

# Lista de usuários
st.subheader("Usuários cadastrados")
usuarios = auth_manager.list_users()
st.write(usuarios)

# Formulário para adicionar usuário
st.subheader("Adicionar novo usuário")
with st.form("add_user_form"):
    novo_username = st.text_input("Username")
    novo_nome = st.text_input("Nome completo")
    nova_senha = st.text_input("Senha", type="password")
    submit_add = st.form_submit_button("Adicionar usuário")
    if submit_add:
        sucesso, msg = auth_manager.add_user(novo_username, novo_nome, nova_senha)
        if sucesso:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

# Remover usuário
st.subheader("Remover usuário")
usuario_remover = st.selectbox("Selecione o usuário para remover", [u for u in usuarios if u != "admin"])
if st.button("Remover usuário"):
    if usuario_remover:
        if auth_manager.remove_user(usuario_remover):
            st.success(f"Usuário '{usuario_remover}' removido com sucesso.")
            st.rerun()
        else:
            st.error("Erro ao remover usuário.") 