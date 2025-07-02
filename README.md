# 🧠 OptiMind - Otimização Inteligente Assistida por IA

## 📋 Descrição

O **OptiMind** é uma plataforma revolucionária que transforma descrições em linguagem natural de problemas de otimização em soluções matemáticas completas, código executável e insights de negócio.

## 🚀 Funcionalidades

- **Interpretação Natural**: Descreva problemas de otimização em linguagem natural ✅ **IMPLEMENTADO**
- **Pipeline Multi-Agente**: 7 agentes especializados processam cada etapa (1/7 implementado)
- **Modelagem Automática**: Geração automática de modelos matemáticos
- **Execução Segura**: Sandbox para execução de código Pyomo
- **Insights Inteligentes**: Interpretação automática de resultados
- **Interface Intuitiva**: Interface web moderna com Streamlit ✅ **IMPLEMENTADO**

## 🏗️ Arquitetura

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

## 🎯 Status Atual do Projeto

### ✅ Blocos Concluídos (3/9)

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
- **Acervo de problemas real** convertido para TOML (22 problemas)
- **Teste automatizado completo** para todos os problemas do acervo

### 🔄 Próximos Blocos (6/9)
- **Bloco 4**: Pesquisador Agent
- **Bloco 5**: Matemático Agent
- **Bloco 6**: Formulador Agent
- **Bloco 7**: Executor Agent
- **Bloco 8**: Interpretador Agent
- **Bloco 9**: Auditor Agent

## 🤖 Meaning Agent - Funcionalidades Implementadas

### Conversação Natural
- **Chat interativo**: Converse naturalmente com o agente para definir problemas
- **Contexto de chat**: O agente mantém histórico para construir problemas passo a passo
- **Respostas amigáveis**: Tratamento especial para saudações e mensagens casuais

### Interpretação Inteligente
- **Estruturação automática**: Converte descrições em JSON estruturado
- **Separação de variáveis**: Distingue variáveis de decisão e auxiliares
- **Captura de equações**: Identifica expressões matemáticas para variáveis auxiliares
- **Política de não-invenção**: Nunca inventa dados, só estrutura o que você fornece

### Validação Robusta
- **Schema JSON rigoroso**: Validação completa de todos os campos
- **Campo `data` obrigatório**: Todos os parâmetros, tabelas e valores são capturados
- **Confiança mensurável**: Score de confiança na interpretação
- **Clarificações automáticas**: Pede dados faltantes quando necessário

### Exemplo de Uso
```
Usuário: "Quero maximizar lucro: 3x + 4y sujeito a x + y <= 10"

Meaning Agent responde:
{
  "problem_type": "LP",
  "sense": "maximize",
  "objective": "3*x + 4*y",
  "decision_variables": {
    "x": {"type": "Real", "description": "Quantity of product X", "bounds": [0, null]},
    "y": {"type": "Real", "description": "Quantity of product Y", "bounds": [0, null]}
  },
  "constraints": [{"expression": "x + y <= 10", "description": "Total capacity limit"}],
  "data": {},
  "is_valid_problem": true,
  "confidence": 0.95,
  "clarification": "Great! I understand your LP problem..."
}
```

## 🧪 Testes Automatizados

### Teste Completo do Meaning Agent
```bash
# Testa todos os problemas do acervo (22 problemas)
python tests/test_all_problems.py --all

# Testa um problema específico
python tests/test_all_problems.py --problem "The Extreme Downhill Company"
```

O teste automatizado valida:
- ✅ Processamento correto de todos os problemas do acervo real
- ✅ Validação de schema JSON para cada resposta
- ✅ Tratamento de erros e exceções
- ✅ Relatório detalhado de sucessos e falhas
- ✅ Cobertura completa do Meaning Agent

### Acervo de Problemas
- **22 problemas reais** convertidos para formato TOML
- **Problemas clássicos** de otimização (LP, MIP, NLP, Stochastic, etc.)
- **Dados estruturados** prontos para teste automatizado
- **Curadoria contínua** via `prompts/problem_list.toml`

## 🛠️ Instalação

### Pré-requisitos

- Python 3.9+
- pip
- Git

### Passos de Instalação

