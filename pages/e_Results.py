import streamlit as st
from datetime import datetime
from utils import db
from utils.auth import require_auth
from utils.sidebar import create_sidebar
import json

# Page configuration
st.set_page_config(
    page_title="OptiMind - Optimization Results",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide default Streamlit navigation
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

# Authentication check
require_auth()

# Create sidebar
create_sidebar()

def main():
    st.title('📊 Optimization Results')
    st.markdown('---')

    # Buscar o job mais recente do banco
    jobs = db.get_jobs()
    if not jobs:
        st.info('No optimization job has been processed yet.')
        return
    last_job = jobs[0]  # jobs já vem ordenado do mais recente para o mais antigo
    st.markdown(f"**Job ID:** `{last_job['id']}`")
    st.markdown(f"**Title:** {last_job['job_title']}")
    st.markdown(f"**Status:** {last_job['status']}")
    st.markdown('---')
    st.markdown(f"**User input:** {last_job['user_input']}")
    st.markdown('---')

    # Buscar outputs dos agentes
    agent_outputs = db.get_agent_outputs(last_job['id'])
    if not agent_outputs:
        st.warning('No agent outputs found for this job.')
        return
    for output in agent_outputs:
        agent = output['agent_name']
        try:
            data = json.loads(output['json_output'])
        except Exception:
            data = output['json_output']
        with st.expander(f"{agent} Agent Output", expanded=False):
            st.json(data)

    st.markdown('---')
    st.success(last_job.get('final_message', ''))

if __name__ == "__main__":
    main() 