"""
OptiMind - New Job Page
Interactive chat interface with Meaning Agent for defining optimization problems (simplified)
"""

import streamlit as st
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import re
import json
from utils.auth import require_auth
from utils.sidebar import create_sidebar

# Import Meaning Agent
try:
    from agents.meaning_agent import MeaningAgent
except ImportError as e:
    st.error(f"Error importing Meaning Agent: {e}")
    st.stop()

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

.problem-input-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 15px;
    color: white;
    margin: 2rem 0;
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

def display_problem_summary(problem_data):
    """Display a simple summary of the problem when it's ready"""
    if problem_data and problem_data.get('is_valid_problem', False):
        st.success("✅ Problem ready for processing!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Problem Type", problem_data.get('problem_type', 'Unknown'))
            st.metric("Confidence", f"{problem_data.get('confidence', 0.0):.1%}")
        
        with col2:
            decision_vars = problem_data.get('decision_variables', {})
            auxiliary_vars = problem_data.get('auxiliary_variables', {})
            st.metric("Decision Variables", len(decision_vars))
            st.metric("Auxiliary Variables", len(auxiliary_vars))
        
        # Display the problem in a structured format for validation
        st.markdown("---")
        st.markdown("### 📋 Problem Summary")
        
        # Problem type and objective
        problem_type = problem_data.get('problem_type', 'Unknown')
        sense = problem_data.get('sense', 'maximize')
        objective = problem_data.get('objective', '')
        objective_desc = problem_data.get('objective_description', '')
        
        st.markdown(f"**Problem Type:** {problem_type}")
        st.markdown(f"**Objective:** {sense} {objective}")
        if objective_desc:
            st.markdown(f"**Description:** {objective_desc}")
        
        # Decision Variables
        if decision_vars:
            st.markdown("**Decision Variables:**")
            for var_name, var_info in decision_vars.items():
                var_type = var_info.get('type', 'Unknown')
                var_desc = var_info.get('description', 'No description')
                bounds = var_info.get('bounds', [])
                bounds_str = f" [{bounds[0]}, {bounds[1] if bounds[1] is not None else '∞'}]" if bounds else ""
                st.markdown(f"• **{var_name}** ({var_type}){bounds_str}: {var_desc}")
        
        # Auxiliary Variables
        if auxiliary_vars:
            st.markdown("**Auxiliary Variables:**")
            for var_name, var_info in auxiliary_vars.items():
                var_type = var_info.get('type', 'Unknown')
                var_desc = var_info.get('description', 'No description')
                equation = var_info.get('equation', 'No equation')
                st.markdown(f"• **{var_name}** ({var_type}): {var_desc} = {equation}")
        
        # Constraints
        constraints = problem_data.get('constraints', [])
        if constraints:
            st.markdown(f"**Constraints ({len(constraints)}):**")
            for i, constraint in enumerate(constraints, 1):
                expression = constraint.get('expression', 'No expression')
                description = constraint.get('description', 'No description')
                constraint_type = constraint.get('type', 'Unknown')
                st.markdown(f"{i}. **{expression}** ({constraint_type}): {description}")
        
        st.markdown("---")
        st.info("💡 **Please review the problem summary above. If everything looks correct, you can proceed to processing. If you need any adjustments, continue the conversation with the Meaning Agent.**")

