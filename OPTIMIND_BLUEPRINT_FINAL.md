# OptiMind - Blueprint Arquitetural Completo

## 📋 Resumo Executivo

O **OptiMind** é uma plataforma de otimização assistida por IA que transforma descrições em linguagem natural de problemas de otimização em soluções matemáticas completas, código executável e insights de negócio. A arquitetura utiliza um pipeline multi-agente orquestrado pelo PraisonAI, com interface Streamlit e modelagem Pyomo.

---

## 🏗️ 1. Arquitetura Geral

### 1.1 Visão de Alto Nível

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Streamlit UI  │───▶│  PraisonAI       │───▶│   Pyomo +       │
│   (Frontend)    │    │  (Orquestrador)  │    │   Solvers       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Autenticação  │    │  7 Agentes       │    │   Resultados    │
│   + Segurança   │    │  Especializados  │    │   + Insights    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### 1.2 Componentes Principais

1. **Interface de Usuário (Streamlit)**
   - Chat interativo para entrada de problemas ✅ **IMPLEMENTADO**
   - Timeline de progresso do pipeline
   - Visualização de resultados e insights
   - Sistema de autenticação ✅ **IMPLEMENTADO**

2. **Orquestrador Multi-Agente (PraisonAI)**
   - Pipeline sequencial de 7 agentes especializados
   - Sistema MCP (MetaController Planner) com MetaManager
   - Validação de schemas JSON em cada etapa ✅ **IMPLEMENTADO**
   - Mecanismos de retry e fallback

3. **Motor de Otimização (Pyomo)**
   - Geração automática de código Pyomo
   - Execução em sandbox seguro
   - Suporte a solvers open-source (CBC, GLPK, HiGHS)

4. **Camada de Segurança**
   - Autenticação robusta com senhas seguras (bcrypt) ✅ **IMPLEMENTADO**
   - Validação de força de senha (12+ chars, maiúsculas, minúsculas, números, símbolos) ✅ **IMPLEMENTADO**
   - Rate limiting de login (5 tentativas por IP, bloqueio de 5 minutos) ✅ **IMPLEMENTADO**
   - Proteção de chaves API via `st.secrets` ✅ **IMPLEMENTADO**
   - Execução sandboxed de código
   - Logs de tentativas de login ✅ **IMPLEMENTADO**
   - Arquivos sensíveis protegidos (.gitignore) ✅ **IMPLEMENTADO**

---

## 🤖 2. Pipeline de Agentes

### 2.1 Estrutura dos 7 Agentes

| Agente | Função | Entrada | Saída | Validação | Status |
|--------|--------|---------|-------|-----------|--------|
| **Meaning** ✅ **IMPLEMENTADO** | Valida e interpreta input do usuário | Texto natural | JSON com `is_valid_problem` | Schema básico | ✅ Completo |
| **Pesquisador** | Refina e estrutura o problema | JSON do Meaning | `refined_problem.json` | `problem_schema.json` | 🔄 Próximo |
| **Matemático** | Gera modelo matemático formal | JSON refinado | LaTeX + `model.json` | `model_schema.json` | 🔄 Próximo |
| **Formulador** | Cria código Pyomo | Modelo matemático | Código Python | `code_schema.json` | 🔄 Próximo |
| **Executor** | Executa modelo em sandbox | Código Pyomo | Resultados do solver | `result_schema.json` | 🔄 Próximo |
| **Interpretador** | Analisa e interpreta resultados | Resultados + modelo | Insights de negócio | `insight_schema.json` | 🔄 Próximo |
| **Auditor** | Valida todo o pipeline | Todos os outputs | Aprovação ou retry | Schemas + lógica | 🔄 Próximo |

### 2.2 Meaning Agent - Implementação Completa ✅

#### 2.2.1 Funcionalidades Implementadas
- **Interpretação conversacional**: Responde de forma amigável e natural
- **Contexto de chat**: Mantém histórico de conversas para construir problemas passo a passo
- **Política de não-invenção**: Nunca inventa dados, só estrutura o que o usuário fornece
- **Campo `data` obrigatório**: Todos os parâmetros, tabelas, valores são capturados neste campo
- **Validação de schema**: Toda saída é validada contra `problem_schema.json`
- **Tratamento de mensagens casuais**: Responde amigavelmente a saudações sem tentar estruturar problemas
- **Separação de variáveis**: Distingue claramente variáveis de decisão e auxiliares
- **Equações para auxiliares**: Captura expressões matemáticas que definem variáveis auxiliares

