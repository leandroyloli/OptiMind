import streamlit as st
from utils.auth import AuthManager, require_auth
from utils.sidebar import create_sidebar

st.set_page_config(page_title="User Management - OptiMind", page_icon="👤", layout="wide")

# Require authentication
name, username = require_auth()

# Only admin can access
if username != "admin":
    st.error("Access restricted: only the administrator can access this page.")
    st.stop()

create_sidebar()

st.title("👤 User Management")
st.write("Add or remove users from the system. Only the admin can access this page.")

# Instantiate the user manager
auth_manager = AuthManager()

# List users
st.subheader("Registered Users")
users = auth_manager.list_users()
st.write(users)

# Form to add user
st.subheader("Add New User")
with st.form("add_user_form"):
    new_username = st.text_input("Username")
    new_name = st.text_input("Full Name")
    new_password = st.text_input("Password", type="password")
    submit_add = st.form_submit_button("Add User")
    if submit_add:
        success, msg = auth_manager.add_user(new_username, new_name, new_password)
        if success:
            st.success(msg)
            st.rerun()
        else:
            st.error(msg)

# Remove user
st.subheader("Remove User")
user_to_remove = st.selectbox("Select user to remove", [u for u in users if u != "admin"])
if st.button("Remove User"):
    if user_to_remove:
        if auth_manager.remove_user(user_to_remove):
            st.success(f"User '{user_to_remove}' removed successfully.")
            st.rerun()
        else:
            st.error("Error removing user.") 

