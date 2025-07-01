# 🧠 OptiMind - Otimização Inteligente Assistida por IA

## 📋 Descrição

O **OptiMind** é uma plataforma revolucionária que transforma descrições em linguagem natural de problemas de otimização em soluções matemáticas completas, código executável e insights de negócio.

## 🚀 Funcionalidades

- **Interpretação Natural**: Descreva problemas de otimização em linguagem natural
- **Pipeline Multi-Agente**: 7 agentes especializados processam cada etapa
- **Modelagem Automática**: Geração automática de modelos matemáticos
- **Execução Segura**: Sandbox para execução de código Pyomo
- **Insights Inteligentes**: Interpretação automática de resultados
- **Interface Intuitiva**: Interface web moderna com Streamlit

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
├── app.py                          # Aplicação principal
├── requirements.txt                # Dependências Python
├── README.md                       # Este arquivo
├── .streamlit/
│   ├── config.toml                # Configurações Streamlit
│   └── secrets.toml               # Secrets (não commitado)
├── agents/                        # Agentes especializados
│   ├── __init__.py
│   ├── base_agent.py
│   ├── meaning_agent.py
│   ├── pesquisador_agent.py
│   ├── matematico_agent.py
│   ├── formulador_agent.py
│   ├── executor_agent.py
│   └── interpretador_agent.py
├── schemas/                       # Schemas JSON
│   ├── __init__.py
│   ├── problem_schema.json
│   ├── model_schema.json
│   └── result_schema.json
├── prompts/                       # Prompts dos agentes
│   ├── meaning.txt
│   ├── pesquisador.txt
│   ├── matematico.txt
│   └── formulador.txt
├── utils/                         # Utilitários
│   ├── __init__.py
│   ├── auth.py                   # Autenticação
│   └── validators.py             # Validadores
├── tests/                         # Testes
│   ├── __init__.py
│   ├── test_agents.py
│   └── test_schemas.py
└── examples/                      # Exemplos de uso
    ├── linear_programming.py
    └── mixed_integer.py
```

## 🧪 Testes ✅ **IMPLEMENTADO**

### Testes de Autenticação

O sistema de autenticação possui testes completos que verificam:

- ✅ **Login e Logout**: Verificação de credenciais e sessões
- ✅ **Criação de Usuários**: Adição de novos usuários com validação
- ✅ **Remoção de Usuários**: Exclusão segura de contas
- ✅ **Validação de Senha**: Verificação de força de senha
- ✅ **Rate Limiting**: Proteção contra ataques de força bruta
- ✅ **Hash de Senhas**: Criptografia segura com bcrypt
- ✅ **Integração**: Testes de integração com Streamlit

### Executar Testes

```bash
# Executar todos os testes
python run_tests.py

# Listar testes disponíveis
python run_tests.py --list

# Executar teste específico
python run_tests.py --test TestAuthManager.test_add_user

# Ver ajuda
python run_tests.py --help

# Ou usar pytest diretamente
pytest tests/ -v
```

### Cobertura de Testes

- **14 testes** cobrindo todas as funcionalidades críticas
- **Testes unitários** para cada componente
- **Testes de integração** para fluxos completos
- **Testes de segurança** para validação de senhas e rate limiting

## 🚀 Deploy

### Streamlit Community Cloud

1. **Push para GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Configure no Streamlit Cloud**
   - Acesse [share.streamlit.io](https://share.streamlit.io)
   - Conecte seu repositório GitHub
   - Configure os secrets na interface web
   - Deploy!

### Configuração de Secrets no Streamlit Cloud

Adicione os seguintes secrets na interface do Streamlit Cloud:

```
OPENAI_API_KEY = sua-chave-openai
ADMIN_PASSWORD_HASH = hash-da-senha-admin
DEMO_PASSWORD_HASH = hash-da-senha-demo
MAX_CALLS_PER_DAY = 50
MAX_CALLS_PER_HOUR = 10
```

## 📚 Documentação

- [OPTIMIND_CONTEXTO_ESSENCIAL.md](OPTIMIND_CONTEXTO_ESSENCIAL.md) - Decisões fundamentais
- [OPTIMIND_BLUEPRINT_FINAL.md](OPTIMIND_BLUEPRINT_FINAL.md) - Arquitetura detalhada
- [OPTIMIND_ROADMAP.md](OPTIMIND_ROADMAP.md) - Plano de desenvolvimento

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🆘 Suporte

Para suporte, abra uma issue no GitHub ou entre em contato através do email: support@optimind.com

## 🔄 Roadmap

- [x] Bloco 1: Fundação Básica (Autenticação)
- [ ] Bloco 2: Interface de Entrada
- [ ] Bloco 3: Agente Meaning
- [ ] Bloco 4: Revisão e Confirmação
- [ ] Bloco 5: Pipeline Completo
- [ ] Bloco 6: Otimizações e Deploy

---

**OptiMind** - Transformando problemas de otimização em soluções inteligentes! 🧠✨ 