#### 2.2.2 Prompt Otimizado (`prompts/meaning.txt`)
```json
{
  "problem_type": "LP|MIP|NLP|Stochastic|Combinatorial|Network|Meta-Heuristics|Unknown",
  "sense": "maximize|minimize", 
  "objective": "mathematical expression",
  "objective_description": "description in English",
  "decision_variables": {
    "variable_name": {
      "type": "Real|Integer|Binary",
      "description": "variable description",
      "bounds": [min, max]
    }
  },
  "auxiliary_variables": {
    "variable_name": {
      "type": "Real|Integer|Binary",
      "description": "auxiliary variable description",
      "equation": "expression in terms of decision variables"
    }
  },
  "constraints": [
    {
      "expression": "mathematical expression",
      "description": "constraint description",
      "type": "inequality|equality|bound"
    }
  ],
  "data": {
    "parameter_name": "value or list or table",
    "another_parameter": "..."
  },
  "is_valid_problem": true/false,
  "confidence": 0.0-1.0,
  "clarification": "your friendly response to the user",
  "business_context": {
    "domain": "problem domain",
    "stakeholders": ["stakeholder1", "stakeholder2"],
    "constraints": ["constraint1", "constraint2"]
  }
}
```

#### 2.2.3 Integração com Interface (`pages/d_NewJob.py`)
- **Chat interativo**: Interface de conversa natural com o Meaning Agent
- **Resumo do problema**: Exibe métricas e estrutura quando `is_valid_problem: true`
- **Exemplos de problemas**: Problemas pré-definidos para facilitar o input
- **Validação visual**: Mostra tipo de problema, confiança, variáveis, restrições
- **Continuidade**: Permite continuar a conversa para ajustar ou adicionar dados

#### 2.2.4 Testes Robustos (`tests/test_all_problems.py`)
- **Teste automatizado completo**: Valida todos os 22 problemas do acervo real
- **Testes de casos clássicos**: LP simples, com variáveis auxiliares, minimização
- **Testes de contexto**: Construção passo a passo de problemas
- **Testes de mensagens casuais**: Respostas amigáveis a saudações
- **Validação de schema**: Toda saída é validada contra o schema JSON
- **Testes de consistência**: Verificação de dados financeiros e unidades
- **Acervo TOML estruturado**: `prompts/problem_list.toml` com problemas reais
- **Relatório detalhado**: Estatísticas de sucesso/falha para cada problema
- **Interface CLI**: Suporte a teste individual ou em lote

### 2.3 Sistema MCP (MetaController Planner)

```yaml
# Exemplo de configuração MCP (flows/optimind_flow.yml)
- id: understand_problem
  agent: Meaning
  goal: problem_understood
  condition: is_input_valid
  on_fail:
    retry_agent: Meaning
    max_retries: 2
    fallback: ask_user_clarification

- id: refine_problem
  agent: Pesquisador
  goal: problem_refined
  condition: is_refined_json_valid
  on_fail:
    retry_agent: Meaning
    max_retries: 1

- id: mathematical_model
  agent: Matemático
  goal: model_created
  condition: is_model_json_valid
  on_fail:
    retry_agent: Pesquisador
    max_retries: 2

- id: code_generation
  agent: Formulador
  goal: code_generated
  condition: is_python_code_valid
  on_fail:
    retry_agent: Matemático
    max_retries: 1

- id: execution
  agent: Executor
  goal: solution_found
  condition: is_solver_optimal
  on_fail:
    retry_agent: Formulador
    max_retries: 1
    alternative_solver: true

- id: interpretation
  agent: Interpretador
  goal: insights_generated
  condition: is_insight_complete
  on_fail:
    retry_agent: Interpretador
    max_retries: 1

- id: audit
  agent: Auditor
  goal: pipeline_approved
  condition: all_stages_valid
  on_fail:
    retry_from: context.retry_from
    max_retries: 1
```

### 2.4 Comunicação entre Agentes

Todos os agentes se comunicam via mensagens JSON estruturadas:

```json
{
  "message_id": "msg-123",
  "sender": "Meaning",
  "recipient": "Pesquisador",
  "type": "PROBLEM_REFINED",
  "timestamp": "2024-01-15T10:30:00Z",
  "content": {
    "description": "Maximize profit from products A and B",
    "objective": "100*x + 150*y",
    "variables": {
      "x": {"type": "Real", "bounds": [0, 100]},
      "y": {"type": "Real", "bounds": [0, 50]}
    },
    "constraints": ["x + 2*y <= 100"]
  }
}
```

---

## 🎨 3. Experiência do Usuário (Streamlit)

### 3.1 Fluxo de Navegação

```
LOGIN → HOME → NOVO JOB → DEFINIÇÃO → REVISÃO → TIMELINE → RESULTADOS
```

### 3.2 Páginas Principais

#### 3.2.1 Página de Login ✅ **IMPLEMENTADO**
```python
# app.py - Login com sistema de segurança robusto
from utils.auth import require_auth, logout

# Verificar autenticação com rate limiting e validação
name, username = require_auth()

# Sistema de logout
if st.sidebar.button("🚪 Logout"):
    logout()
    st.rerun()
```

**Características de Segurança:**
- Hash bcrypt com salt automático
- Validação de força de senha (12+ chars, maiúsculas, minúsculas, números, símbolos)
- Rate limiting (5 tentativas por IP, bloqueio de 5 minutos)
- Logs de tentativas de login
- Arquivos sensíveis protegidos (.gitignore)
- Compatibilidade com streamlit-authenticator v0.4.2
- Estrutura correta (cookie_key, session_state)

#### 3.2.2 Home (Lista de Jobs) ✅ **IMPLEMENTADO**
- Botão "Novo Job" proeminente
- Lista de jobs anteriores com metadata
- Filtros por data, status, tipo de problema

#### 3.2.3 Definição de Problema ✅ **IMPLEMENTADO**
```python
# Interface de entrada - Implementada em pages/d_NewJob.py
st.text_area(
    "Descreva seu problema de otimização:",
    placeholder="Ex: Maximizar lucro vendendo produtos A e B...",
    height=400  # Interface adaptativa
)

# Chat interativo com Meaning Agent
if st.button("💬 Enviar"):
    result = meaning_agent.process_problem(user_input)
    if result['success']:
        problem_data = result['result']
        display_problem_summary(problem_data)
```

**Funcionalidades Implementadas:**
- Chat interativo com Meaning Agent
- Resumo visual do problema estruturado
- Exemplos de problemas pré-definidos
- Validação de entrada expandida
- Interface adaptativa e responsiva
- Integração completa com schema JSON

#### 3.2.4 Histórico de Jobs ✅ **IMPLEMENTADO**
- Lista de jobs processados
- Status de cada job
- Filtros e busca
- Detalhes de cada execução

#### 3.2.5 Ferramentas Administrativas ✅ **IMPLEMENTADO**
- Gerenciamento de usuários
- Configurações do sistema
- Logs de segurança
- Monitoramento de uso

---

## 🔧 4. Especificações Técnicas

### 4.1 Stack Tecnológico

| Componente | Tecnologia | Versão | Propósito |
|------------|------------|--------|-----------|
| **Frontend** | Streamlit | 1.28+ | Interface web |
| **Orquestrador** | PraisonAI | Latest | Multi-agente |
| **Modelagem** | Pyomo | 6.8+ | Otimização |
| **Solvers** | CBC, GLPK, HiGHS | Latest | Resolução |
| **LLM** | OpenAI GPT-4o | - | Agentes IA |
| **Validação** | jsonschema | 4.19+ | Schemas JSON |
| **Autenticação** | streamlit-authenticator | Latest | Login |
| **Visualização** | Altair/Matplotlib | Latest | Gráficos |

### 4.2 Estrutura de Arquivos

