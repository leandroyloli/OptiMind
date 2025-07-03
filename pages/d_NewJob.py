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
from utils.sidebar import create_sidebar, clear_chat_cache
import datetime
from utils import db

# Import Agents
try:
    from agents.meaning_agent import MeaningAgent
    from agents.researcher_agent import ResearcherAgent
except ImportError as e:
    st.error(f"Error importing agents: {e}")
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

type_descriptions = {
    'LP': 'Linear Programming',
    'MIP': 'Mixed Integer Programming',
    'NLP': 'Nonlinear Programming',
    'Stochastic': 'Stochastic/Uncertainty',
    'Combinatorial': 'Combinatorial Optimization',
    'Network': 'Network Optimization',
    'Meta-Heuristics': 'Meta-Heuristic Methods',
    'Simulation': 'Simulation-Based Optimization',
    'Scheduling': 'Scheduling/Timetabling',
    'Routing': 'Routing/Path Optimization',
    'Assignment': 'Assignment/Matching',
    'Inventory': 'Inventory/Stock Optimization',
    'Portfolio': 'Portfolio/Financial Optimization',
    'GameTheory': 'Game Theory/Strategic',
    'Robust': 'Robust Optimization',
    'Dynamic': 'Dynamic/Sequential Optimization',
    'MultiObjective': 'Multi-Objective Optimization',
    'Unknown': 'Unknown Type'
}

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
        # st.markdown("---")
        # st.markdown("### 📋 Problem Summary")
        
        # Problem type and objective
        # problem_type = problem_data.get('problem_type', 'Unknown')
        # Buscar descrição do tipo, se disponível
        # type_desc = type_descriptions.get(problem_type, 'Unknown Type')
        # sense = problem_data.get('sense', 'maximize')
        # objective = problem_data.get('objective', '')
        # objective_desc = problem_data.get('objective_description', '')
        
        # st.markdown(f"**Problem Type:** {problem_type}, {type_desc}")
        # st.markdown(f"**Objective:** {sense} {objective}")
        # if objective_desc:
        #     st.markdown(f"**Description:** {objective_desc}")
        
        # Decision Variables
        # if decision_vars:
        #     st.markdown("**Decision Variables:**")
        #     for var_name, var_info in decision_vars.items():
        #         var_type = var_info.get('type', 'Unknown')
        #         var_desc = var_info.get('description', 'No description')
        #         bounds = var_info.get('bounds', [])
        #         bounds_str = f" [{bounds[0]}, {bounds[1] if bounds[1] is not None else '∞'}]" if bounds else ""
        #         st.markdown(f"• **{var_name}** ({var_type}){bounds_str}: {var_desc}")
        
        # Auxiliary Variables
        # if auxiliary_vars:
        #     st.markdown("**Auxiliary Variables:**")
        #     for var_name, var_info in auxiliary_vars.items():
        #         var_type = var_info.get('type', 'Unknown')
        #         var_desc = var_info.get('description', 'No description')
        #         equation = var_info.get('equation', 'No equation')
        #         st.markdown(f"• **{var_name}** ({var_type}): {var_desc} = {equation}")
        
        # Constraints
        # constraints = problem_data.get('constraints', [])
        # if constraints:
        #     st.markdown(f"**Constraints ({len(constraints)}):**")
        #     for i, constraint in enumerate(constraints, 1):
        #         expression = constraint.get('expression', 'No expression')
        #         description = constraint.get('description', 'No description')
        #         constraint_type = constraint.get('type', 'Unknown')
        #         st.markdown(f"{i}. **{expression}** ({constraint_type}): {description}")
        
        # Mostrar o campo data
        # data = problem_data.get('data', {})
        # if data:
        #     st.markdown("**Data:**")
        #     st.json(data)
        
        # st.markdown("---")
        # st.info("💡 **Please review the problem summary above. If everything looks correct, you can proceed to processing. If you need any adjustments, continue the conversation with the Meaning Agent.**")

