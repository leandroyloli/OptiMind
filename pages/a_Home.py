"""
OptiMind - Home Page
"""

import streamlit as st
from utils.auth import require_auth
from utils.sidebar import create_sidebar

# Page  configuration
st.set_page_config(
    page_title="OptiMind - AI-Powered Optimization by Mirow & Co.",
    page_icon="🧠",
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
</style>
""", unsafe_allow_html=True)

# Sidebar function is now imported from utils.sidebar

def main():
    """OptiMind Home Page"""
    
    # Authentication check
    try:
        name, username = require_auth()
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        st.stop()
    
    # Criar sidebar
    create_sidebar()
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        color: #1f77b4;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px #0000001a;
    }
    .section-header {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
    }
    .golden-circle {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
    }
    .use-case-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .algorithm-section {
        background: #f1f3f4;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
    }
    .tech-solution {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
    }
    .logo-section {
        text-align: center;
        margin-top: 4rem;
        padding: 2rem;
        background: #f8f9fa;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 0. Beautiful centered title
    st.markdown('<h1 class="main-header">🧠 OptiMind</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center; color: #7f8c8d; margin-bottom: 3rem;">AI-Powered Optimization Platform  by Mirow & Co.</h2>', unsafe_allow_html=True)
    
    # 0. Button to go to next page
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start New Optimization Job", type="primary", use_container_width=True, key="new_job_btn"):
            st.switch_page("pages/d_NewJob.py")
    
    st.divider()
    
    # 1. PINPOINT - The Consultant's Pain Points
    st.markdown('<h2 class="section-header">🎯 The Consultants Reality</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%); padding: 2rem; border-radius: 15px; color: white; margin: 2rem 0;">
    <h3 style="text-align: center; margin-bottom: 1.5rem;">🚨 The Growing Pressure on Consultants</h3>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>⏰ Time Pressure</h4>
            <p>Clients need solutions yesterday. Traditional optimization takes weeks of PhD-level expertise.</p>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🎯 Complexity Gap</h4>
            <p>Business problems are complex, but mathematical modeling requires specialized knowledge.</p>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🚀 Innovation Demand</h4>
            <p>Clients increasingly demand cutting-edge, innovative, and complex solutions to stay competitive.</p>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>📊 Communication Gap</h4>
            <p>Clients speak business language. Optimization experts speak mathematics. Translation is expensive.</p>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
   
    # 3. RESOLUTION - The OptiMind Solution
    st.markdown('<h2 class="section-header">🎯 The OptiMind Resolution</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); padding: 2rem; border-radius: 15px; color: white; margin: 2rem 0;">
    <h3 style="text-align: center; margin-bottom: 1.5rem;">🤖 Your AI Optimization Partner</h3>
    
    <div style="text-align: center; font-size: 1.2rem; line-height: 1.8;">
    <p><strong>OptiMind is an AI agent that helps consultants build the best possible solution for each specific problem.</strong></p>
    <p>We transform complex PhD-level optimization into simple, understandable business solutions.</p>
    <p>Making consultants' lives simpler to deliver more value to clients using knowledge that was once only available to PhD experts.</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 4. Industry Use Cases
    st.markdown('<h2 class="section-header">🏭 Industry Use Cases</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); padding: 2rem; border-radius: 15px; color: white; margin: 2rem 0;">
    <h3 style="text-align: center; margin-bottom: 2rem;">🎯 Real-World Applications Across Industries</h3>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem;">
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🏭 Manufacturing</h4>
            <ul style="margin: 1rem 0; line-height: 1.6;">
                <li>Production scheduling optimization</li>
                <li>Supply chain management</li>
                <li>Inventory control systems</li>
                <li>Quality control optimization</li>
            </ul>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🚚 Logistics & Transportation</h4>
            <ul style="margin: 1rem 0; line-height: 1.6;">
                <li>Vehicle routing optimization</li>
                <li>Fleet management</li>
                <li>Warehouse layout design</li>
                <li>Delivery scheduling</li>
            </ul>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>💰 Financial Services</h4>
            <ul style="margin: 1rem 0; line-height: 1.6;">
                <li>Portfolio optimization</li>
                <li>Risk management</li>
                <li>Asset allocation</li>
                <li>Trading strategy optimization</li>
            </ul>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🏥 Healthcare</h4>
            <ul style="margin: 1rem 0; line-height: 1.6;">
                <li>Staff scheduling optimization</li>
                <li>Resource allocation</li>
                <li>Patient flow management</li>
                <li>Medical supply optimization</li>
            </ul>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🛒 Retail & E-commerce</h4>
            <ul style="margin: 1rem 0; line-height: 1.6;">
                <li>Pricing optimization</li>
                <li>Inventory management</li>
                <li>Store layout design</li>
                <li>Marketing campaign optimization</li>
            </ul>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>⚡ Energy & Utilities</h4>
            <ul style="margin: 1rem 0; line-height: 1.6;">
                <li>Power grid optimization</li>
                <li>Energy distribution</li>
                <li>Renewable energy planning</li>
                <li>Maintenance scheduling</li>
            </ul>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 5. Simple Interface, PhD-Level Power
    st.markdown('<h2 class="section-header">🎯 Simple Interface, PhD-Level Power</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%); padding: 2rem; border-radius: 15px; color: white; margin: 2rem 0;">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">👤 What Users See</h3>
        <ul style="font-size: 1.1rem; line-height: 1.8;">
        <li>📝 Natural language problem description</li>
        <li>✅ Simple confirmation of understanding</li>
        <li>⏱️ Real-time progress updates</li>
        <li>📊 Clear business insights and recommendations</li>
        <li>🎯 Optimized solution delivery</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #8e44ad 0%, #9b59b6 100%); padding: 2rem; border-radius: 15px; color: white; margin: 2rem 0;">
        <h3 style="text-align: center; margin-bottom: 1.5rem;">🧠 What Happens Inside</h3>
        <ul style="font-size: 1.1rem; line-height: 1.8;">
        <li>🤖 7 AI agents working in sequence</li>
        <li>📚 Advanced LLM models (GPT-4)</li>
        <li>🔬 PhD-level mathematical modeling</li>
        <li>⚙️ Multiple optimization engines (CPLEX, Gurobi)</li>
        <li>📊 Statistical analysis and validation</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 6. PhD-Level Problems, Simple Solutions
    st.markdown('<h2 class="section-header">🔬 PhD-Level Problems, Simple Solutions</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #f39c12 0%, #e67e22 100%); padding: 2rem; border-radius: 15px; color: white; margin: 2rem 0;">
    <h3 style="text-align: center; margin-bottom: 1.5rem;">🎓 Complex Mathematical Challenges We Solve</h3>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem; margin-bottom: 1.5rem;">
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>📐 Mixed Integer Programming</h4>
            <p>Problems with both continuous and discrete variables - traditionally requiring months of PhD-level expertise.</p>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🎲 Stochastic Optimization</h4>
            <p>Uncertainty modeling with probability distributions - advanced operations research techniques.</p>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🎯 Multi-Objective Optimization</h4>
            <p>Pareto frontier analysis - balancing conflicting objectives simultaneously.</p>
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🧩 Combinatorial Optimization</h4>
            <p>NP-hard problems like vehicle routing and facility location - requiring specialized algorithms.</p>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>🌐 Network Optimization</h4>
            <p>Flow optimization, shortest paths, and transportation problems for network efficiency.</p>
        </div>
        <div style="background: #ffffff1a; padding: 1.5rem; border-radius: 10px;">
            <h4>⚡ Meta-Heuristics</h4>
            <p>Genetic algorithms, simulated annealing, and other advanced search methods for complex problems.</p>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 7. Technical Architecture
    st.markdown('<h2 class="section-header">🏗️ Technical Architecture</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; color: white; margin: 2rem 0;">
    <h4 style="text-align: center; margin-bottom: 1.5rem;">Sequential Processing Pipeline</h4>
    
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; margin-bottom: 1rem;">
        <div style="text-align: center; flex: 1; margin: 0.5rem;">
            <div style="background: #ffffff33; padding: 1rem; border-radius: 10px;">
                <strong>🧠 Meaning Agent</strong><br>
                Interprets natural language and extracts mathematical structure
            </div>
        </div>
        <div style="text-align: center; flex: 1; margin: 0.5rem;">
            <div style="background: #ffffff33; padding: 1rem; border-radius: 10px;">
                <strong>🔍 Research Agent</strong><br>
                Identifies suitable optimization algorithms and techniques
            </div>
        </div>
        <div style="text-align: center; flex: 1; margin: 0.5rem;">
            <div style="background: #ffffff33; padding: 1rem; border-radius: 10px;">
                <strong>📊 Mathematical Agent</strong><br>
                Formulates precise mathematical models and constraints
            </div>
        </div>
        <div style="text-align: center; flex: 1; margin: 0.5rem;">
            <div style="background: #ffffff33; padding: 1rem; border-radius: 10px;">
                <strong>💻 Formulation Agent</strong><br>
                Converts mathematical models into executable code
            </div>
        </div>
        <div style="text-align: center; flex: 1; margin: 0.5rem;">
            <div style="background: #ffffff33; padding: 1rem; border-radius: 10px;">
                <strong>⚙️ Execution Agent</strong><br>
                Runs optimization algorithms and generates solutions
            </div>
        </div>
        <div style="text-align: center; flex: 1; margin: 0.5rem;">
            <div style="background: #ffffff33; padding: 1rem; border-radius: 10px;">
                <strong>📈 Interpretation Agent</strong><br>
                Translates results into business insights and recommendations
            </div>
        </div>
    </div>
    
    <div style="display: flex; justify-content: center; align-items: center; margin-top: 1rem;">
        <div style="text-align: center; max-width: 300px;">
            <div style="background: #ffffff33; padding: 1rem; border-radius: 10px;">
                <strong>👁️ Auditor Agent</strong><br>
                Orchestrates and validates all other agents' outputs
            </div>
        </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    
    # 8. Democratization Message
    st.markdown('<h2 class="section-header">🌍 Democratizing Advanced Optimization</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); padding: 3rem; border-radius: 15px; color: white; margin: 2rem 0; text-align: center;">
    <h3 style="margin-bottom: 2rem; font-size: 2rem;">🎓 From PhD-Level to Everyone</h3>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin: 2rem 0;">
        <div style="background: #ffffff1a; padding: 2rem; border-radius: 10px;">
            <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">💪 Empowering Consultants</h4>
            <p style="font-size: 1.2rem;">From dependency to autonomy</p>
            <p style="font-size: 1rem; opacity: 0.9;">Consultants become optimization experts themselves</p>
        </div>
        <div style="background: #ffffff1a; padding: 2rem; border-radius: 10px;">
            <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">⏰ Time Reduction</h4>
            <p style="font-size: 1.2rem;">From months to hours</p>
            <p style="font-size: 1rem; opacity: 0.9;">95% faster solution delivery</p>
        </div>
        <div style="background: #ffffff1a; padding: 2rem; border-radius: 10px;">
            <h4 style="font-size: 1.5rem; margin-bottom: 1rem;">👥 Accessibility</h4>
            <p style="font-size: 1.2rem;">From PhD experts to business analysts</p>
            <p style="font-size: 1rem; opacity: 0.9;">Democratizing advanced mathematics</p>
        </div>
    </div>
    
    <div style="margin-top: 3rem; padding: 2rem; background: #ffffff1a; border-radius: 10px;">
    <h4 style="font-size: 1.8rem; margin-bottom: 1rem;">🚀 The Future of Optimization</h4>
    <p style="font-size: 1.3rem; line-height: 1.6;">
    We're making PhD-level optimization accessible to everyone. No more waiting months for solutions. 
    No more complex mathematical jargon. Just describe your problem in plain English and get world-class solutions in hours.
    </p>
    </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    
    # 9. Logo section at the end
    # st.markdown('<div class="logo-section">', unsafe_allow_html=True)
    
    # Mirow Labs Logo 
    col1, col2, col3 = st.columns([3, 1, 3])
    
    with col1:
        # Empty space
        st.write("")
    
    with col2:
        # Mirow Labs Logo centered
        try:
            st.image("logoMirow.png", width=200, use_container_width=False)
        except:
            st.markdown("""
            <h2 style="text-align: center; color: #2c3e50; margin-bottom: 1rem;">Powered by Mirow Labs</h2>
            """, unsafe_allow_html=True)
    
    with col3:
        # Empty space
        st.write("")
    
    st.markdown("""
    <p style="text-align: center; color: #7f8c8d; font-size: 1.1rem;">
    Solving Real Business Problems with advanced Mathematical Solutions
    </p>
    <p style="text-align: center; color: #95a5a6; margin-top: 2rem;">
    © 2025 | OptiMind - AI-Powered Optimization Platform
    </p>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main() 