```
optimind/
├── app.py                          # Aplicação principal Streamlit ✅
├── requirements.txt                # Dependências Python ✅
├── setup_dev_credentials.py        # Gerenciador de credenciais ✅
├── SECURITY.md                     # Credenciais (NÃO commitado) ✅
├── users.json                      # Dados de usuários (NÃO commitado) ✅
└── login_attempts.json             # Logs de segurança (NÃO commitado) ✅
├── README.md                       # Documentação ✅
├── LICENSE                         # Licença (MIT) ✅
├── .streamlit/
│   ├── config.toml                # Configurações Streamlit ✅
│   └── secrets.toml               # Chaves API (não no git) ✅
├── pages/                          # Páginas Streamlit ✅
│   ├── __init__.py                # Inicialização das páginas ✅
│   ├── a_Home.py                  # Página inicial ✅
│   ├── b_AdminTools.py            # Ferramentas administrativas ✅
│   ├── c_UserManagement.py        # Gerenciamento de usuários ✅
│   ├── d_NewJob.py                # Interface de entrada ✅
│   └── e_History.py               # Histórico de jobs ✅
├── agents/                         # Agentes (próximo bloco)
│   ├── __init__.py
│   ├── meaning.py                 # Agente de meaning
│   ├── pesquisador.py             # Agente de pesquisa
│   ├── matematico.py              # Agente matemático
│   ├── formulador.py              # Agente formulador
│   ├── executor.py                # Agente executor
│   ├── interpretador.py           # Agente interpretador
│   ├── auditor.py                 # Agente auditor
│   └── metamanager.py             # MetaManager MCP
├── schemas/                        # Schemas JSON (próximo bloco)
│   ├── problem_schema.json        # Schema do problema
│   ├── model_schema.json          # Schema do modelo
│   ├── code_schema.json           # Schema do código
│   ├── result_schema.json         # Schema dos resultados
│   └── insight_schema.json        # Schema dos insights
├── flows/
│   └── optimind_flow.yml          # Configuração MCP
├── prompts/                        # Prompts (próximo bloco)
│   ├── meaning.txt                # Prompt do agente meaning
│   ├── pesquisador.txt            # Prompt do agente pesquisador
│   ├── matematico.txt             # Prompt do agente matemático
│   ├── formulador.txt             # Prompt do agente formulador
│   └── interpretador.txt          # Prompt do agente interpretador
├── utils/
│   ├── __init__.py                # Inicialização utils ✅
│   ├── auth.py                    # Autenticação ✅
│   ├── sidebar.py                 # Sidebar ✅
│   ├── validators.py              # Funções de validação ✅
│   ├── graph_mcp.py               # Visualização MCP
│   └── helpers.py                 # Funções auxiliares
├── tests/                          # Testes ✅
│   ├── test_app_online.py         # Testes de app online ✅
│   ├── test_auth.py               # Testes de autenticação ✅
│   ├── test_input_interface.py    # Testes da interface de entrada ✅
│   └── test_openai_secrets.py     # Testes de secrets ✅
└── examples/                       # Exemplos (próximo bloco)
    ├── linear_programming.json    # Exemplo LP
    ├── integer_programming.json   # Exemplo MIP
    └── nonlinear_programming.json # Exemplo NLP
```

### 4.3 Schemas JSON

#### 4.3.1 Problem Schema
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "OptimizationProblem",
  "type": "object",
  "required": [
    "problem_type", "sense", "objective", "objective_description",
    "decision_variables", "auxiliary_variables", "constraints", "data",
    "is_valid_problem", "confidence", "clarification", "business_context"
  ],
  "properties": {
    "problem_type": {"enum": ["LP", "MIP", "NLP", "Stochastic", "Unknown"]},
    "sense": {"enum": ["maximize", "minimize"]},
    "objective": {"type": "string"},
    "decision_variables": {
      "type": "object",
      "patternProperties": {
        "^[a-zA-Z][a-zA-Z0-9_]*$": {
          "type": "object",
          "properties": {
            "type": {"enum": ["Real", "Integer", "Binary"]},
            "description": {"type": "string"},
            "bounds": {"type": "array", "items": {"type": ["number", "null"]}}
          },
          "required": ["type", "description"]
        }
      }
    },
    "auxiliary_variables": {
      "type": "object",
      "patternProperties": {
        "^[a-zA-Z][a-zA-Z0-9_]*$": {
          "type": "object",
          "properties": {
            "type": {"enum": ["Real", "Integer", "Binary"]},
            "description": {"type": "string"},
            "equation": {"type": "string"}
          },
          "required": ["type", "description", "equation"]
        }
      }
    },
    "constraints": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "expression": {"type": "string"},
          "description": {"type": "string"},
          "type": {"enum": ["inequality", "equality", "bound"]}
        },
        "required": ["expression", "description"]
      }
    },
    "data": {
      "type": "object",
      "description": "All numerical values, tables, time series, initial values, rates, and parameters needed to solve the problem"
    },
    "is_valid_problem": {"type": "boolean"},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "clarification": {"type": "string"},
    "business_context": {
      "type": "object",
      "properties": {
        "domain": {"type": "string"},
        "stakeholders": {"type": "array", "items": {"type": "string"}},
        "constraints": {"type": "array", "items": {"type": "string"}}
      }
    }
  }
}
```

#### 4.3.2 Model Schema
```json
{
  "type": "object",
  "required": ["objective", "variables", "constraints"],
  "properties": {
    "objective": {
      "type": "string",
      "description": "Função objetivo em formato Pyomo"
    },
    "variables": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "name": {"type": "string"},
          "type": {"enum": ["Real", "Integer", "Binary"]},
          "bounds": {
            "type": "array",
            "items": {"type": ["number", "null"]},
            "minItems": 2,
            "maxItems": 2
          }
        }
      }
    },
    "constraints": {
      "type": "array",
      "items": {"type": "string"}
    }
  }
}
```

### 4.4 Prompts dos Agentes

#### 4.4.1 Agente Meaning
```
SYSTEM: Você é o Agente Meaning do OptiMind.