def build_problem_summary_markdown(problem_data):
    """Gera um markdown completo do resumo do problema para exibir no chat, sem o Business Context."""
    if not problem_data:
        return ""
    
    # Construir o markdown do summary
    md_lines = ["### 📋 Problem Summary", ""]  # Linha vazia após título
    
    # Problem type and objective
    problem_type = problem_data.get('problem_type', 'Unknown')
    type_desc = type_descriptions.get(problem_type, 'Unknown Type')
    sense = problem_data.get('sense', 'maximize')
    objective = problem_data.get('objective', '')
    objective_desc = problem_data.get('objective_description', '')
    
    md_lines.append(f"**Problem Type:** {problem_type} ({type_desc})")
    md_lines.append(f"**Objective:** {sense.title()} {objective}")
    if objective_desc:
        md_lines.append(f"**Description:** {objective_desc}")
    
    md_lines.append("")  # Linha vazia antes das variáveis
    
    # Decision Variables
    decision_vars = problem_data.get('decision_variables', {})
    if decision_vars:
        md_lines.append(f"**Decision Variables ({len(decision_vars)}):**")
        for var_name, var_info in decision_vars.items():
            var_type = var_info.get('type', 'Unknown')
            var_desc = var_info.get('description', 'No description')
            bounds = var_info.get('bounds', [])
            bounds_str = f" [{bounds[0]}, {bounds[1] if bounds[1] is not None else '∞'}]" if bounds else ""
            md_lines.append(f"• **{var_name}** ({var_type}){bounds_str}: {var_desc}")
    else:
        md_lines.append(f"**Decision Variables (0):** None")
    
    md_lines.append("")  # Linha vazia antes das variáveis auxiliares
    
    # Auxiliary Variables - sempre mostrar, mesmo que vazio
    auxiliary_vars = problem_data.get('auxiliary_variables', {})
    if auxiliary_vars:
        md_lines.append(f"**Auxiliary Variables ({len(auxiliary_vars)}):**")
        for var_name, var_info in auxiliary_vars.items():
            var_type = var_info.get('type', 'Unknown')
            var_desc = var_info.get('description', 'No description')
            equation = var_info.get('equation', 'No equation')
            md_lines.append(f"• **{var_name}** ({var_type}): {var_desc} = {equation}")
    else:
        md_lines.append(f"**Auxiliary Variables (0):** None")
    
    md_lines.append("")  # Linha vazia antes das restrições
    
    # Constraints
    constraints = problem_data.get('constraints', [])
    if constraints:
        md_lines.append(f"**Constraints ({len(constraints)}):**")
        for i, constraint in enumerate(constraints, 1):
            expression = constraint.get('expression', 'No expression')
            description = constraint.get('description', 'No description')
            constraint_type = constraint.get('type', 'Unknown')
            md_lines.append(f"{i}. **{expression}** ({constraint_type}): {description}")
    else:
        md_lines.append(f"**Constraints (0):** None")
    
    # Business Context - manter apenas dados técnicos
    business_context = problem_data.get('business_context', {})
    if business_context:
        domain = business_context.get('domain', 'Unknown')
        if domain != 'Unknown':
            md_lines.append("")  # Linha vazia antes do domain
            md_lines.append(f"**Domain:** {domain}")
    
    md_lines.extend(["", "---", ""])  # Linhas vazias antes e depois do separador
    md_lines.append("💡 **Review the problem summary above. If everything looks correct, click 'Start Structure Analysis' to proceed.**")
    
    return '\n'.join(md_lines)

def compile_user_messages(chat_messages):
    """Compila todas as mensagens do usuário em uma string única."""
    user_messages = []
    for msg in chat_messages:
        if msg.get('sender') == 'user':
            user_messages.append(msg.get('message', ''))
    
    if not user_messages:
        return 'No user input found'
    
    # Juntar as mensagens com numeração
    compiled = []
    for i, message in enumerate(user_messages, 1):
        compiled.append(f"{i}. {message}")
    
    return '\n'.join(compiled)