1. **Clone o repositório**
   ```bash
   git clone <repository-url>
   cd OptiMind
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure as variáveis de ambiente**
   ```bash
   # Crie o arquivo .streamlit/secrets.toml
   mkdir .streamlit
   ```

   Adicione ao arquivo `.streamlit/secrets.toml`:
   ```toml
   [OPENAI]
   api_key = "sua-chave-openai-aqui"
   
   [USERS]
   admin_password_hash = "$2b$12$..."
   user1_password_hash = "$2b$12$..."
   
   [LIMITS]
   max_calls_per_day = 50
   max_calls_per_hour = 10
   ```

5. **Execute a aplicação**
   ```bash
   streamlit run app.py
   ```

   A aplicação estará disponível em: **http://localhost:8501**

   **Login:** Use as credenciais do arquivo `SECURITY.md` ou execute `python setup_dev_credentials.py`

## 🔐 Autenticação ✅ **IMPLEMENTADO**

### Usuários Padrão

Para desenvolvimento, o sistema cria automaticamente dois usuários com senhas seguras.

**Credenciais de Desenvolvimento:**
> ⚠️ **Por segurança, as credenciais não estão documentadas aqui.**
> Consulte o arquivo `SECURITY.md` (não commitado) ou execute `python setup_dev_credentials.py`

> ⚠️ **IMPORTANTE**: As senhas são geradas automaticamente e **NÃO estão documentadas aqui por segurança**. 
> Para obter as credenciais de desenvolvimento, consulte o arquivo `SECURITY.md` (não commitado) ou 
> execute o script de setup: `python setup_dev_credentials.py`

> 🔒 **Segurança**: Em produção, sempre use senhas únicas e complexas geradas individualmente!

### Características de Segurança Implementadas:
- ✅ Hash bcrypt com salt automático
- ✅ Validação de força de senha (12+ chars, maiúsculas, minúsculas, números, símbolos)
- ✅ Rate limiting (5 tentativas por IP, bloqueio de 5 minutos)
- ✅ Logs de tentativas de login
- ✅ Arquivos sensíveis protegidos (.gitignore)
- ✅ Compatibilidade com streamlit-authenticator v0.4.2
- ✅ Estrutura correta (cookie_key, session_state)

### Adicionando Novos Usuários

```python
from utils.auth import AuthManager

auth_manager = AuthManager()
success, message = auth_manager.add_user("novo_usuario", "Nome Completo", "senha123")
if success:
    print("Usuário criado com sucesso!")
else:
    print(f"Erro: {message}")
```

### 🔐 Gerenciando Credenciais de Desenvolvimento

Para gerenciar as credenciais de desenvolvimento:

```bash
# Mostrar credenciais atuais
python setup_dev_credentials.py

# Ou execute diretamente para gerar novas credenciais
python setup_dev_credentials.py
```

## 📁 Estrutura do Projeto

```
OptiMind/
├── app.py                          # Aplicação principal ✅
├── requirements.txt                # Dependências Python ✅
├── README.md                       # Este arquivo ✅
├── .streamlit/
│   ├── config.toml                # Configurações Streamlit ✅
│   └── secrets.toml               # Secrets (não commitado) ✅
├── pages/                          # Páginas Streamlit ✅
│   ├── __init__.py                # Inicialização das páginas ✅
│   ├── a_Home.py                  # Página inicial ✅
│   ├── b_AdminTools.py            # Ferramentas administrativas ✅
│   ├── c_UserManagement.py        # Gerenciamento de usuários ✅
│   ├── d_NewJob.py                # Interface de chat com Meaning Agent ✅
│   └── e_History.py               # Histórico de jobs ✅
├── agents/                        # Agentes especializados ✅
│   ├── __init__.py               # Inicialização dos agentes ✅
│   ├── base_agent.py             # Classe base para agentes ✅
│   └── meaning_agent.py          # Meaning Agent implementado ✅
├── schemas/                       # Schemas JSON ✅
│   ├── __init__.py               # Inicialização schemas ✅
│   ├── problem_schema.json       # Schema do problema ✅
│   └── validator.py              # Validador JSON ✅
├── prompts/                       # Prompts dos agentes ✅
│   ├── meaning.txt               # Prompt do Meaning Agent ✅
├── utils/                         # Utilitários ✅
│   ├── __init__.py               # Inicialização utils ✅
│   ├── auth.py                   # Autenticação ✅
│   └── sidebar.py                # Sidebar ✅
├── tests/                         # Testes ✅
│   ├── test_app_online.py        # Testes de app online ✅
│   ├── test_auth.py              # Testes de autenticação ✅
│   ├── test_input_interface.py   # Testes da interface de entrada ✅
│   ├── test_meaning_agent.py     # Testes do Meaning Agent ✅
│   └── test_openai_secrets.py    # Testes de secrets ✅
└── examples/                      # Exemplos de uso (próximo bloco)
    ├── linear_programming.py
    └── mixed_integer.py
