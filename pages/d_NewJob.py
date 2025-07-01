"""
OptiMind - New Job Page
Interface for defining optimization problems
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import re
from utils.auth import require_auth
from utils.sidebar import create_sidebar

# Page configuration
st.set_page_config(
    page_title="OptiMind - New Optimization Job",
    page_icon="🚀",
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

/* Custom styles for the new job page */
.problem-input-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin: 2rem 0;
}

.validation-section {
    background: #f8f9fa;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #28a745;
    margin: 1rem 0;
}

.error-section {
    background: #f8d7da;
    padding: 1.5rem;
    border-radius: 10px;
    border-left: 4px solid #dc3545;
    margin: 1rem 0;
    color: #721c24;
}

.example-card {
    background: #e3f2fd;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #2196f3;
    margin: 0.5rem 0;
    cursor: pointer;
    transition: all 0.3s ease;
}

.example-card:hover {
    background: #bbdefb;
    transform: translateY(-2px);
}

.objective-selector {
    background: #f1f3f4;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def validate_optimization_input(text, objective_type):
    """
    Validate optimization problem input
    Returns: (is_valid, errors, suggestions)
    """
    errors = []
    suggestions = []
    
    # Check if text is empty
    if not text or text.strip() == "":
        errors.append("Problem description cannot be empty")
        suggestions.append("Please describe your optimization problem")
        return False, errors, suggestions
    
    # Check minimum length
    if len(text.strip()) < 10:
        errors.append("Problem description is too short")
        suggestions.append("Please provide more details about your problem")
        return False, errors, suggestions
    
    # Check for optimization keywords
    optimization_keywords = ['maximize', 'minimize', 'maximizar', 'minimizar', 'max', 'min']
    has_optimization_keyword = any(keyword in text.lower() for keyword in optimization_keywords)
    
    if not has_optimization_keyword:
        errors.append("No optimization objective found")
        suggestions.append("Include words like 'maximize', 'minimize', 'max', or 'min' in your description")
    
    # Check for variables (common patterns)
    variable_patterns = [
        r'\b[a-zA-Z]\b',  # Single letters
        r'\b[a-zA-Z][a-zA-Z0-9_]*\b',  # Variables with numbers/underscores
        r'\b(x|y|z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w)\b'  # Common variable names
    ]
    
    has_variables = any(re.search(pattern, text) for pattern in variable_patterns)
    if not has_variables:
        errors.append("No variables found in the problem")
        suggestions.append("Include variables like x, y, z, or other letters in your problem")
    
    # Check for constraints (common patterns)
    constraint_keywords = [
        'subject to', 's.t.', 'constraint', 'restriction', 'limit', 'bound', 
        '<=', '>=', '=', '<', '>', 'at least', 'at most', 'minimum', 'maximum',
        'maintain', 'balance', 'cash', 'budget', 'capacity', 'demand', 'supply'
    ]
    has_constraints = any(keyword in text.lower() for keyword in constraint_keywords)
    
    if not has_constraints:
        errors.append("No constraints found in the problem")
        suggestions.append("Include constraints using words like 'subject to', '<=', '>=', 'at least', 'maintain', or mathematical symbols")
    
    # If no errors, add positive feedback
    if not errors:
        suggestions.append("✅ Problem looks good! Ready for processing.")
    
    return len(errors) == 0, errors, suggestions

def get_example_problems():
    """Return example optimization problems"""
    return [
        {
            "title": "Production Planning",
            "description": "Maximize profit: 100*x + 150*y subject to x + 2*y <= 100, x + y <= 80, x >= 0, y >= 0",
            "objective": "maximize"
        },
        {
            "title": "Portfolio Optimization",
            "description": "Minimize risk: 0.1*x^2 + 0.2*y^2 + 0.15*x*y subject to x + y = 1, x >= 0, y >= 0",
            "objective": "minimize"
        },
        {
            "title": "Transportation Problem",
            "description": "Minimize cost: 10*x1 + 15*x2 + 12*x3 subject to x1 + x2 + x3 >= 50, x1 <= 20, x2 <= 30, x3 <= 25",
            "objective": "minimize"
        },
        {
            "title": "Resource Allocation",
            "description": "Maximize efficiency: 5*x + 3*y + 4*z subject to 2*x + y + z <= 100, x + 3*y + 2*z <= 150, x,y,z >= 0",
            "objective": "maximize"
        }
    ]

def main():
    """New Job Page - Define optimization problem"""
    
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
    <div style="text-align: center; padding: 2rem;">
        <h1>🚀 New Optimization Job</h1>
        <p style="font-size: 1.2rem; color: #666;">
            Describe your optimization problem in natural language
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Breadcrumb navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <span style="color: #999;">🏠 Home</span> → 
            <span style="color: #1f77b4; font-weight: bold;">🚀 New Job</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize session state for this page
    if 'new_job_data' not in st.session_state:
        st.session_state.new_job_data = {
            'problem_description': '',
            'objective_type': 'maximize',
            'is_valid': False,
            'validation_errors': [],
            'validation_suggestions': []
        }
    
    st.divider()

    # Problem input section
    st.markdown("""
    <div class="problem-input-section">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">📝 Define Your Optimization Problem</h3>
        <p style="text-align: center; font-size: 1.1rem;">
            You will be talking to the Meaning Agent, our first AI specialist. Describe your problem in natural language. Include variables, objective function, and constraints.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Objective type selection
    # st.markdown('<div class="objective-selector">', unsafe_allow_html=True)
    st.markdown("### 🎯 Optimization Objective")
    objective_type = st.radio(
        "Choose the type of optimization:",
        ["Maximize", "Minimize"],
        horizontal=True,
        key="objective_selector"
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Problem description input
    problem_description = st.text_area(
        "**Describe your optimization problem:**",
        placeholder="Example: Maximize profit: 100*x + 150*y subject to x + 2*y <= 100, x + y <= 80, x >= 0, y >= 0",
        height=400,
        key="problem_input"
    )
    
    # # Examples section
    # st.markdown("### 💡 Example Problems")
    # st.markdown("Click on an example to use it as a starting point:")
    
    # examples = get_example_problems()
    # cols = st.columns(2)
    
    # for i, example in enumerate(examples):
    #     with cols[i % 2]:
    #         if st.button(
    #             f"**{example['title']}**\n{example['description'][:60]}...",
    #             key=f"example_{i}",
    #             use_container_width=True
    #         ):
    #             st.session_state.new_job_data['problem_description'] = example['description']
    #             st.session_state.new_job_data['objective_type'] = example['objective']
    #             st.rerun()
    
    # Validation section
    if problem_description:
        is_valid, errors, suggestions = validate_optimization_input(problem_description, objective_type)
        
        # Update session state
        st.session_state.new_job_data.update({
            'problem_description': problem_description,
            'objective_type': objective_type,
            'is_valid': is_valid,
            'validation_errors': errors,
            'validation_suggestions': suggestions
        })
        
        # Show validation results
        if not is_valid:
            st.markdown("""
            <div class="error-section">
                <h4>⚠️ Validation Issues</h4>
            </div>
            """, unsafe_allow_html=True)
            
            for error in errors:
                st.error(f"• {error}")
            
            st.markdown("**💡 Suggestions:**")
            for suggestion in suggestions:
                st.info(f"• {suggestion}")
    
    # Action buttons
    st.divider()
    
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("pages/a_Home.py")
    
    with col4:
        if st.button("🚀 Start Processing", type="primary", use_container_width=True, 
                    disabled=not st.session_state.new_job_data.get('is_valid', False)):
            if st.session_state.new_job_data.get('is_valid', False):
                st.info("🔄 Redirecting to processing pipeline...")
                st.success("✅ Problem submitted! Processing pipeline will be implemented in the next block.")
            else:
                st.error("Please fix validation issues before processing")

if __name__ == "__main__":
    main() 