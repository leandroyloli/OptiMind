# OptiMind - Contexto Essencial para Desenvolvimento

## 🎯 Propósito

Este documento contém **contexto essencial** que não está nos outros MDs mas é crucial para continuar o desenvolvimento do OptiMind. Se você está retomando o projeto, leia este documento **antes** dos outros.

## 🚀 Atualização UX/UI e Persistência (2025-07) ✅ **COMPLETAMENTE IMPLEMENTADO**

- **Novo fluxo de chat**: ✅ O usuário interage com o Meaning Agent em um chat, recebe sugestões/refinamentos do Researcher Agent, e vê mensagens de todos os agentes do pipeline no histórico do chat.
- **Pipeline semi-manual**: ✅ Só há um clique necessário para processar o pipeline completo ("Start Optimization"), o resto é automático.
- **Mensagens de todos os agentes**: ✅ Cada etapa do pipeline (Meaning, Researcher, Mathematician, Formulator, Executor, Interpreter, Auditor) aparece como mensagem no chat, com histórico completo.
- **Página de resultados dedicada**: ✅ Após o processamento, o usuário é redirecionado para uma página de resultados, com expanders (toggles) **colapsados por padrão** para cada agente mostrando o JSON de saída.
- **Página de histórico**: ✅ Mostra todos os jobs em um DataFrame filtrável (usando `dataframe_explorer` do pacote streamlit-extras), permitindo busca, seleção múltipla, etc. Selecionar um job mostra a mesma visualização da página de resultados.
- **Persistência em banco SQLite**: ✅ Todos os jobs, conversas e outputs dos agentes são salvos em um banco SQLite (`optimind.db`) com **3 tabelas estruturadas**.
- **ID de job**: ✅ Cada job recebe um ID único no formato `job_{id}_{AAAAMMDD-HH:MM:SS}_{titulo}`.
- **Integração total**: ✅ O pipeline, histórico e resultados estão totalmente integrados, com **navegação fluida via sidebar funcional**.
- **Filtros inteligentes**: ✅ O histórico usa o `dataframe_explorer` para filtros avançados e intuitivos.
- **Compilação de entrada do usuário**: ✅ **Campo `user_input` compila TODAS as mensagens do usuário** em formato numerado para contexto completo.
- **Interface otimizada**: ✅ Botões redundantes removidos, expanders colapsados, informações desnecessárias (created_at) removidas.

### 🗄️ **Banco de Dados SQLite - Estrutura Completa** ✅ **IMPLEMENTADO**

```python
# 3 Tabelas principais em optimind.db
def init_db():
    # 1. jobs - Metadados principais
    '''CREATE TABLE IF NOT EXISTS jobs (
        id TEXT PRIMARY KEY,                    # job_001_20250107-14:30:25_ProductionPlanning
        created_at TEXT,                        # 2025-01-07T14:30:25.123456
        user_input TEXT,                        # "1. I want to maximize profit\n2. We have products A and B"
        job_title TEXT,                         # "Production Planning"
        status TEXT,                            # "Completed"
        final_message TEXT                      # Resultado final formatado
    )'''
    
    # 2. conversations - Histórico completo do chat
    '''CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   # 1, 2, 3...
        job_id TEXT,                           # Referência ao job
        sender TEXT,                           # "user" ou "assistant"
        message TEXT,                          # Conteúdo da mensagem
        timestamp TEXT                         # Quando foi enviada
    )'''
    
    # 3. agent_outputs - Saídas JSON dos agentes
    '''CREATE TABLE IF NOT EXISTS agent_outputs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,   # 1, 2, 3...
        job_id TEXT,                           # Referência ao job
        agent_name TEXT,                       # "Meaning", "Researcher", etc.
        json_output TEXT,                      # Saída JSON estruturada
        timestamp TEXT                         # Quando foi gerada
    )'''
```

### 📊 **Compilação Inteligente de Mensagens do Usuário** ✅ **IMPLEMENTADO**