Sua função é analisar descrições de problemas de otimização em linguagem natural e determinar se são válidos.

INSTRUÇÕES:
1. Identifique se o texto descreve um problema de otimização
2. Extraia o objetivo (maximizar/minimizar)
3. Identifique variáveis e restrições
4. Se não for claro, peça esclarecimentos

SAÍDA: JSON com exatamente estes campos:
{
  "is_valid_problem": boolean,
  "intent": "maximize" | "minimize" | null,
  "clarification": string (vazio se válido),
  "problem_draft": {
    "description": string,
    "variables": object,
    "constraints": array
  }
}

EXEMPLO:
Input: "Quero maximizar lucro vendendo x e y com limite de 100"
Output: {
  "is_valid_problem": true,
  "intent": "maximize",
  "clarification": "",
  "problem_draft": {
    "description": "Maximizar lucro vendendo produtos x e y",
    "variables": {"x": {"type": "Real"}, "y": {"type": "Real"}},
    "constraints": ["x + y <= 100"]
  }
}
```

#### 4.4.2 Agente Matemático
```
SYSTEM: Você é o Agente Matemático do OptiMind.

Sua função é converter problemas de otimização em modelos matemáticos formais.

INSTRUÇÕES:
1. Receba JSON 'refined_problem' validado
2. Gere modelo matemático em LaTeX
3. Produza JSON estruturado do modelo
4. Use notação matemática clara e precisa

SAÍDA: JSON com exatamente estes campos:
{
  "model_json": {
    "objective": string,
    "variables": array,
    "constraints": array
  },
  "latex": string
}

EXEMPLO:
Input: {"objective": "100*x + 150*y", "variables": {...}}
Output: {
  "model_json": {
    "objective": "100*x + 150*y",
    "variables": [{"name": "x", "type": "Real", "bounds": [0, null]}],
    "constraints": ["x + 2*y <= 100"]
  },
  "latex": "\\[ \\max 100x + 150y \\text{ subject to } x + 2y \\le 100, x \\ge 0, y \\ge 0 \\]"
}
```

---

## 🔒 5. Segurança e Autenticação

### 5.1 Proteção de Chaves API

```python
# Configuração segura da OpenAI
import streamlit as st
import openai

# Chave armazenada em secrets (nunca no código)
openai.api_key = st.secrets["OPENAI"]["api_key"]

# Verificação de autenticação
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.error("Acesso não autorizado")
    st.stop()
```

### 5.2 Rate Limiting

```python
# Controle de uso por usuário
def check_rate_limit(user_id):
    if "usage" not in st.session_state:
        st.session_state.usage = {}
    
    if user_id not in st.session_state.usage:
        st.session_state.usage[user_id] = {"calls": 0, "last_reset": time.time()}
    
    # Reset diário
    if time.time() - st.session_state.usage[user_id]["last_reset"] > 86400:
        st.session_state.usage[user_id] = {"calls": 0, "last_reset": time.time()}
    
    # Limite de 50 chamadas por dia
    if st.session_state.usage[user_id]["calls"] >= 50:
        return False
    
    st.session_state.usage[user_id]["calls"] += 1
    return True
