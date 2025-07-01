"""
OptiMind - History Page
Show previous optimization jobs
"""

import streamlit as st
from utils.auth import require_auth
from utils.sidebar import create_sidebar

# Page configuration
st.set_page_config(
    page_title="OptiMind - Job History",
    page_icon="📊",
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

/* Custom styles for history page */
.history-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin: 2rem 0;
    text-align: center;
}

.job-card {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #1f77b4;
    margin: 1rem 0;
    transition: all 0.3s ease;
}

.job-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.empty-state {
    text-align: center;
    padding: 4rem 2rem;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

def get_mock_jobs():
    """Return mock job history for demonstration"""
    return [
        {
            "id": "job_001",
            "title": "Production Planning Optimization",
            "description": "Maximize profit: 100*x + 150*y subject to x + 2*y <= 100, x + y <= 80, x >= 0, y >= 0",
            "status": "completed",
            "created_at": "2025-01-15 10:30:00",
            "completed_at": "2025-01-15 10:35:00",
            "objective_type": "maximize",
            "variables": ["x", "y"],
            "constraints": 4,
            "solution": {
                "optimal_value": 8500,
                "x_value": 50,
                "y_value": 25,
                "solver": "CBC"
            }
        },
        {
            "id": "job_002",
            "title": "Portfolio Risk Minimization",
            "description": "Minimize risk: 0.1*x^2 + 0.2*y^2 + 0.15*x*y subject to x + y = 1, x >= 0, y >= 0",
            "status": "completed",
            "created_at": "2025-01-14 15:20:00",
            "completed_at": "2025-01-14 15:25:00",
            "objective_type": "minimize",
            "variables": ["x", "y"],
            "constraints": 3,
            "solution": {
                "optimal_value": 0.125,
                "x_value": 0.6,
                "y_value": 0.4,
                "solver": "HiGHS"
            }
        },
        {
            "id": "job_003",
            "title": "Transportation Cost Optimization",
            "description": "Minimize cost: 10*x1 + 15*x2 + 12*x3 subject to x1 + x2 + x3 >= 50, x1 <= 20, x2 <= 30, x3 <= 25",
            "status": "processing",
            "created_at": "2025-01-15 11:00:00",
            "completed_at": None,
            "objective_type": "minimize",
            "variables": ["x1", "x2", "x3"],
            "constraints": 4,
            "solution": None
        }
    ]

def get_status_color(status):
    """Get color for job status"""
    colors = {
        "completed": "#28a745",
        "processing": "#ffc107",
        "failed": "#dc3545",
        "pending": "#6c757d"
    }
    return colors.get(status, "#6c757d")

def get_status_icon(status):
    """Get icon for job status"""
    icons = {
        "completed": "✅",
        "processing": "🔄",
        "failed": "❌",
        "pending": "⏳"
    }
    return icons.get(status, "❓")

def main():
    """History Page - Show previous optimization jobs"""
    
    # Authentication check
    try:
        name, username = require_auth()
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.stop()
    
    # Create sidebar
    create_sidebar()
    
    # Page header
    st.markdown("""
    <div class="history-header">
        <h1>📊 Job History</h1>
        <p style="font-size: 1.2rem;">
            View and manage your previous optimization jobs
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Breadcrumb navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <span style="color: #999;">🏠 Home</span> → 
            <span style="color: #1f77b4; font-weight: bold;">📊 History</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Filters section
    st.markdown("### 🔍 Filters")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        status_filter = st.selectbox(
            "Status:",
            ["All", "Completed", "Processing", "Failed", "Pending"],
            key="status_filter"
        )
    
    with col2:
        objective_filter = st.selectbox(
            "Objective:",
            ["All", "Maximize", "Minimize"],
            key="objective_filter"
        )
    
    with col3:
        date_filter = st.selectbox(
            "Date:",
            ["All", "Today", "Last 7 days", "Last 30 days"],
            key="date_filter"
        )
    
    with col4:
        search_term = st.text_input(
            "Search:",
            placeholder="Search jobs...",
            key="search_filter"
        )
    
    # Get mock data
    jobs = get_mock_jobs()
    
    # Apply filters (simplified for demo)
    filtered_jobs = jobs
    
    if status_filter != "All":
        filtered_jobs = [job for job in filtered_jobs if job["status"] == status_filter.lower()]
    
    if objective_filter != "All":
        filtered_jobs = [job for job in filtered_jobs if job["objective_type"] == objective_filter.lower()]
    
    if search_term:
        filtered_jobs = [job for job in filtered_jobs if search_term.lower() in job["title"].lower() or search_term.lower() in job["description"].lower()]
    
    # Show results
    st.markdown(f"### 📋 Results ({len(filtered_jobs)} jobs)")
    
    if not filtered_jobs:
        st.markdown("""
        <div class="empty-state">
            <h3>📭 No jobs found</h3>
            <p>No optimization jobs match your current filters.</p>
            <p>Try adjusting your search criteria or create a new job.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for job in filtered_jobs:
            with st.container():
                st.markdown(f"""
                <div class="job-card">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                        <h4 style="margin: 0; color: #1f77b4;">{job['title']}</h4>
                        <span style="color: {get_status_color(job['status'])}; font-weight: bold;">
                            {get_status_icon(job['status'])} {job['status'].title()}
                        </span>
                    </div>
                    <p style="color: #666; margin-bottom: 1rem; font-style: italic;">{job['description']}</p>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; font-size: 0.9rem;">
                        <div><strong>Created:</strong> {job['created_at']}</div>
                        <div><strong>Objective:</strong> {job['objective_type'].title()}</div>
                        <div><strong>Variables:</strong> {', '.join(job['variables'])}</div>
                        <div><strong>Constraints:</strong> {job['constraints']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Show solution if completed
                if job['status'] == 'completed' and job['solution']:
                    with st.expander("📊 View Solution"):
                        sol = job['solution']
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Optimal Value", f"{sol['optimal_value']:.2f}")
                        with col2:
                            st.metric("Solver Used", sol['solver'])
                        with col3:
                            st.metric("X Value", f"{sol['x_value']:.2f}")
                        with col4:
                            st.metric("Y Value", f"{sol['y_value']:.2f}")
                
                # Action buttons
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("👁️ View Details", key=f"view_{job['id']}", use_container_width=True):
                        st.info(f"Detailed view for {job['title']} (Feature coming soon)")
                with col2:
                    if st.button("🔄 Rerun", key=f"rerun_{job['id']}", use_container_width=True):
                        st.info(f"Rerunning {job['title']} (Feature coming soon)")
                with col3:
                    if st.button("📋 Export", key=f"export_{job['id']}", use_container_width=True):
                        st.info(f"Exporting {job['title']} (Feature coming soon)")
                
                st.divider()
    
    # Action buttons at bottom
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("pages/a_Home.py")
    
    with col2:
        if st.button("🚀 New Job", use_container_width=True):
            st.switch_page("pages/d_NewJob.py")
    
    with col3:
        if st.button("🔄 Refresh", use_container_width=True):
            st.rerun()

if __name__ == "__main__":
    main() 