```python
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

# Exemplo de saída:
# "1. I want to maximize profit
#  2. We have products A and B  
#  3. Product A costs $5, Product B costs $3
#  4. We have capacity constraint of 100 units"
```

### 🎨 **Melhorias de UX/UI Implementadas** ✅ **IMPLEMENTADO**

#### 1. **Sidebar Funcional em Todas as Páginas**
```python
# utils/sidebar.py - Implementação completa
def create_sidebar():
    # Navegação principal
    if st.sidebar.button("🏠 Home", use_container_width=True, type="primary"):
        st.switch_page("pages/a_Home.py")
    
    if st.sidebar.button("🚀 New Job", use_container_width=True):
        st.switch_page("pages/d_NewJob.py")
    
    if st.sidebar.button("📊 Results", use_container_width=True):
        st.switch_page("pages/e_Results.py")
    
    if st.sidebar.button("📜 History", use_container_width=True):
        st.switch_page("pages/f_History.py")
```

#### 2. **Interface Limpa e Organizada**
- ✅ **Expanders colapsados**: Todos os agent outputs começam `expanded=False`
- ✅ **Botões redundantes removidos**: "Go to History", "Latest Results" eliminados
- ✅ **Informações desnecessárias removidas**: Campo "created_at" removido das visualizações
- ✅ **Navegação contextual**: Botão "Ver Resultados" aparece apenas quando apropriado

#### 3. **Histórico com Filtros Avançados**
```python
# pages/f_History.py - Implementação do dataframe_explorer
from streamlit_extras.dataframe_explorer import dataframe_explorer

def main():
    st.title('📜 Optimization Job History')
    jobs = db.get_jobs()
    df = pd.DataFrame([{
        'ID': job['id'],
        'Title': job['job_title'],
        'Status': job['status'],
    } for job in jobs])
    
    filtered_df = dataframe_explorer(df)  # Filtros inteligentes
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
```

### 🔄 **Fluxo Completo do Pipeline** ✅ **IMPLEMENTADO**

1. **Entrada do Usuário**: Chat interativo com Meaning Agent
2. **Análise do Meaning**: Estruturação em JSON validado
3. **Refinamento**: Researcher Agent aprimora o problema
4. **Pipeline Automático**: Um clique executa todos os agentes subsequentes
5. **Salvamento Completo**: Job, conversas, e outputs salvos no SQLite
6. **Visualização**: Botão "Ver Resultados" aparece automaticamente
7. **Histórico**: Acesso a todos os jobs com filtros avançados

### Exemplo de tela do histórico:
```python
from streamlit_extras.dataframe_explorer import dataframe_explorer
filtered_df = dataframe_explorer(df)
st.dataframe(filtered_df)
```

---

## 🏗️ Decisões Arquiteturais Fundamentais

### 1. Por que PraisonAI?
- **Escolhido sobre LangChain**: PraisonAI tem integração nativa com Streamlit e suporte a multi-agentes mais robusto
- **Vantagens**: Sandbox automático, ferramentas integradas, menos boilerplate
- **Alternativa considerada**: AutoGen (mais complexo) ou LangGraph (mais verboso)

### 2. Por que 7 Agentes Específicos?
- **Meaning** ✅ **IMPLEMENTADO**: Separação clara entre input humano e processamento
- **Pesquisador**: Necessário para problemas complexos que precisam de refinamento
- **Matemático**: Gera tanto LaTeX quanto JSON estruturado
- **Formulador**: Especializado em Pyomo, escolhe solver automaticamente
- **Executor**: Sandbox separado por segurança
- **Interpretador**: Traduz resultados técnicos para insights de negócio
- **Auditor**: Meta-agente que valida todo o pipeline

### 3. Por que JSON Schemas Rígidos? ✅ **IMPLEMENTADO**
- **Problema**: LLMs às vezes geram JSON inválido ou inconsistente
- **Solução**: Validação rigorosa em cada etapa
- **Benefício**: Detecta erros cedo, permite retry automático
- **Implementação**: `schemas/problem_schema.json` com validação completa