def main():
    """New Job Page - Interactive chat with Meaning Agent (simplified)"""
    
    # Authentication check
    try:
        name, username = require_auth()
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.stop()

    # Detectar se esta é uma nova sessão (primeiro acesso à página ou cache limpo)
    # Se não existe 'chat_messages' no session_state, significa que é uma nova sessão
    is_new_session = 'chat_messages' not in st.session_state
    
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
    
    # Adicionar botão "Start Fresh" se já existe uma conversa em andamento
    if not is_new_session and st.session_state.get('chat_messages'):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 Start Fresh (Clear Chat)", type="secondary", use_container_width=True):
                clear_chat_cache()
                st.rerun()
    
    # Initialize session state for chat
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
        st.session_state.meaning_agent = None
        st.session_state.researcher_agent = None
        st.session_state.problem_ready = False
        st.session_state.final_problem_data = None
        st.session_state.refined_problem_data = None
        st.session_state.pipeline_stage = "meaning"  # meaning, researcher, processing
        st.session_state.pipeline_complete = False
    
    # Initialize Agents
    if st.session_state.meaning_agent is None:
        try:
            st.session_state.meaning_agent = MeaningAgent()
            st.session_state.researcher_agent = ResearcherAgent()
            # Add welcome message
            if not st.session_state.chat_messages:
                st.session_state.chat_messages.append({
                    'sender': 'assistant',
                    'message': "Hi! I'm the Meaning Agent. I'm here to help you define optimization problems. Just tell me what you want to optimize and I'll help you structure it step by step. What would you like to work on?"
                })
        except Exception as e:
            st.error(f"Failed to initialize agents: {e}")
            st.stop()
    
    st.divider()

    # Pipeline stage indicator
    if st.session_state.pipeline_stage == "meaning":
        st.markdown("""
        <div class="problem-input-section">
            <h3 style="text-align: center; margin-bottom: 1.5rem;">💬 Chat with Meaning Agent</h3>
            <p style="text-align: center; font-size: 1.1rem;">
                Just describe your optimization problem below. The agent will help you structure it and remember our conversation.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Botões de ação no topo
    col1, col2 = st.columns([1, 3])
    with col1:
        if st.button("🏠 Back to Home", use_container_width=True):
            st.switch_page("pages/a_Home.py")

    # Chat interface
    for idx, message in enumerate(st.session_state.chat_messages):
        with st.chat_message(message['sender']):
            # Renderizar a mensagem
            st.markdown(message['message'], unsafe_allow_html=False)
            
            # FLUXO 1: Se é um Problem Summary do Meaning Agent e ainda não foi para o Researcher
            if (message['message'].startswith('### 📋 Problem Summary') and
                message['sender'] == 'assistant' and
                st.session_state.problem_ready and
                st.session_state.refined_problem_data is None and
                idx == len(st.session_state.chat_messages) - 1):
                
                # Mostrar dados se existirem
                if (st.session_state.final_problem_data and 
                    st.session_state.final_problem_data.get('data')):
                    with st.expander('Data', expanded=False):
                        st.json(st.session_state.final_problem_data['data'])
                
                st.markdown("---")
                # BOTÃO 1: Start Structure (chama Researcher Agent)
                if st.button('🔧 Start Structure Analysis', type='primary', key=f'start_structure_{idx}'):
                    st.session_state.chat_messages.append({
                        'sender': 'assistant',
                        'message': '🔍 Researcher Agent is now analyzing and refining your problem...'
                    })
                    
                    with st.spinner("🔍 Research Agent is analyzing problem structure..."):
                        try:
                            researcher_result = st.session_state.researcher_agent.refine_problem(st.session_state.final_problem_data)
                            if researcher_result.get('success', False):
                                refined_data = researcher_result.get('result', {})
                                st.session_state.refined_problem_data = refined_data
                                
                                # Criar mensagem detalhada do Researcher Agent
                                researcher_message = '✅ Problem structure analysis complete!\n\n'
                                improvements = refined_data.get('improvements', [])
                                if improvements:
                                    researcher_message += '**Improvements Made:**\n'
                                    for i, improvement in enumerate(improvements, 1):
                                        researcher_message += f'{i}. {improvement}\n'
                                    researcher_message += '\n'
                                
                                missing_data = refined_data.get('missing_data', [])
                                if missing_data:
                                    researcher_message += '**Missing Data Identified:**\n'
                                    for i, missing in enumerate(missing_data, 1):
                                        researcher_message += f'{i}. {missing}\n'
                                    researcher_message += '\n'
                                
                                clarification_requests = refined_data.get('clarification_requests', [])
                                if clarification_requests:
                                    researcher_message += '**Clarification Requests:**\n'
                                    for i, request in enumerate(clarification_requests, 1):
                                        researcher_message += f'{i}. {request}\n'
                                    researcher_message += '\n'
                                
                                researcher_message += 'Your problem structure is now validated and ready for optimization!'
                                
                                st.session_state.chat_messages.append({
                                    'sender': 'assistant',
                                    'message': researcher_message
                                })
                                
                                # Adicionar Summary Structured Problem
                                # O Research Agent retorna uma estrutura com 'refined_problem' dentro
                                refined_problem_data = refined_data.get('refined_problem', refined_data)
                                
                                # DEBUG: Comparar dados originais vs refinados
                                print(f"🔍 ORIGINAL OBJECTIVE: {st.session_state.final_problem_data.get('objective', 'N/A')}")
                                print(f"🔍 REFINED OBJECTIVE: {refined_problem_data.get('objective', 'N/A')}")
                                
                                structured_summary = build_problem_summary_markdown(refined_problem_data)
                                if structured_summary:
                                    # Substituir o título para "Summary Structured Problem"
                                    structured_summary = structured_summary.replace('### 📋 Problem Summary', '### 📋 Summary Structured Problem')
                                    st.session_state.chat_messages.append({
                                        'sender': 'assistant',
                                        'message': structured_summary
                                    })
                            else:
                                st.session_state.chat_messages.append({
                                    'sender': 'assistant',
                                    'message': f'❌ Error in structure analysis: {researcher_result.get("error", "Unknown error")}'
                                })
                        except Exception as e:
                            st.session_state.chat_messages.append({
                                'sender': 'assistant',
                                'message': f'❌ Error processing with Researcher Agent: {str(e)}'
                            })
                    st.rerun()
            
            # FLUXO 2: Se é a última mensagem do Researcher Agent (problema refinado)
            elif (message['sender'] == 'assistant' and 
                  idx == len(st.session_state.chat_messages) - 1 and
                  st.session_state.refined_problem_data and 
                  not st.session_state.pipeline_complete and
                  (message['message'].startswith('### 📋 Summary Structured Problem') or
                   'refined_problem' in st.session_state.refined_problem_data)):
                
                # Mostrar dados refinados se existirem
                refined_problem_data = st.session_state.refined_problem_data.get('refined_problem', st.session_state.refined_problem_data)
                if refined_problem_data and refined_problem_data.get('data'):
                    with st.expander('Data (Refined)', expanded=False):
                        st.json(refined_problem_data['data'])
                
                st.markdown("---")
                # BOTÃO 2: Start (executa pipeline completo)
                if st.button("🚀 Start Optimization", type="primary", key=f"start_optimization_{idx}"):
                    # Marcar pipeline como iniciado
                    st.session_state.pipeline_complete = True
                    
                    # Executar pipeline com spinners individuais para cada agente
                    with st.spinner("📐 Mathematician Agent is generating the mathematical model..."):
                        import time
                        time.sleep(2)  # Simular processamento
                        st.session_state.chat_messages.append({
                            'sender': 'assistant',
                            'message': "📐 **Mathematician Agent** built the mathematical formulation successfully!"
                        })
                    
                    with st.spinner("💻 Formulator Agent is generating Pyomo code..."):
                        time.sleep(2)  # Simular processamento
                        st.session_state.chat_messages.append({
                            'sender': 'assistant',
                            'message': "💻 **Formulator Agent** generated the Pyomo code successfully!"
                        })
                    
                    with st.spinner("⚡ Executor Agent is running the optimization model..."):
                        time.sleep(3)  # Simular processamento mais longo
                        st.session_state.chat_messages.append({
                            'sender': 'assistant',
                            'message': "⚡ **Executor Agent** ran the optimization model successfully!"
                        })
                    
                    with st.spinner("📊 Interpreter Agent is analyzing the results..."):
                        time.sleep(2)  # Simular processamento
                        st.session_state.chat_messages.append({
                            'sender': 'assistant',
                            'message': "📊 **Interpreter Agent** analyzed the results successfully!"
                        })
                    
                    with st.spinner("🔍 Auditor Agent is validating the solution..."):
                        time.sleep(2)  # Simular processamento
                        st.session_state.chat_messages.append({
                            'sender': 'assistant',
                            'message': "🔍 **Auditor Agent** validated the solution successfully!"
                        })
                    
                    # Mensagem final de conclusão
                    st.session_state.chat_messages.append({
                        'sender': 'assistant',
                        'message': "✅ **Optimization pipeline completed successfully!** All agents have finished their work."
                    })
                    
                    # Salvar no banco de dados
                    jobs_db = db.get_jobs()
                    next_id = str(len(jobs_db) + 1).zfill(3)
                    now = datetime.datetime.now()
                    date_str = now.strftime('%Y%m%d-%H:%M:%S')
                    job_title = st.session_state.final_problem_data.get('business_context', {}).get('domain', 'OptimizationJob')
                    job_id = f"job_{next_id}_{date_str}_{job_title.replace(' ', '_')}"
                    
                    # Resultado final para salvar no banco
                    final_message = """✅ Optimization complete! Here are your results:

🎯 **Optimal Solution Found:**
• Optimal Value: $1,200
• x = 15 units  
• y = 5 units

📈 **Performance Metrics:**
• Solver: CBC
• Execution Time: 0.05 seconds
• Status: Optimal
• Iterations: 3

📊 **Business Insights:**
• Maximum profit achieved at capacity limit
• Product X is more profitable (5 vs 3)
• Solution uses 100% of available capacity
• No slack in constraints

🔍 **Model Details:**
• Problem Type: Linear Programming (LP)
• Variables: 2 decision variables
• Constraints: 3 (1 capacity + 2 non-negativity)
• Objective: Maximize 5x + 3y

Your optimization problem has been successfully solved! 🎉"""
                    
                    db.insert_job({
                        'id': job_id,
                        'created_at': now.isoformat(),
                        'user_input': compile_user_messages(st.session_state.chat_messages),
                        'job_title': job_title,
                        'status': 'Completed',
                        'final_message': final_message,
                    })
                    
                    # Salvar conversas e outputs
                    for msg in st.session_state.chat_messages:
                        db.insert_conversation(job_id, msg['sender'], msg['message'], now.isoformat())
                    
                    db.insert_agent_output(job_id, 'Meaning', json.dumps(st.session_state.final_problem_data), now.isoformat())
                    db.insert_agent_output(job_id, 'Researcher', json.dumps(st.session_state.refined_problem_data), now.isoformat())
                    db.insert_agent_output(job_id, 'Mathematician', json.dumps({'output': 'Fake model output'}), now.isoformat())
                    db.insert_agent_output(job_id, 'Formulator', json.dumps({'output': 'Fake code output'}), now.isoformat())
                    db.insert_agent_output(job_id, 'Executor', json.dumps({'output': 'Fake execution output'}), now.isoformat())
                    db.insert_agent_output(job_id, 'Interpreter', json.dumps({'output': 'Fake analysis output'}), now.isoformat())
                    db.insert_agent_output(job_id, 'Auditor', json.dumps({'output': 'Fake validation output'}), now.isoformat())
                    
                    # Salvar job_id para acessar na página de resultados
                    st.session_state.current_job_id = job_id
                    
                    # Recarregar a página para mostrar as novas mensagens
                    st.rerun()
            
            # FLUXO 3: Se é a mensagem final do pipeline completo (mostrar botão Ver Resultados)
            elif (message['sender'] == 'assistant' and 
                  idx == len(st.session_state.chat_messages) - 1 and
                  st.session_state.pipeline_complete and
                  'Optimization pipeline completed successfully' in message['message'] and
                  hasattr(st.session_state, 'current_job_id')):
                
                st.markdown("---")
                # BOTÃO 3: Ver Resultados (vai para página de resultados)
                if st.button("📊 Ver Resultados", type="primary", key=f"view_results_{idx}"):
                    # Limpar jobs da session_state e navegar para resultados
                    st.session_state['jobs'] = []
                    st.switch_page('pages/e_Results.py')
    
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
                    agent_result = st.session_state.meaning_agent.process(prompt)
                    # print('DEBUG agent_result:', agent_result)
                    clarification = agent_result.get('clarification')
                    if not clarification and 'result' in agent_result:
                        clarification = agent_result['result'].get('clarification')
                    problem_data = agent_result.get('result', agent_result)
                    is_valid = problem_data.get('is_valid_problem', False)
                    # Adiciona primeiro a mensagem de feedback textual
                    if clarification:
                        st.session_state.chat_messages.append({
                            'sender': 'assistant',
                            'message': clarification
                        })
                    else:
                        st.session_state.chat_messages.append({
                            'sender': 'assistant',
                            'message': '[ERRO] Não foi possível extrair a mensagem de clarification do Meaning Agent.'
                        })
                    # Só mostra o summary se o problema for válido
                    if is_valid:
                        summary_md = build_problem_summary_markdown(problem_data)
                        if summary_md:
                            st.session_state.chat_messages.append({
                                'sender': 'assistant',
                                'message': summary_md
                            })
                            # Atualiza o estado global com o último problem_data válido
                            st.session_state.final_problem_data = problem_data
                            st.session_state.problem_ready = True
                        else:
                            st.session_state.chat_messages.append({
                                'sender': 'assistant',
                                'message': '[ERRO] Não foi possível gerar o summary do problema.'
                            })
                    st.rerun()
                except Exception as e:
                    st.session_state.chat_messages.append({
                        'sender': 'assistant',
                        'message': f"Erro ao processar: {e}"
                    })
                    st.rerun()

if __name__ == "__main__":
    main() 