def main():
    """New Job Page - Interactive chat with Meaning Agent (simplified)"""
    
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
            Chat with our Meaning Agent to define your optimization problem. Just describe your problem in natural language below.
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
    
    # Initialize session state for chat
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
        st.session_state.meaning_agent = None
        st.session_state.problem_ready = False
        st.session_state.final_problem_data = None
    
    # Initialize Meaning Agent
    if st.session_state.meaning_agent is None:
        try:
            st.session_state.meaning_agent = MeaningAgent()
            # Add welcome message
            if not st.session_state.chat_messages:
                st.session_state.chat_messages.append({
                    'sender': 'assistant',
                    'message': "Hi! I'm the Meaning Agent. I'm here to help you define optimization problems. Just tell me what you want to optimize and I'll help you structure it step by step. What would you like to work on?"
                })
        except Exception as e:
            st.error(f"Failed to initialize Meaning Agent: {e}")
            st.stop()
    
    st.divider()

    # Chat interface
    st.markdown("""
    <div class="problem-input-section">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">💬 Chat with Meaning Agent</h3>
        <p style="text-align: center; font-size: 1.1rem;">
            Just describe your optimization problem below. The agent will help you structure it and remember our conversation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Botões de ação no topo
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("pages/a_Home.py")
    with col4:
        if st.button("🚀 Start Processing", type="primary", use_container_width=True, 
                    disabled=not st.session_state.problem_ready):
            if st.session_state.problem_ready:
                st.success("✅ Problem ready! Processing pipeline will be implemented in the next block.")
                st.info(f"Problem data: {json.dumps(st.session_state.final_problem_data, indent=2)}")
            else:
                st.error("Please complete the conversation with the Meaning Agent first")

    # Chat interface
    for idx, message in enumerate(st.session_state.chat_messages):
        with st.chat_message(message['sender']):
            st.text(message['message'])
            # Se for a última mensagem do agente e o problema está pronto, mostrar apenas o resumo dentro da bolha
            if (
                message['sender'] == 'assistant' and
                idx == len(st.session_state.chat_messages) - 1 and
                st.session_state.problem_ready and
                st.session_state.final_problem_data
            ):
                problem_data = st.session_state.final_problem_data
                st.markdown("---")
                st.markdown("### 📋 Problem Summary")
                problem_type = problem_data.get('problem_type', 'Unknown')
                sense = problem_data.get('sense', 'maximize')
                objective = problem_data.get('objective', '')
                objective_desc = problem_data.get('objective_description', '')
                st.markdown(f"**Problem Type:** {problem_type}")
                st.markdown(f"**Objective:** {sense} {objective}")
                if objective_desc:
                    st.markdown(f"**Description:** {objective_desc}")
                decision_vars = problem_data.get('decision_variables', {})
                auxiliary_vars = problem_data.get('auxiliary_variables', {})
                if decision_vars:
                    st.markdown(f"**Decision Variables ({len(decision_vars)}):**")
                    for i, (var_name, var_info) in enumerate(decision_vars.items(), 1):
                        var_type = var_info.get('type', 'Unknown')
                        var_desc = var_info.get('description', 'No description')
                        bounds = var_info.get('bounds', [])
                        bounds_str = f" [{bounds[0]}, {bounds[1] if bounds[1] is not None else '∞'}]" if bounds else ""
                        st.markdown(f"{i}. **{var_name}** ({var_type}){bounds_str}: {var_desc}")
                if auxiliary_vars:
                    st.markdown(f"**Auxiliary Variables ({len(auxiliary_vars)}):**")
                    for i, (var_name, var_info) in enumerate(auxiliary_vars.items(), 1):
                        var_type = var_info.get('type', 'Unknown')
                        var_desc = var_info.get('description', 'No description')
                        equation = var_info.get('equation', 'No equation')
                        st.markdown(f"{i}. **{var_name}** ({var_type}): {var_desc} = {equation}")
                constraints = problem_data.get('constraints', [])
                if constraints:
                    st.markdown(f"**Constraints ({len(constraints)}):**")
                    for i, constraint in enumerate(constraints, 1):
                        expression = constraint.get('expression', 'No expression')
                        description = constraint.get('description', 'No description')
                        constraint_type = constraint.get('type', 'Unknown')
                        st.markdown(f"{i}. **{expression}** ({constraint_type}): {description}")
                st.markdown("---")
                st.info("💡 **Please review the problem summary above. If everything looks correct, you can proceed to processing. If you need any adjustments, continue the conversation with the Meaning Agent.**")
    
    # Chat input usando st.chat_input
    if prompt := st.chat_input("Describe your optimization problem here..."):
        st.session_state.chat_messages.append({
            'sender': 'user',
            'message': prompt
        })
        with st.chat_message("user"):
            st.text(prompt)
        with st.chat_message("assistant"):
            with st.spinner("🤖 Meaning Agent is analyzing your problem..."):
                try:
                    # Process with Meaning Agent (no objective_type needed for context-aware processing)
                    agent_result = st.session_state.meaning_agent.process_problem(prompt)
                    
                    if agent_result.get('success', False):
                        problem_data = agent_result.get('result', {})
                        
                        # Use the natural response from the model (clarification field)
                        agent_message = problem_data.get('clarification', 'I understand your problem. Please provide more details if needed.')
                        
                        # Update problem ready state
                        if problem_data.get('is_valid_problem', False):
                            st.session_state.problem_ready = True
                            st.session_state.final_problem_data = problem_data
                        else:
                            st.session_state.problem_ready = False
                    else:
                        agent_message = f"Sorry, I encountered an error: {agent_result.get('error', 'Unknown error')}"
                        st.session_state.problem_ready = False
                    
                    # Add message to chat history
                    st.session_state.chat_messages.append({
                        'sender': 'assistant',
                        'message': agent_message
                    })
                    
                    # Force a rerun to show the new message
                    st.rerun()
                    
                except Exception as e:
                    error_msg = f"Error processing with Meaning Agent: {str(e)}"
                    st.error(error_msg)
                    st.session_state.chat_messages.append({
                        'sender': 'assistant',
                        'message': error_msg
                    })

if __name__ == "__main__":
    main() 