```

### 5.3 Execução Sandboxed

```python
# Executor com limites de segurança
from praisonaiagents.tools import CodeInterpreterTool

executor_tool = CodeInterpreterTool(
    timeout=300,  # 5 minutos máximo
    memory_limit="1GB",
    allowed_imports=["pyomo", "numpy", "pandas"],
    blocked_imports=["os", "subprocess", "sys"]
)
```

---

## 🚀 6. Deploy e Hospedagem

### 6.1 Streamlit Community Cloud

#### 6.1.1 Configuração
```toml
# .streamlit/config.toml
[theme]
primaryColor="#020e66"
backgroundColor="#f8fafc"
secondaryBackgroundColor="#c8f0ff"
textColor="#1f2937" 

[server]
maxUploadSize = 200
enableXsrfProtection = true
enableCORS = false

[browser]
gatherUsageStats = false
```

#### 6.1.2 Secrets Management
```toml
# .streamlit/secrets.toml (não commitado)
[OPENAI]
api_key = "sk-..."

[USERS]
admin_password_hash = "$2b$12$..."
user1_password_hash = "$2b$12$..."
```

#### 6.1.3 Limitações e Considerações
- **RAM**: 1GB disponível
- **CPU**: 1 vCPU
- **Storage**: 1GB
- **Timeout**: 60 segundos por request
- **Rate Limit**: 5 deploys por minuto

### 6.2 Alternativas de Hospedagem

| Plataforma | Vantagens | Desvantagens | Custo |
|------------|-----------|--------------|-------|
| **Streamlit Cloud** | Fácil deploy, integrado | Limitações de recursos | Gratuito |
| **Render** | Mais recursos, customizável | Setup mais complexo | Gratuito (com sleep) |
| **Heroku** | Escalável, confiável | Preço após free tier | $7+/mês |
| **AWS EC2** | Controle total, potente | Complexidade DevOps | $10+/mês |

---

## 📊 7. Monitoramento e Logs

### 7.1 Estrutura de Logs

```python
import logging
from datetime import datetime

# Configuração de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('optimind.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_agent_execution(agent_name, input_data, output_data, execution_time):
    logger.info(f"Agent {agent_name} executed in {execution_time:.2f}s")
    logger.debug(f"Input: {input_data}")
    logger.debug(f"Output: {output_data}")
```

### 7.2 Métricas de Performance

```python
# Métricas por job
job_metrics = {
    "job_id": "job_123",
    "user_id": "user_456",
    "start_time": datetime.now(),
    "agent_times": {
        "meaning": 2.3,
        "pesquisador": 1.8,
        "matematico": 3.1,
        "formulador": 2.7,
        "executor": 15.2,
        "interpretador": 1.5,
        "auditor": 0.8
    },
    "total_time": 27.4,
    "api_calls": 7,
    "estimated_cost": 0.023
}
```

---

## 🧪 8. Testes e Validação

### 8.1 Testes Unitários

```python
# tests/test_agents.py
import unittest
from agents.meaning import MeaningAgent
from schemas.problem_schema import problem_schema
from jsonschema import validate

class TestMeaningAgent(unittest.TestCase):
    def setUp(self):
        self.agent = MeaningAgent()
    
    def test_valid_optimization_problem(self):
        input_text = "Maximize profit from products A and B"
        result = self.agent.process(input_text)
        
        # Valida schema
        validate(instance=result, schema=problem_schema)
        
        # Valida lógica
        self.assertTrue(result["is_valid_problem"])
        self.assertEqual(result["intent"], "maximize")
    
    def test_invalid_input(self):
        input_text = "Hello, how are you?"
        result = self.agent.process(input_text)
        
        self.assertFalse(result["is_valid_problem"])
        self.assertNotEqual(result["clarification"], "")
```

### 8.2 Testes de Integração

```python
# tests/test_integration.py
def test_full_pipeline():
    """Testa o pipeline completo com problema simples"""
    
    # Input de teste
    user_input = "Maximize 3x + 4y subject to x + y <= 10, x >= 0, y >= 0"
    
    # Executa pipeline
    result = run_full_pipeline(user_input)
    
    # Validações
    assert result["status"] == "success"
    assert result["objective_value"] == 40.0
    assert result["variables"]["x"] == 0.0
    assert result["variables"]["y"] == 10.0
