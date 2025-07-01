# OptiMind - Contexto Essencial para Desenvolvimento

## 🎯 Propósito

Este documento contém **contexto essencial** que não está nos outros MDs mas é crucial para continuar o desenvolvimento do OptiMind. Se você está retomando o projeto, leia este documento **antes** dos outros.

---

## 🏗️ Decisões Arquiteturais Fundamentais

### 1. Por que PraisonAI?
- **Escolhido sobre LangChain**: PraisonAI tem integração nativa com Streamlit e suporte a multi-agentes mais robusto
- **Vantagens**: Sandbox automático, ferramentas integradas, menos boilerplate
- **Alternativa considerada**: AutoGen (mais complexo) ou LangGraph (mais verboso)

### 2. Por que 7 Agentes Específicos?
- **Meaning**: Separação clara entre input humano e processamento
- **Pesquisador**: Necessário para problemas complexos que precisam de refinamento
- **Matemático**: Gera tanto LaTeX quanto JSON estruturado
- **Formulador**: Especializado em Pyomo, escolhe solver automaticamente
- **Executor**: Sandbox separado por segurança
- **Interpretador**: Traduz resultados técnicos para insights de negócio
- **Auditor**: Meta-agente que valida todo o pipeline

### 3. Por que JSON Schemas Rígidos?
- **Problema**: LLMs às vezes geram JSON inválido ou inconsistente
- **Solução**: Validação rigorosa em cada etapa
- **Benefício**: Detecta erros cedo, permite retry automático

### 4. Por que Sistema de Autenticação Robusto?
- **Problema**: Aplicações web precisam de segurança contra ataques
- **Solução**: Autenticação com senhas seguras, rate limiting, validação de força
- **Benefício**: Proteção contra força bruta, credenciais seguras, logs de segurança

---

## 🔧 Padrões de Implementação

### 1. Estrutura de Agentes
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
```

### 2. Padrão de Comunicação
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
```

### 3. Padrão de Validação
```python
# Para cada etapa
def validate_stage_output(output, schema):
    try:
        jsonschema.validate(instance=output, schema=schema)
        return True, None
    except jsonschema.ValidationError as e:
        return False, str(e)
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

---

## 🎨 Decisões de UX/UI

### 1. Fluxo de Usuário
- **Por que confirmação obrigatória?**: Evita processamento desnecessário e custos
- **Por que timeline visual?**: Transparência do processo, confiança do usuário
- **Por que JSON colapsável?**: Técnicos podem ver detalhes, leigos não se confundem

### 2. Tratamento de Erros
- **Nunca mostrar stack trace**: Sempre mensagens amigáveis
- **Sugestões específicas**: "Tente adicionar 'maximizar' ou 'minimizar' ao seu problema"
- **Retry automático**: Se possível, sem intervenção do usuário

### 3. Loading States
- **Spinners específicos**: Cada agente tem seu próprio indicador
- **Tempo estimado**: Mostrar progresso baseado em experiência
- **Cancelamento**: Permitir parar em qualquer momento

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

### 2. Rate Limiting
- **Por usuário**: 50 chamadas por dia
- **Por sessão**: 10 chamadas por hora
- **Por IP**: 100 chamadas por dia (backup)
- **Por login**: 5 tentativas por IP, bloqueio de 5 minutos

### 3. Proteção de Dados
- **Nenhum dado persistido**: Tudo em session_state
- **Logs anonimizados**: Sem dados pessoais
- **Chaves nunca expostas**: Apenas no backend
- **Senhas hasheadas**: bcrypt com salt automático
- **Arquivos sensíveis**: users.json, login_attempts.json, SECURITY.md não commitados

---

## 💰 Decisões de Custo

### 1. Modelos LLM
- **GPT-4o-mini**: Para agentes simples (Meaning, Pesquisador)
- **GPT-4o**: Para agentes complexos (Matemático, Formulador)
- **Custo estimado**: $0.01-0.10 por job completo

### 2. Otimizações
- **Cache de prompts**: Evitar regeneração
- **Batch processing**: Se possível, processar múltiplos problemas
- **Modelos menores**: Para validações simples

### 3. Monitoramento de Custos
```python
# Rastrear custos por usuário
def track_cost(user_id, tokens_used, model):
    cost = calculate_cost(tokens_used, model)
    update_user_usage(user_id, cost)
    if cost > daily_limit:
        block_user(user_id)