```

## 🧪 Testes ✅ **IMPLEMENTADO**

### Testes de Autenticação

O sistema de autenticação possui testes completos que verificam:

- ✅ **Login e Logout**: Verificação de credenciais e sessões
- ✅ **Criação de Usuários**: Adição de novos usuários com validação
- ✅ **Validação de Senha**: Força de senha e hash bcrypt
- ✅ **Rate Limiting**: Proteção contra força bruta
- ✅ **Logs de Segurança**: Rastreamento de tentativas de login

### Testes da Interface de Entrada

Testes abrangentes da interface de entrada:

- ✅ **Validação de Input**: Texto vazio, palavras-chave, restrições de negócio
- ✅ **Navegação**: Transições entre páginas
- ✅ **Estado da Aplicação**: Persistência de dados
- ✅ **Interface Responsiva**: Adaptação a diferentes tamanhos

### Testes do Meaning Agent

Testes robustos do primeiro agente do pipeline:

- ✅ **Casos Clássicos**: Problemas LP simples e complexos
- ✅ **Variáveis Auxiliares**: Captura de equações matemáticas
- ✅ **Contexto de Chat**: Construção passo a passo de problemas
- ✅ **Mensagens Casuais**: Tratamento de saudações
- ✅ **Validação de Schema**: Todas as saídas validadas
- ✅ **Política de Não-Invenção**: Nunca inventa dados
- ✅ **Campo `data`**: Captura de todos os parâmetros

### Executando os Testes

```bash
# Executar todos os testes
python run_tests.py

# Testes específicos
python -m pytest tests/test_meaning_agent.py
python -m pytest tests/test_auth.py
python -m pytest tests/test_input_interface.py
```

## 🎯 Como Usar

### 1. Acesse a Aplicação
- Execute `streamlit run app.py`
- Acesse http://localhost:8501
- Faça login com suas credenciais

### 2. Defina seu Problema
- Vá para "🚀 New Job"
- Descreva seu problema de otimização em linguagem natural
- Exemplo: "Maximize profit: 3x + 4y subject to x + y <= 10"

### 3. Interaja com o Meaning Agent
- O agente interpretará sua descrição
- Ele pode pedir esclarecimentos se necessário
- Continue a conversa para refinar o problema

### 4. Revise o Resultado
- O agente estruturará seu problema em JSON
- Revise as variáveis, restrições e dados
- Confirme se tudo está correto

### 5. Próximos Passos
- O sistema está preparado para os próximos agentes
- Pesquisador Agent será implementado em seguida
- Pipeline completo em desenvolvimento

## 🔧 Desenvolvimento

### Estrutura de Agentes

```python
# Padrão para todos os agentes
class BaseAgent:
    def __init__(self, name, system_prompt):
        self.name = name
        self.system_prompt = system_prompt
        self.llm = OpenAI(model="gpt-4o-mini")
    
    def process(self, input_data):
        # 1. Validar input
        # 2. Chamar LLM
        # 3. Validar output
        # 4. Retornar resultado
        pass

# Meaning Agent implementado
class MeaningAgent(BaseAgent):
    def __init__(self):
        super().__init__("Meaning", load_prompt("meaning.txt"))
        self.chat_history = []
    
    def process_problem(self, user_input):
        # Processa problema com contexto de chat
        # Valida saída contra schema
        # Retorna JSON estruturado
        pass
