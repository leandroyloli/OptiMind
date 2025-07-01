import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.sidebar import create_sidebar


st.set_page_config(page_title="Admin Tools - OptiMind", page_icon="🛠️", layout="wide")

# Require authentication
from utils.auth import require_auth
name, username = require_auth()

# Only admin can access
if username != "admin":
    st.error("Access restricted: only the administrator can access this page.")
    st.stop()

create_sidebar()

st.title("🛠️ Admin Tools")
st.write("Administrative tools for API connection tests and other utilities. Only the admin can access this page.")

# --- API Connection Tests ---
st.header("API Connection Tests")

with st.expander("Test OpenAI API Connection", expanded=False):
    if st.button("Test OpenAI Connection", key="test_openai_api"):
        import openai
        import time
        # Try to read the key and model from secrets
        api_key = st.secrets["OPENAI"]["OPENAI_API_KEY"]
        model = st.secrets["OPENAI"]["OPENAI_MODEL"]
        if not api_key:
            st.error("OPENAI_API_KEY not found in secrets.")
        else:
            openai.api_key = api_key
            with st.spinner("Testing connection to OpenAI..."):
                try:
                    start = time.time()
                    models = openai.models.list()
                    elapsed = time.time() - start
                    st.success(f"Connection successful! {len(models.data)} models available. (time: {elapsed:.2f}s)")
                except Exception as e:
                    st.error(f"Error connecting to OpenAI API: {e}")

# Future tools can be added below 