```

---

## 🧪 Decisões de Testes

### 1. Casos de Teste Essenciais ✅ **IMPLEMENTADO**
```python
# Problemas que DEVEM funcionar
test_cases = [
    "Maximize 3x + 4y subject to x + y <= 10",  # LP simples
    "Minimize cost where x + y >= 5, x,y integer",  # MIP
    "Maximize profit with x <= 100, y <= 50",  # LP com bounds
    "Invalid input: Hello world",  # Deve ser rejeitado
    "Maximize x + y with x + y <= 5, x >= 10",  # Inviável
]

# Testes implementados em tests/test_input_interface.py
# 16 testes cobrindo:
# - Validação de input vazio
# - Validação de palavras-chave
# - Validação de restrições de negócio
# - Casos extremos e edge cases
# - Tipos de retorno das funções
```

### 2. Validação de Schemas
- **Teste cada schema**: Com dados válidos e inválidos
- **Teste edge cases**: JSON vazio, campos faltando, tipos errados
- **Teste performance**: Schemas não devem demorar >1s

### 3. Testes de Integração
- **Pipeline completo**: Do input ao resultado
- **Erro handling**: Cada ponto de falha
- **Performance**: Tempo total <30s

---

## 🚀 Decisões de Deploy

### 1. Streamlit Community Cloud
- **Limitações conhecidas**: 1GB RAM, 1 vCPU, 60s timeout
- **Adaptações necessárias**: Usar modelos menores, otimizar memória
- **Alternativas**: Render, Heroku se necessário

### 2. Secrets Management
```toml
# .streamlit/secrets.toml (não no git)
[OPENAI]
api_key = "sk-..."

[USERS]
admin_password_hash = "$2b$12$..."
user1_password_hash = "$2b$12$..."

[LIMITS]
max_calls_per_day = 50
max_calls_per_hour = 10
```

### 3. Monitoramento
- **Logs estruturados**: Para debugging
- **Métricas básicas**: Uso, erros, performance
- **Alertas**: Se custo > limite ou erros > threshold

---

## 🔄 Padrões de Retry e Fallback

### 1. Estratégia de Retry
```python
# Para cada agente
def execute_with_retry(agent, input_data, max_retries=2):
    for attempt in range(max_retries):
        try:
            result = agent.process(input_data)
            if validate_result(result):
                return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(1)  # Backoff simples
```

### 2. Fallback de Solvers
```python
# Se CBC falha, tentar GLPK
solver_fallback = {
    "cbc": ["glpk", "highs"],
    "glpk": ["highs"],
    "highs": ["glpk"]
}
```

### 3. Fallback de Modelos
```python
# Se GPT-4o falha, usar GPT-4o-mini
model_fallback = {
    "gpt-4o": ["gpt-4o-mini"],
    "gpt-4o-mini": ["gpt-3.5-turbo"]
}
```

---

## 📊 Decisões de Performance

### 1. Otimizações Críticas
- **Cache de prompts**: Evitar regeneração
- **Lazy loading**: Carregar agentes sob demanda
- **Connection pooling**: Para chamadas OpenAI
- **Compressão**: Para dados grandes

### 2. Limites de Recursos
- **Memória**: <800MB para funcionar no Streamlit Cloud
- **Tempo**: <30s para job completo
- **API calls**: <10 por job
- **Tokens**: <2000 por agente

### 3. Monitoramento de Performance
```python
# Métricas essenciais
performance_metrics = {
    "total_time": float,
    "agent_times": dict,
    "api_calls": int,
    "tokens_used": int,
    "memory_peak": float
}
```

---

## 🎯 Decisões de Negócio

### 1. Público-Alvo
- **Primário**: Consultores de otimização não-técnicos
- **Secundário**: Estudantes e pesquisadores
- **Não focado**: Desenvolvedores experientes

### 2. Limitações Aceitáveis
- **Problemas simples**: LP, MIP básicos
- **Não suportado**: Problemas estocásticos complexos, NLP avançado
- **Escalabilidade**: Até 100 usuários simultâneos

### 3. Roadmap de Features
- **Fase 1**: Problemas lineares e inteiros
- **Fase 2**: Problemas não-lineares simples
- **Fase 3**: Problemas estocásticos
- **Fase 4**: API para integração

---

## 🔧 Configurações Técnicas Específicas

### 1. Versões de Dependências
```txt
# requirements.txt - versões específicas
streamlit==1.28.0
praisonaiagents==0.1.0
pyomo==6.8.0
openai==1.3.0
jsonschema==4.19.0
streamlit-authenticator==0.2.0
```

### 2. Configuração Streamlit
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

### 3. Configuração de Segurança
```toml
# .streamlit/secrets.toml (NÃO commitado)
[OPENAI]
api_key = "sua-chave-openai"