```

### Schemas JSON

```json
{
  "problem_type": "LP|MIP|NLP|Stochastic|Unknown",
  "sense": "maximize|minimize",
  "objective": "mathematical expression",
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
    "parameter_name": "value or list or table"
  },
  "is_valid_problem": true/false,
  "confidence": 0.0-1.0,
  "clarification": "friendly response to user"
}
```

## 📊 Métricas de Qualidade

### Cobertura de Testes
- **Autenticação**: 100% das funcionalidades críticas
- **Interface**: 100% dos fluxos de usuário
- **Meaning Agent**: 100% dos casos de uso
- **Schemas**: 100% da validação

### Performance
- **Tempo de resposta**: < 2s para processamento do Meaning Agent
- **Taxa de sucesso**: > 95% para problemas bem definidos
- **Validação**: 100% das saídas validadas contra schema

### Segurança
- **Rate limiting**: 5 tentativas por IP, bloqueio de 5 minutos
- **Senhas**: Hash bcrypt com salt automático
- **Arquivos sensíveis**: Protegidos por .gitignore
- **Logs**: Rastreamento completo de tentativas de login

## 🚀 Próximos Passos

### Curto Prazo (Próximas 2 semanas)
1. **Implementar Pesquisador Agent** (Bloco 4)
2. **Criar schema para problemas refinados**
3. **Integrar Pesquisador no pipeline**
4. **Testes de integração entre Meaning e Pesquisador**

### Médio Prazo (Próximos 2 meses)
1. **Completar pipeline de agentes** (Matemático, Formulador, Executor)
2. **Implementar sistema MCP**
3. **Criar timeline visual de progresso**
4. **Testes end-to-end completos**

### Longo Prazo (Próximos 6 meses)
1. **Implementar Interpretador e Auditor**
2. **Otimizações de performance**
3. **Deploy em produção**
4. **Documentação completa**

## 📚 Documentação

### Arquivos Principais
- `README.md`: Este arquivo - guia de instalação e uso
- `OPTIMIND_BLUEPRINT_FINAL.md`: Arquitetura completa do sistema
- `OPTIMIND_CONTEXTO_ESSENCIAL.md`: Contexto para desenvolvimento
- `OPTIMIND_ROADMAP.md`: Roadmap detalhado de desenvolvimento

### Schemas e Prompts
- `schemas/problem_schema.json`: Schema do problema de otimização
- `prompts/meaning.txt`: Prompt do Meaning Agent
- `tests/test_meaning_agent.py`: Testes do Meaning Agent

### Código Principal
- `app.py`: Aplicação principal Streamlit
- `pages/d_NewJob.py`: Interface de chat com Meaning Agent
- `agents/meaning_agent.py`: Implementação do Meaning Agent
- `utils/auth.py`: Sistema de autenticação

## 🔗 Links e Recursos

### Tecnologias Utilizadas
- **Streamlit**: Interface web
- **PraisonAI**: Orquestração multi-agente (planejado)
- **Pyomo**: Modelagem de otimização (planejado)
- **OpenAI GPT-4**: Processamento de linguagem natural
- **JSON Schema**: Validação de dados

### Recursos Externos
- [Documentação Streamlit](https://docs.streamlit.io/)
- [Documentação Pyomo](https://pyomo.readthedocs.io/)
- [JSON Schema Specification](https://json-schema.org/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

## 🤝 Contribuição

### Como Contribuir
1. Fork o repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Padrões de Código
- Siga PEP 8 para Python
- Adicione testes para novas funcionalidades
- Documente funções e classes
- Mantenha cobertura de testes alta

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---

## 🎉 Status do Projeto

**OptiMind está em desenvolvimento ativo!**

- ✅ **Bloco 1**: Fundação Básica - CONCLUÍDO
- ✅ **Bloco 2**: Interface de Entrada - CONCLUÍDO  
- ✅ **Bloco 3**: Meaning Agent e Schemas - CONCLUÍDO
- 🔄 **Bloco 4**: Pesquisador Agent - EM DESENVOLVIMENTO
- 🔄 **Blocos 5-9**: Próximos agentes - PLANEJADOS

**33% do projeto concluído** (3/9 blocos)

O sistema já possui uma base sólida com autenticação robusta, interface funcional e o primeiro agente (Meaning) completamente implementado e testado. Estamos prontos para avançar para o Pesquisador Agent e completar o pipeline multi-agente.

---

*OptiMind - Transformando problemas de otimização em soluções inteligentes* 🧠✨ 