### 4. Por que Acervo TOML e Teste Automatizado? ✅ **IMPLEMENTADO**
- **Problema**: Testes com exemplos artificiais não validam robustez real
- **Solução**: Acervo de 22 problemas reais em TOML + teste automatizado
- **Benefício**: Validação contra problemas reais, curadoria contínua, reprodutibilidade
- **Implementação**: `prompts/problem_list.toml` + `tests/test_all_problems.py`

### 5. Por que Sistema de Autenticação Robusto? ✅ **IMPLEMENTADO**
- **Problema**: Aplicações web precisam de segurança contra ataques
- **Solução**: Autenticação com senhas seguras, rate limiting, validação de força
- **Benefício**: Proteção contra força bruta, credenciais seguras, logs de segurança

---

## 🔧 Padrões de Implementação

### 1. Estrutura de Agentes ✅ **IMPLEMENTADO**
```python
# Padrão para todos os agentes
class BaseAgent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = OpenAI(model="gpt-4o-mini")  # Usar modelo menor para custo
    
    def process(self, input_data):
        # 1. Validar input
        # 2. Chamar LLM
        # 3. Validar output
        # 4. Retornar resultado
        pass

class MeaningAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Meaning",
            system_prompt=load_prompt("meaning.txt")
        )
        self.chat_history = []  # Contexto de conversa
    
    def process_problem(self, user_input, objective=None):
        # Adiciona contexto de chat
        self.chat_history.append({"sender": "user", "message": user_input})
        
        # Constrói prompt com histórico
        full_prompt = self.build_prompt_with_context()
        
        # Processa e valida
        result = self.llm.generate(full_prompt)
        validated_result = self.validate_output(result)
        
        # Adiciona resposta ao histórico
        self.chat_history.append({"sender": "assistant", "message": validated_result})
        
        return {"success": True, "result": validated_result}
```

### 2. Padrão de Comunicação ✅ **IMPLEMENTADO**
```python
# Todas as mensagens seguem este formato
message = {
    "message_id": generate_uuid(),
    "sender": agent_name,
    "recipient": next_agent_name,
    "type": message_type,
    "timestamp": datetime.now().isoformat(),
    "content": validated_json_data
}

# Meaning Agent já implementa este padrão
# Próximos agentes seguirão a mesma estrutura
```

### 3. Padrão de Validação ✅ **IMPLEMENTADO**
```python
# Para cada etapa
def validate_stage_output(output, schema):
    try:
        jsonschema.validate(instance=output, schema=schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, str(e)

# Implementado em schemas/validator.py
# Meaning Agent usa validação rigorosa contra problem_schema.json
```

### 4. Padrão de Autenticação Segura ✅ **IMPLEMENTADO**
```python
# Sistema de autenticação com múltiplas camadas de segurança
class AuthManager:
    def __init__(self):
        self.max_attempts = 5  # Rate limiting
        self.lockout_duration = 300  # 5 minutos
    
    def validate_password_strength(self, password):
        # Validação: 12+ chars, maiúsculas, minúsculas, números, símbolos
        pass
    
    def is_ip_blocked(self, ip_address):
        # Verifica se IP está bloqueado por tentativas excessivas
        pass

# Estrutura compatível com streamlit-authenticator v0.4.2
authenticator = stauth.Authenticate(
    credentials=credentials,
    cookie_name="optimind_cookie",
    cookie_key="abcdef",  # v0.4.2 usa cookie_key
    location="main",
    cookie_expiry_days=30
)
```