[USERS]
admin_password_hash = "$2b$12$..."
demo_password_hash = "$2b$12$..."

[LIMITS]
max_calls_per_day = 50
max_calls_per_hour = 10
max_login_attempts = 5
lockout_duration = 300
```

### 3. Estrutura de Pastas ✅ **ATUALIZADA**
```
optimind/
├── app.py                    # Entry point ✅
├── pages/                    # Páginas Streamlit ✅
│   ├── __init__.py          # Inicialização das páginas ✅
│   ├── a_Home.py            # Página inicial ✅
│   ├── b_AdminTools.py      # Ferramentas administrativas ✅
│   ├── c_UserManagement.py  # Gerenciamento de usuários ✅
│   ├── d_NewJob.py          # Interface de entrada ✅
│   └── e_History.py         # Histórico de jobs ✅
├── agents/                   # Todos os agentes (próximo bloco)
├── schemas/                  # JSON schemas (próximo bloco)
├── prompts/                  # Prompt templates (próximo bloco)
├── utils/                    # Funções auxiliares ✅
│   ├── __init__.py          # Inicialização utils ✅
│   ├── auth.py              # Autenticação ✅
│   ├── sidebar.py           # Sidebar ✅
│   └── validators.py        # Validação ✅
├── tests/                    # Testes ✅
│   ├── test_app_online.py   # Testes de app online ✅
│   ├── test_auth.py         # Testes de autenticação ✅
│   ├── test_input_interface.py # Testes da interface ✅
│   └── test_openai_secrets.py  # Testes de secrets ✅
├── examples/                 # Exemplos de problemas (próximo bloco)
├── .streamlit/              # Configurações ✅
├── setup_dev_credentials.py # Gerenciador de credenciais ✅
├── SECURITY.md              # Credenciais (NÃO commitado) ✅
├── users.json               # Dados de usuários (NÃO commitado) ✅
└── login_attempts.json      # Logs de segurança (NÃO commitado) ✅
```

---

## 🚨 Problemas Conhecidos e Soluções

### 1. LLM Hallucination
- **Problema**: Agentes às vezes inventam dados
- **Solução**: Validação rigorosa de schemas
- **Fallback**: Pedir esclarecimentos ao usuário

### 2. Solver Infeasibility
- **Problema**: Problemas sem solução viável
- **Solução**: Detectar e explicar claramente
- **Fallback**: Sugerir relaxamento de restrições

### 3. Timeout Issues
- **Problema**: Problemas complexos demoram muito
- **Solução**: Timeout de 5 minutos
- **Fallback**: Sugerir simplificação do problema

### 4. Memory Constraints
- **Problema**: Streamlit Cloud tem 1GB RAM
- **Solução**: Otimizar uso de memória
- **Fallback**: Limitar tamanho dos problemas

---

## 📚 Recursos e Referências Essenciais

### 1. Documentação Principal
- [PraisonAI Docs](https://docs.praison.ai/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Pyomo Docs](https://pyomo.readthedocs.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)

### 2. Exemplos Úteis
- [Streamlit Multi-Agent Example](https://github.com/leporejoseph/PraisonAi-Streamlit)
- [Pyomo Optimization Examples](https://pyomo.readthedocs.io/en/stable/working_models.html)

### 3. Ferramentas de Debug
- [JSON Schema Validator](https://www.jsonschemavalidator.net/)
- [OpenAI Token Counter](https://platform.openai.com/tokenizer)

---

## 🎯 Checklist de Continuidade

### Antes de Retomar Desenvolvimento
- [ ] Ler este documento completamente
- [ ] Verificar estado atual do projeto
- [ ] Validar configurações de ambiente
- [ ] Testar conexões (OpenAI, Streamlit)
- [ ] Revisar último bloco implementado (Bloco 2 concluído)

### Durante Desenvolvimento
- [ ] Seguir padrões estabelecidos
- [ ] Manter compatibilidade com decisões arquiteturais
- [ ] Documentar mudanças significativas
- [ ] Testar continuamente
- [ ] Monitorar custos e performance

### Após Implementação
- [ ] Validar critérios de sucesso
- [ ] Testar em produção
- [ ] Atualizar documentação
- [ ] Planejar próximo bloco

---

**Versão**: 1.1  
**Data**: Julho 2025  
**Status**: Contexto essencial para desenvolvimento - Bloco 2 concluído 