```

### 8.3 Casos de Teste

| Tipo de Problema | Descrição | Resultado Esperado |
|------------------|-----------|-------------------|
| **LP Simples** | Maximizar 3x + 4y s.t. x + y ≤ 10 | x=0, y=10, obj=40 |
| **MIP** | Maximizar x + y s.t. x + y ≤ 5, x,y ∈ ℤ | x=2, y=3, obj=5 |
| **Inviável** | x + y ≤ 5, x ≥ 10 | Status: infeasible |
| **Ilimitado** | Maximizar x + y | Status: unbounded |

---

## 📈 9. Roadmap de Desenvolvimento

### 9.1 Fase 1 - MVP (4 semanas)
- [x] Setup básico do projeto ✅ **CONCLUÍDO**
- [x] Sistema de autenticação robusto ✅ **CONCLUÍDO**
- [x] Interface Streamlit básica ✅ **CONCLUÍDO**
- [x] Interface de entrada de problemas ✅ **CONCLUÍDO**
- [x] Validação de input expandida ✅ **CONCLUÍDO**
- [x] Suite de testes robusta ✅ **CONCLUÍDO**
- [x] Deploy no Streamlit Cloud ✅ **CONCLUÍDO**
- [ ] Implementação dos 7 agentes básicos
- [ ] Schemas JSON e validação

### 9.2 Fase 2 - Melhorias (2 semanas)
- [ ] Sistema MCP completo
- [ ] Timeline de progresso
- [ ] Autenticação de usuários
- [ ] Logs e monitoramento
- [ ] Testes unitários

### 9.3 Fase 3 - Produção (2 semanas)
- [ ] Otimizações de performance
- [ ] Tratamento robusto de erros
- [ ] Documentação completa
- [ ] Casos de teste abrangentes
- [ ] Deploy em produção

### 9.4 Fase 4 - Expansão (contínuo)
- [ ] Suporte a problemas estocásticos
- [ ] Integração com mais solvers
- [ ] API REST para integração
- [ ] Dashboard de analytics
- [ ] Suporte multi-idioma

---

## 💰 10. Análise de Custos

### 10.1 Custos de Desenvolvimento

| Item | Estimativa | Observações |
|------|------------|-------------|
| **Desenvolvimento** | 8 semanas | 1 desenvolvedor full-time |
| **Infraestrutura** | $0-50/mês | Depende da hospedagem |
| **OpenAI API** | $0.01-0.10/job | ~1000 tokens por job |
| **Manutenção** | 4h/semana | Monitoramento e melhorias |

### 10.2 Otimizações de Custo

1. **Cache de Resultados**: Problemas similares podem reutilizar soluções
2. **Modelos Menores**: Usar GPT-3.5 para tarefas simples
3. **Rate Limiting**: Limitar uso por usuário
4. **Batch Processing**: Processar múltiplos problemas juntos

---

## 🎯 11. Métricas de Sucesso

### 11.1 KPIs Técnicos
- **Taxa de Sucesso**: >95% dos problemas resolvidos corretamente
- **Tempo de Resposta**: <30 segundos para problemas simples
- **Precisão**: >90% de acerto na interpretação de problemas
- **Disponibilidade**: >99% uptime

### 11.2 KPIs de Negócio
- **Adoção**: 100 usuários ativos no primeiro mês
- **Retenção**: >70% de usuários retornam
- **Satisfação**: >4.5/5 rating de usuários
- **Eficiência**: 80% redução no tempo de modelagem

---

## 🔮 12. Considerações Futuras

### 12.1 Expansões Técnicas
- **Modelos Locais**: Integração com Ollama para LLMs locais
- **GPU Support**: Para problemas de otimização complexos
- **Distributed Solving**: Paralelização de problemas grandes
- **Real-time Collaboration**: Múltiplos usuários no mesmo problema

### 12.2 Expansões de Negócio
- **API Enterprise**: Para integração com sistemas existentes
- **Consultoria**: Serviços de implementação e treinamento
- **Marketplace**: Templates de problemas comuns
- **Educação**: Cursos de otimização com OptiMind

---

## 📝 13. Checklist de Implementação

### 13.1 Setup Inicial
- [ ] Criar repositório Git
- [ ] Configurar ambiente virtual Python
- [ ] Instalar dependências básicas
- [ ] Configurar Streamlit
- [ ] Criar estrutura de pastas

### 13.2 Desenvolvimento Core
- [ ] Implementar agentes individuais
- [ ] Criar schemas JSON
- [ ] Implementar sistema MCP
- [ ] Desenvolver interface Streamlit
- [ ] Implementar autenticação

### 13.3 Integração e Testes
- [ ] Integrar pipeline completo
- [ ] Implementar validações
- [ ] Criar testes unitários
- [ ] Testes de integração
- [ ] Testes de performance

### 13.4 Deploy e Produção
- [ ] Configurar secrets
- [ ] Deploy no Streamlit Cloud
- [ ] Configurar monitoramento
- [ ] Documentação final
- [ ] Treinamento de usuários

---

## 📚 14. Referências e Recursos

### 14.1 Documentação Técnica
- [PraisonAI Documentation](https://docs.praison.ai/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pyomo Documentation](https://pyomo.readthedocs.io/)
- [JSON Schema Specification](https://json-schema.org/)

### 14.2 Exemplos e Tutoriais
- [Streamlit Multi-Agent Examples](https://github.com/leporejoseph/PraisonAi-Streamlit)
- [Pyomo Optimization Examples](https://pyomo.readthedocs.io/en/stable/working_models.html)
- [OpenAI API Examples](https://platform.openai.com/examples)

### 14.3 Ferramentas Úteis
- [JSON Schema Validator](https://www.jsonschemavalidator.net/)
- [LaTeX Editor](https://www.overleaf.com/)
- [Streamlit Components](https://docs.streamlit.io/library/api-reference)

---

## ✅ 15. Conclusão

O OptiMind representa uma solução completa e inovadora para democratizar o acesso à otimização matemática. A arquitetura multi-agente, combinada com interface intuitiva e execução segura, oferece:

1. **Acessibilidade**: Consultores não-técnicos podem resolver problemas complexos
2. **Confiabilidade**: Validação rigorosa e tratamento de erros robusto
3. **Escalabilidade**: Arquitetura modular permite expansões futuras
4. **Segurança**: Execução sandboxed e proteção de dados
5. **Custo-efetividade**: Uso eficiente de recursos e APIs

Com este blueprint detalhado, a implementação pode prosseguir de forma sistemática e estruturada, resultando em uma plataforma robusta e profissional para otimização assistida por IA.

---

**Versão**: 1.1  
**Data**: Julho 2025  
**Autor**: Equipe OptiMind  
**Status**: Aprovado para implementação - Bloco 2 concluído 

## Meaning Agent (Atualizado)

O Meaning Agent é um parceiro conversacional que interpreta problemas de otimização em linguagem natural, extraindo:
- Variáveis de decisão
- Variáveis auxiliares
- Restrições
- **Dados do problema** (campo `data`): parâmetros, tabelas, séries temporais, taxas, valores iniciais, etc.

**Política de dados:**
- O agente **nunca inventa ou assume dados**. Ele só estrutura o que o usuário explicitamente forneceu.
- Se faltar algum dado, o agente pede ao usuário.

### Exemplo de JSON extraído
```json
{
  "problem_type": "Stochastic",
  "sense": "minimize",
  "objective": "net_financing_costs",
  ...
  "data": {
    "accounts_receivable": [1.5, 1.0, 1.4, 2.3, 2.0, 2.0],
    "planned_payments": [1.8, 1.6, 2.2, 1.2, 0.8, 1.2],
    "months": ["JAN", "FEB", "MAR", "APR", "MAY", "JUN"],
    "beginning_cash_balance": 0.4,
    "min_cash_balance": 0.25,
    "loan_interest_rate": 0.01,
    "receivable_loan_rate": 0.015,
    "cash_interest_rate": 0.005,
    "payment_discount_loss": 0.02,
    "receivable_loan_limit": 0.75
  },
  ...
}
```

### Fluxo de interação
1. O usuário descreve o problema em linguagem natural, incluindo dados, tabelas, parâmetros, etc.
2. O Meaning Agent estrutura o problema e os dados em JSON.
3. O usuário revisa o problema reescrito e os dados extraídos antes de processar.
4. Se faltar algum dado, o agente pede explicitamente ao usuário.
5. O JSON é passado para os próximos agentes ou módulos de solução.

---

## (Atualize outras seções conforme necessário para refletir o novo fluxo e a presença do campo 'data'.) 