### 5. Padrão de Interface de Entrada ✅ **IMPLEMENTADO**
```python
# Interface de entrada com validação expandida
def validate_problem_input(text, objective):
    """Validação local antes de enviar para agente"""
    errors = []
    
    # Validações básicas
    if not text.strip():
        errors.append("Descrição do problema não pode estar vazia")
    
    # Validação de palavras-chave
    keywords = ["maximizar", "minimizar", "maximize", "minimize"]
    if not any(keyword in text.lower() for keyword in keywords):
        errors.append("Adicione 'maximizar' ou 'minimizar' ao seu problema")
    
    # Validação de restrições de negócio
    business_constraints = ["at least", "maintain", "balance", "pelo menos", "manter", "equilibrar"]
    if any(constraint in text.lower() for constraint in business_constraints):
        # Restrições de negócio detectadas - OK
        pass
    
    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "suggestions": generate_suggestions(text, objective)
    }

# Interface implementada em pages/d_NewJob.py
st.text_area(
    "Descreva seu problema de otimização:",
    placeholder="Ex: Maximizar lucro vendendo produtos A e B...",
    height=400  # Interface adaptativa
)
```

### 6. Padrão de Teste Automatizado ✅ **IMPLEMENTADO**
```python
# Teste automatizado para todos os problemas do acervo
def test_meaning_agent_on_all_problems():
    """Testa o Meaning Agent com todos os problemas"""
    problems = load_problems()  # Carrega prompts/problem_list.toml
    agent = MeaningAgent()
    
    for problem in problems:
        response = agent.process_problem(problem['description'])
        is_valid, validation_errors = validate_problem_output(response)
        
        if not is_valid:
            # Registra falha com detalhes
            failed_problems.append({
                'title': problem['title'],
                'errors': validation_errors,
                'response': response
            })
    
    # Relatório final com estatísticas
    print(f"✅ Sucessos: {successful_tests}/{total_tests}")
    print(f"❌ Falhas: {failed_tests}/{total_tests}")

# Uso: python tests/test_all_problems.py --all
# Uso: python tests/test_all_problems.py --problem "Título do Problema"
```

**Benefícios do teste automatizado:**
- **Validação contra problemas reais**: Não apenas exemplos artificiais
- **Curadoria contínua**: Novos problemas são automaticamente testados
- **Reprodutibilidade**: Mesmos problemas, mesmos resultados
- **Detecção de regressões**: Mudanças no agente são validadas automaticamente
- **Relatório detalhado**: Estatísticas e erros específicos por problema

---

## 🎨 Decisões de UX/UI

### 1. Fluxo de Usuário ✅ **IMPLEMENTADO**
- **Por que confirmação obrigatória?**: Evita processamento desnecessário e custos
- **Por que timeline visual?**: Transparência do processo, confiança do usuário
- **Por que JSON colapsável?**: Técnicos podem ver detalhes, leigos não se confundem
- **Por que chat interativo?**: Conversa natural com Meaning Agent para construção passo a passo

### 2. Tratamento de Erros ✅ **IMPLEMENTADO**
- **Nunca mostrar stack trace**: Sempre mensagens amigáveis
- **Sugestões específicas**: "Tente adicionar 'maximizar' ou 'minimizar' ao seu problema"
- **Retry automático**: Se possível, sem intervenção do usuário
- **Política de não-invenção**: Meaning Agent nunca inventa dados, pede esclarecimentos

### 3. Loading States ✅ **IMPLEMENTADO**
- **Spinners específicos**: Cada agente tem seu próprio indicador
- **Tempo estimado**: Mostrar progresso baseado em experiência
- **Cancelamento**: Permitir parar em qualquer momento
- **Feedback conversacional**: Meaning Agent responde de forma amigável e natural

---

## 🔒 Decisões de Segurança

### 1. Sandbox de Execução
```python
# Pyomo roda em container isolado
executor_config = {
    "timeout": 300,  # 5 minutos
    "memory_limit": "1GB",
    "allowed_imports": ["pyomo", "numpy", "pandas"],
    "blocked_imports": ["os", "subprocess", "sys", "requests"]
}
```

### 2. Rate Limiting ✅ **IMPLEMENTADO**
- **Por usuário**: 50 chamadas por dia
- **Por sessão**: 10 chamadas por hora
- **Por IP**: 100 chamadas por dia (backup)
- **Por login**: 5 tentativas por IP, bloqueio de 5 minutos

