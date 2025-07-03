import streamlit as st
import pandas as pd
from utils import db
from utils.auth import require_auth
from utils.sidebar import create_sidebar
import json
from streamlit_extras.dataframe_explorer import dataframe_explorer

# Page configuration
st.set_page_config(
    page_title="OptiMind - Optimization History",
    page_icon="📜",
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

def display_job_details(job):
    st.markdown(f"**Job ID:** `{job['id']}`")
    st.markdown(f"**Title:** {job['job_title']}")
    st.markdown(f"**Status:** {job['status']}")
    st.markdown('---')
    st.markdown(f"**User input:** {job['user_input']}")
    st.markdown('---')
    agent_outputs = db.get_agent_outputs(job['id'])
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
    st.success(job.get('final_message', ''))

def main():
    st.title('📜 Optimization Job History')
    jobs = db.get_jobs()
    if not jobs:
        st.info('No jobs found.')
        return
    df = pd.DataFrame([
        {
            'ID': job['id'],
            'Created at': job['created_at'],
            'Title': job['job_title'],
            'Status': job['status'],
        }
        for job in jobs
    ])
    st.markdown('🔎 Use the filters below to explore your jobs:')
    filtered_df = dataframe_explorer(df)
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    if filtered_df.empty:
        st.warning('No jobs match the selected filters.')
        return
    job_ids = filtered_df['ID'].tolist()
    selected_id = st.selectbox('Select a job to view details:', job_ids)
    selected_job = next(job for job in jobs if job['id'] == selected_id)
    display_job_details(selected_job)

if __name__ == "__main__":
    main()