### 3. Proteção de Dados ✅ **IMPLEMENTADO**
- **Nenhum dado persistido**: Tudo em session_state
- **Logs anonimizados**: Sem dados pessoais
- **Chaves nunca expostas**: Apenas no backend
- **Senhas hasheadas**: bcrypt com salt automático
- **Arquivos sensíveis**: users.json, login_attempts.json, SECURITY.md não commitados

---

## 💰 Decisões de Custo

### 1. Modelos LLM ✅ **IMPLEMENTADO**
```python
# Meaning Agent usa gpt-4o-mini para custo otimizado
# Prompt otimizado para clareza e brevidade
# Contexto de chat limitado para evitar tokens excessivos

# Configuração atual
llm_config = {
    "model": "gpt-4o-mini",  # Mais barato que gpt-4
    "max_tokens": 2000,      # Limite para controle de custo
    "temperature": 0.1       # Baixa para consistência
}
```

### 2. Otimizações de Prompt ✅ **IMPLEMENTADO**
- **Prompt conciso**: Instruções claras e diretas
- **Exemplos específicos**: Ancoram comportamento do agente
- **Validação local**: Reduz chamadas desnecessárias
- **Contexto limitado**: Histórico de chat controlado

### 3. Cache e Reutilização
- **Cache de prompts**: Evita regeneração desnecessária
- **Reutilização de contexto**: Mantém histórico relevante
- **Validação local**: Reduz chamadas à API

---

## 🤖 Meaning Agent - Implementação Completa ✅

### 1. Funcionalidades Principais ✅ **IMPLEMENTADO**

#### 1.1 Interpretação Conversacional
```python
# O agente responde de forma amigável e natural
# Exemplo de resposta a saudações:
{
  "is_valid_problem": false,
  "clarification": "Hi there! 👋 I'm the Meaning Agent and I'm here to help you define optimization problems. What would you like to optimize today?"
}
```

#### 1.2 Contexto de Chat ✅ **IMPLEMENTADO**
```python
# Mantém histórico de conversas
self.chat_history = [
    {"sender": "user", "message": "I want to maximize profit"},
    {"sender": "assistant", "message": "Great! What products are you considering?"},
    {"sender": "user", "message": "Products A and B"},
    # ... continua construindo o problema passo a passo
]
```

#### 1.3 Política de Não-Invenção ✅ **IMPLEMENTADO**
```python
# Regra fundamental: nunca inventa dados
# Se faltar informação, pede explicitamente:
{
  "clarification": "I see you want to minimize cost. What's the cost function you want to minimize? And are there any constraints on production or resources?"
}
```

#### 1.4 Campo `data` Obrigatório ✅ **IMPLEMENTADO**
```python
# Todos os parâmetros, tabelas, valores são capturados
"data": {
    "accounts_receivable": [1.5, 1.0, 1.4, 2.3, 2.0, 2.0],
    "planned_payments": [1.8, 1.6, 2.2, 1.2, 0.8, 1.2],
    "loan_interest_rate": 0.01,
    "receivable_loan_rate": 0.015,
    # ... todos os dados fornecidos pelo usuário
}
```

### 2. Integração com Interface ✅ **IMPLEMENTADO**

#### 2.1 Chat Interativo (`pages/d_NewJob.py`)
```python
# Interface de conversa natural
if st.button("💬 Enviar"):
    result = meaning_agent.process_problem(user_input)
    if result['success']:
        problem_data = result['result']
        display_problem_summary(problem_data)
```

#### 2.2 Resumo Visual
```python
# Exibe métricas e estrutura quando problema é válido
if problem_data.get('is_valid_problem', False):
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
```

### 3. Testes Robustos ✅ **IMPLEMENTADO**

#### 3.1 Casos de Uso Clássicos
```python
def test_meaning_agent():
    # Teste de problema LP simples
    result = agent.process_problem("Maximize profit: 3x + 4y subject to x + y <= 10")
    assert result['success'] == True
    assert result['result']['problem_type'] == 'LP'
    assert result['result']['is_valid_problem'] == True
```

#### 3.2 Testes de Contexto
```python
def test_chat_context():
    # Construção passo a passo
    agent.process_problem("I want to maximize profit")
    agent.process_problem("The variables are x and y")
    result = agent.process_problem("The objective is 3x + 4y")
    assert len(result['result']['decision_variables']) == 2
```

#### 3.3 Testes de Mensagens Casuais
```python
def test_casual_messages():
    # Respostas amigáveis a saudações
    result = agent.process_problem("Hello")
    assert result['result']['is_valid_problem'] == False
    assert "friendly" in result['result']['clarification'].lower()
```

---

## 📋 Status Atual do Projeto

### ✅ Blocos Concluídos

#### Bloco 1: Fundação Básica ✅ **CONCLUÍDO**
- Autenticação robusta com segurança completa
- Interface Streamlit funcional
- Deploy no Streamlit Cloud
- Suite de testes abrangente

#### Bloco 2: Interface de Entrada ✅ **CONCLUÍDO**
- Formulário de entrada de problemas
- Navegação entre páginas
- Validação de input expandida
- Estado da aplicação gerenciado

#### Bloco 3: Meaning Agent e Schemas ✅ **CONCLUÍDO**
- **Schema JSON completo** com validação rigorosa
- **Meaning Agent implementado** com todas as funcionalidades
- **Integração com interface** de chat interativo
- **Testes robustos** cobrindo todos os casos de uso
- **Política de não-invenção** de dados
- **Contexto de chat** para construção passo a passo
- **Tratamento de mensagens casuais**
- **Campo `data` obrigatório** para todos os parâmetros

### 🔄 Próximos Blocos

#### Bloco 4: Pesquisador Agent
- Refinamento de problemas complexos
- Estruturação adicional de dados
- Validação de consistência

#### Bloco 5: Matemático Agent
- Geração de modelos matemáticos formais
- Output em LaTeX
- Validação de expressões matemáticas

---

## 🎯 Próximos Passos Imediatos

### 1. Implementar Pesquisador Agent
```python
# Estrutura base já definida
class PesquisadorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Pesquisador",
            system_prompt=load_prompt("pesquisador.txt")
        )
    
    def refine_problem(self, meaning_output):
        # Recebe JSON do Meaning Agent
        # Refina e estrutura o problema
        # Retorna JSON validado
        pass
```

### 2. Criar Schema para Problemas Refinados
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "RefinedOptimizationProblem",
  "type": "object",
  "required": [
    "original_problem", "refined_problem", "improvements", "confidence"
  ],
  "properties": {
    "original_problem": {"$ref": "#/definitions/OptimizationProblem"},
    "refined_problem": {"$ref": "#/definitions/OptimizationProblem"},
    "improvements": {"type": "array", "items": {"type": "string"}},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1}
  }
}
```

### 3. Integrar no Pipeline
```python
# Fluxo: Meaning → Pesquisador → Matemático
def process_optimization_pipeline(user_input):
    # 1. Meaning Agent
    meaning_result = meaning_agent.process_problem(user_input)
    if not meaning_result['success']:
        return meaning_result
    
    # 2. Pesquisador Agent
    pesquisador_result = pesquisador_agent.refine_problem(meaning_result['result'])
    if not pesquisador_result['success']:
        return pesquisador_result
    
    # 3. Próximos agentes...
    return {"success": True, "pipeline": [meaning_result, pesquisador_result]}
```

---

## 🔧 Configuração de Desenvolvimento

### 1. Ambiente Local
```bash
# Clone e setup
git clone <repository>
cd OptiMind
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt

# Configurar secrets
python setup_dev_credentials.py

# Executar
streamlit run app.py
```

### 2. Testes
```bash
# Todos os testes
python run_tests.py

# Testes específicos
python -m pytest tests/test_meaning_agent.py
python -m pytest tests/test_auth.py
```

### 3. Deploy
```bash
# Deploy no Streamlit Cloud
# Configurar secrets na interface web
# Deploy automático via Git
```

---

*Este documento reflete o estado atual do OptiMind com o Bloco 3 (Meaning Agent e Schemas) completamente implementado e funcional.* 