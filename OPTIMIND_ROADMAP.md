# OptiMind - Roadmap de Desenvolvimento

## 🎯 Visão Geral

Este roadmap divide o desenvolvimento do OptiMind em **blocos lógicos e testáveis**, permitindo validação incremental e deploy contínuo. Cada bloco deve ser **completamente funcional** antes de avançar para o próximo.

---

## 📋 Bloco 1: Fundação Básica (Semana 1)

### 🎯 Objetivo
Criar a base mínima funcional com autenticação robusta, configuração e deploy.

### 🔒 Melhorias de Segurança Implementadas
- **Senhas seguras**: Hash bcrypt com salt automático
- **Validação de força**: 12+ caracteres, maiúsculas, minúsculas, números, símbolos
- **Rate limiting**: 5 tentativas por IP, bloqueio de 5 minutos
- **Logs de segurança**: Rastreamento de tentativas de login
- **Proteção de arquivos**: users.json, login_attempts.json, SECURITY.md não commitados
- **Script de gerenciamento**: setup_dev_credentials.py para credenciais seguras

### 📝 Tarefas

#### 1.1 Setup do Projeto
- [x] Criar repositório Git
- [x] Configurar ambiente virtual Python 3.9+
- [x] Criar estrutura de pastas básica
- [x] Configurar `.gitignore`

#### 1.2 Autenticação Básica ✅ **CONCLUÍDO**
- [x] Instalar `streamlit-authenticator` v0.4.2
- [x] Criar página de login funcional
- [x] Implementar verificação de credenciais
- [x] Testar fluxo de autenticação
- [x] Implementar sistema de senhas seguras (bcrypt)
- [x] Adicionar validação de força de senha
- [x] Implementar rate limiting (5 tentativas por IP)
- [x] Adicionar logs de tentativas de login
- [x] Proteger arquivos sensíveis (.gitignore)
- [x] Criar script de gerenciamento de credenciais
- [x] Corrigir compatibilidade com streamlit-authenticator v0.4.2
- [x] Implementar estrutura correta (cookie_key, session_state)
- [x] Testar login/logout completo

#### 1.2.1 Testes Robustos de Autenticação ✅ **CONCLUÍDO**
- [x] Criar suite completa de testes (`tests/test_auth.py`)
- [x] Implementar testes unitários para todas as funcionalidades
- [x] Testar hash e verificação de senhas (bcrypt)
- [x] Testar validação de força de senha (12+ chars, maiúsculas, minúsculas, números, símbolos)
- [x] Testar criação e remoção de usuários
- [x] Testar rate limiting (5 tentativas por IP, bloqueio de 5 minutos)
- [x] Testar obtenção e listagem de usuários
- [x] Testar integração com Streamlit (mocks)
- [x] Criar script de execução de testes (`run_tests.py`)
- [x] Implementar testes com fixtures pytest para ambiente limpo
- [x] Garantir 100% de cobertura das funcionalidades críticas
- [x] Validar que testes usam as mesmas funções do app real
- [x] **Resultado**: 11 testes passando, 3 pulados (integração Streamlit)

#### 1.3 Página Inicial ✅ **CONCLUÍDO**
- [x] Criar página Home com descrição do OptiMind
- [x] Adicionar botão "Novo Job" (ainda não funcional)
- [x] Implementar design moderno e light em inglês
- [x] Implementar Golden Circle (Why/How/What)
- [x] Adicionar casos de uso em consultoria
- [x] Incluir algoritmos técnicos detalhados
- [x] Explicar arquitetura técnica e agentes
- [x] Adicionar logo centralizado no final
- [x] **Implementar storytelling focado na dor dos consultores**
- [x] **Adicionar casos de sucesso da Mirow Co com métricas reais**
- [x] **Mostrar simplicidade para usuário vs complexidade interna**
- [x] **Destacar problemas PhD-level resolvidos**
- [x] **Incluir mensagem de democratização de soluções avançadas**
- [x] Implementar sidebar bonito e funcional
- [x] Adicionar header com nome do app (OptiMind)
- [x] Implementar navegação principal (Home, Novo Job, Histórico)
- [x] Implementar botão de logout funcional
- [x] Adicionar footer com branding Mirow & Co.
- [x] Aplicar CSS customizado para design moderno
- [x] Integrar sidebar em todas as páginas principais
- [x] Testar funcionalidade de logout
- [x] Validar navegação entre seções
- [X] Gestao de usuario para adicionar e retirar user quando for admin

#### 1.4 Configuração de Secrets
- [x] Configurar `.streamlit/secrets.toml`
- [x] Implementar validação da chave OpenAI
- [x] Testar conexão com OpenAI API
- [x] Configurar rate limiting básico

#### 1.5 Deploy Inicial
- [x] Criar `requirements.txt` básico
- [x] Configurar `.streamlit/config.toml`
- [ ] Deploy no Streamlit Community Cloud
- [ ] Configurar secrets na Cloud
- [ ] Testar deploy completo

### ✅ Critérios de Sucesso (Testes)
```python
# Testes para validar Bloco 1
def test_bloco_1():
    # 1. Autenticação funciona
    assert login_successful("admin", "password") == True
    assert login_failed("wrong", "credentials") == False
    
    # 2. Segurança implementada
    assert password_strength_validation_works() == True
    assert rate_limiting_works() == True
    assert sensitive_files_protected() == True
    
    # 3. Secrets configurados
    assert openai_api_key_is_valid() == True
    assert secrets_not_exposed_in_frontend() == True
    
    # 4. Deploy funcional
    assert app_loads_without_errors() == True
    assert authentication_works_in_production() == True
    
    # 5. Testes robustos implementados ✅
    assert run_tests() == "11 passed, 3 skipped"  # python run_tests.py
    assert test_coverage_auth() == "100%"  # Todas funcionalidades críticas testadas
    assert tests_use_real_functions() == True  # Testes usam código real do app
```

### 🚀 Resultado Esperado
- Site básico funcionando com login seguro
- Sistema de autenticação robusto com rate limiting
- Senhas seguras com validação de força
- Arquivos sensíveis protegidos
- Chave OpenAI validada e funcionando
- Deploy no Streamlit Cloud operacional
- **Suite completa de testes robustos** (11 testes passando)
- **Cobertura 100% das funcionalidades críticas**
- **Testes validam código real do app**
- Base sólida para próximos blocos

---

## 📋 Bloco 2: Interface de Entrada (Semana 2)

### 🎯 Objetivo
Implementar interface para entrada de problemas de otimização.

### 📝 Tarefas

#### 2.1 Página de Definição de Problema
- [ ] Criar formulário de entrada de texto
- [ ] Adicionar seleção Maximizar/Minimizar
- [ ] Implementar validação básica de input
- [ ] Adicionar exemplos e placeholder

#### 2.2 Navegação entre Páginas
- [ ] Implementar sistema de páginas Streamlit
- [ ] Criar fluxo: Home → Novo Job → Definição
- [ ] Adicionar breadcrumbs/navegação
- [ ] Testar transições entre páginas

#### 2.3 Validação de Input
- [ ] Implementar validação de texto não vazio
- [ ] Detectar palavras-chave (maximizar, minimizar)
- [ ] Validar formato básico do problema
- [ ] Mostrar mensagens de erro amigáveis

#### 2.4 Estado da Aplicação
- [ ] Implementar `st.session_state` para dados
- [ ] Persistir dados entre páginas
- [ ] Limpar estado ao iniciar novo job
- [ ] Testar persistência de dados

### ✅ Critérios de Sucesso (Testes)
```python
def test_bloco_2():
    # 1. Interface de entrada funciona
    assert can_input_problem_text() == True
    assert can_select_maximize_minimize() == True
    
    # 2. Validação funciona
    assert validates_empty_input() == True
    assert validates_optimization_keywords() == True
    
    # 3. Navegação funciona
    assert can_navigate_between_pages() == True
    assert state_persists_between_pages() == True
```

### 🚀 Resultado Esperado
- Interface completa para entrada de problemas
- Validação básica funcionando
- Navegação fluida entre páginas
- Estado da aplicação gerenciado

---

## 📋 Bloco 3: Agente Meaning (Semana 3)

### 🎯 Objetivo
Implementar o primeiro agente que interpreta problemas de otimização.

### 📝 Tarefas

#### 3.1 Estrutura de Agentes
- [ ] Criar pasta `agents/`
- [ ] Implementar classe base `BaseAgent`
- [ ] Configurar PraisonAI básico
- [ ] Testar conexão com OpenAI

#### 3.2 Agente Meaning
- [ ] Implementar `MeaningAgent`
- [ ] Criar prompt específico para interpretação
- [ ] Implementar validação de JSON de saída
- [ ] Testar com problemas simples

#### 3.3 Schemas JSON
- [ ] Criar pasta `schemas/`
- [ ] Implementar `problem_schema.json`
- [ ] Criar validador JSON
- [ ] Testar validação de schemas

#### 3.4 Integração com UI
- [ ] Conectar formulário ao agente
- [ ] Mostrar resultado da interpretação
- [ ] Implementar feedback visual
- [ ] Adicionar loading states

#### 3.5 Tratamento de Erros
- [ ] Implementar fallback para problemas inválidos
- [ ] Criar mensagens de erro amigáveis
- [ ] Testar cenários de falha
- [ ] Implementar retry básico

### ✅ Critérios de Sucesso (Testes)
```python
def test_bloco_3():
    # 1. Agente funciona
    assert agent_understands_valid_problem() == True
    assert agent_rejects_invalid_input() == True
    
    # 2. JSON válido
    assert output_matches_schema() == True
    assert json_validation_works() == True
    
    # 3. UI integrada
    assert can_submit_problem_to_agent() == True
    assert shows_interpretation_result() == True
    assert handles_errors_gracefully() == True
```

### 🚀 Resultado Esperado
- Agente Meaning funcionando
- Interpretação correta de problemas válidos
- Rejeição adequada de problemas inválidos
- Interface integrada com feedback

---

## 📋 Bloco 4: Revisão e Confirmação (Semana 4)

### 🎯 Objetivo
Implementar etapa de revisão onde usuário confirma interpretação.

### 📝 Tarefas

#### 4.1 Página de Revisão
- [ ] Criar página de revisão do problema
- [ ] Mostrar interpretação do agente
- [ ] Exibir JSON estruturado (colapsável)
- [ ] Implementar botões Confirmar/Editar

#### 4.2 Formatação de Saída
- [ ] Formatar interpretação de forma amigável
- [ ] Destacar variáveis, objetivo e restrições
- [ ] Implementar visualização JSON bonita
- [ ] Adicionar tooltips explicativos

#### 4.3 Fluxo de Confirmação
- [ ] Implementar confirmação do usuário
- [ ] Permitir edição e reenvio
- [ ] Salvar problema confirmado
- [ ] Transicionar para próximo estágio

#### 4.4 Validação de Confirmação
- [ ] Validar que usuário confirmou
- [ ] Implementar timeout de confirmação
- [ ] Permitir cancelamento
- [ ] Testar fluxo completo

### ✅ Critérios de Sucesso (Testes)
```python
def test_bloco_4():
    # 1. Revisão funciona
    assert shows_interpretation_clearly() == True
    assert json_display_is_collapsible() == True
    
    # 2. Confirmação funciona
    assert can_confirm_problem() == True
    assert can_edit_and_resubmit() == True
    
    # 3. Fluxo completo
    assert problem_confirmed_saves_to_state() == True
    assert can_proceed_to_next_stage() == True
```

### 🚀 Resultado Esperado
- Interface de revisão clara e intuitiva
- Confirmação/edição funcionando
- Fluxo completo até confirmação
- Base para pipeline de agentes

---

## 📋 Bloco 5: Pipeline de Agentes (Semana 5-6)

### 🎯 Objetivo
Implementar pipeline completo dos 7 agentes com orquestração.

### 📝 Tarefas

#### 5.1 MetaManager e MCP
- [ ] Implementar `MetaManager` básico
- [ ] Criar sistema MCP simples
- [ ] Implementar controle de fluxo
- [ ] Testar orquestração básica

#### 5.2 Agentes Restantes
- [ ] Implementar `PesquisadorAgent`
- [ ] Implementar `MatematicoAgent`
- [ ] Implementar `FormuladorAgent`
- [ ] Implementar `ExecutorAgent`
- [ ] Implementar `InterpretadorAgent`
- [ ] Implementar `AuditorAgent`

#### 5.3 Schemas Completos
- [ ] Criar todos os schemas JSON
- [ ] Implementar validadores
- [ ] Testar validação em cada etapa
- [ ] Documentar schemas

#### 5.4 Prompts Especializados
- [ ] Criar prompts para cada agente
- [ ] Testar prompts com exemplos
- [ ] Otimizar prompts baseado em testes
- [ ] Documentar prompts

#### 5.5 Integração Pyomo
- [ ] Configurar Pyomo e solvers
- [ ] Testar execução de código Pyomo
- [ ] Implementar sandbox de execução
- [ ] Validar resultados

### ✅ Critérios de Sucesso (Testes)
```python
def test_bloco_5():
    # 1. Pipeline completo
    assert all_agents_execute_sequentially() == True
    assert pipeline_produces_valid_result() == True
    
    # 2. Validação em cada etapa
    assert each_stage_validates_output() == True
    assert schemas_are_enforced() == True
    
    # 3. Pyomo funciona
    assert can_solve_simple_lp() == True
    assert can_solve_simple_mip() == True
    assert execution_is_sandboxed() == True
```

### 🚀 Resultado Esperado
- Pipeline completo de 7 agentes funcionando
- Validação rigorosa em cada etapa
- Execução Pyomo sandboxed
- Resultados válidos para problemas simples

---

## 📋 Bloco 6: Timeline e Progresso (Semana 7)

### 🎯 Objetivo
Implementar interface de progresso e timeline do pipeline.

### 📝 Tarefas

#### 6.1 Timeline Visual
- [ ] Criar timeline horizontal
- [ ] Mostrar progresso em tempo real
- [ ] Implementar ícones para cada agente
- [ ] Adicionar animações de progresso

#### 6.2 Painéis de Detalhes
- [ ] Implementar painéis laterais para cada agente
- [ ] Mostrar JSON de saída de cada etapa
- [ ] Exibir LaTeX do agente matemático
- [ ] Mostrar código Pyomo gerado

#### 6.3 Estados de Progresso
- [ ] Implementar estados: pendente, executando, completo, erro
- [ ] Adicionar spinners durante execução
- [ ] Mostrar tempo de execução
- [ ] Implementar cancelamento

#### 6.4 Feedback em Tempo Real
- [ ] Atualizar progresso em tempo real
- [ ] Mostrar mensagens de status
- [ ] Implementar notificações
- [ ] Adicionar logs visuais

### ✅ Critérios de Sucesso (Testes)
```python
def test_bloco_6():
    # 1. Timeline funciona
    assert shows_progress_visually() == True
    assert updates_in_real_time() == True
    
    # 2. Detalhes acessíveis
    assert can_view_agent_details() == True
    assert shows_json_latex_code() == True
    
    # 3. Estados corretos
    assert shows_correct_states() == True
    assert handles_errors_in_timeline() == True
```

### 🚀 Resultado Esperado
- Timeline visual funcional
- Progresso em tempo real
- Detalhes de cada etapa acessíveis
- Interface profissional e informativa

---

## 📋 Bloco 7: Resultados e Insights (Semana 8)

### 🎯 Objetivo
Implementar página de resultados finais com insights e downloads.

### 📝 Tarefas

#### 7.1 Página de Resultados
- [ ] Criar página de resultados
- [ ] Mostrar valor ótimo da função objetivo
- [ ] Exibir tabela de variáveis e valores
- [ ] Implementar visualizações básicas

#### 7.2 Insights de Negócio
- [ ] Exibir insights do agente interpretador
- [ ] Destacar restrições binding
- [ ] Mostrar recomendações
- [ ] Implementar formatação rica

#### 7.3 Downloads e Exportação
- [ ] Implementar download do código Pyomo
- [ ] Gerar PDF do modelo LaTeX
- [ ] Exportar resultados em JSON
- [ ] Criar relatório executivo

#### 7.4 Histórico de Jobs
- [ ] Implementar salvamento de jobs
- [ ] Criar lista de jobs anteriores
- [ ] Permitir reexecução de jobs
- [ ] Implementar filtros e busca

### ✅ Critérios de Sucesso (Testes)
```python
def test_bloco_7():
    # 1. Resultados exibidos
    assert shows_optimal_value() == True
    assert shows_variable_values() == True
    
    # 2. Downloads funcionam
    assert can_download_pyomo_code() == True
    assert can_download_results_json() == True
    
    # 3. Histórico funciona
    assert saves_jobs_to_history() == True
    assert can_reexecute_previous_jobs() == True
```

### 🚀 Resultado Esperado
- Página de resultados completa
- Insights de negócio claros
- Downloads funcionando
- Histórico de jobs operacional

---

## 📋 Bloco 8: Otimizações e Produção (Semana 9-10)

### 🎯 Objetivo
Otimizar performance, adicionar recursos avançados e preparar para produção.

### 📝 Tarefas

#### 8.1 Otimizações de Performance
- [ ] Implementar cache de resultados
- [ ] Otimizar chamadas de API
- [ ] Reduzir tempo de resposta
- [ ] Implementar lazy loading

#### 8.2 Tratamento Robusto de Erros
- [ ] Implementar retry automático
- [ ] Adicionar fallback de solvers
- [ ] Melhorar mensagens de erro
- [ ] Implementar logging detalhado

#### 8.3 Recursos Avançados
- [ ] Adicionar suporte a problemas estocásticos
- [ ] Implementar múltiplos solvers
- [ ] Adicionar templates de problemas
- [ ] Implementar comparação de soluções

#### 8.4 Preparação para Produção
- [ ] Configurar monitoramento
- [ ] Implementar métricas
- [ ] Otimizar para Streamlit Cloud
- [ ] Preparar documentação final

### ✅ Critérios de Sucesso (Testes)
```python
def test_bloco_8():
    # 1. Performance otimizada
    assert response_time_under_30s() == True
    assert cache_works_correctly() == True
    
    # 2. Erros tratados
    assert handles_solver_failures() == True
    assert provides_helpful_error_messages() == True
    
    # 3. Produção pronta
    assert monitoring_configured() == True
    assert documentation_complete() == True
```

### 🚀 Resultado Esperado
- Aplicação otimizada e robusta
- Tratamento completo de erros
- Recursos avançados funcionando
- Pronta para produção

---

## 🧪 Estratégia de Testes

### Testes por Bloco
Cada bloco deve incluir:
1. **Testes unitários** para componentes individuais
2. **Testes de integração** para fluxos completos
3. **Testes de UI** para interface do usuário
4. **Testes de performance** para validação de requisitos

### Critérios de Progressão
Para avançar para o próximo bloco:
- ✅ Todos os testes do bloco atual passando
- ✅ Funcionalidade demonstrada em ambiente de produção
- ✅ Documentação atualizada
- ✅ Código revisado e limpo

### Testes de Regressão
- Manter suite de testes para blocos anteriores
- Executar testes completos antes de cada deploy
- Validar que novas funcionalidades não quebram existentes

---

## 📊 Métricas de Progresso

### Por Bloco
- **Bloco 1**: 12.5% do projeto
- **Bloco 2**: 25% do projeto
- **Bloco 3**: 37.5% do projeto
- **Bloco 4**: 50% do projeto
- **Bloco 5**: 75% do projeto
- **Bloco 6**: 87.5% do projeto
- **Bloco 7**: 100% do projeto
- **Bloco 8**: Otimizações e produção

### Indicadores de Sucesso
- **Funcionalidade**: Cada bloco deve estar 100% funcional
- **Qualidade**: Cobertura de testes >80%
- **Performance**: Tempo de resposta <30s
- **Usabilidade**: Interface intuitiva e responsiva

---

## 🚀 Deploy Contínuo

### Estratégia
- Deploy após cada bloco completo
- Testes automatizados antes do deploy
- Rollback rápido em caso de problemas
- Monitoramento contínuo em produção

### Ambientes
- **Desenvolvimento**: Local para desenvolvimento
- **Staging**: Streamlit Cloud para testes
- **Produção**: Streamlit Cloud para usuários finais

---

## 📝 Checklist de Implementação

### Antes de Começar
- [ ] Ambiente Python configurado
- [ ] Conta OpenAI ativa
- [ ] Conta Streamlit Cloud
- [ ] Repositório Git criado
- [ ] Documentação do blueprint lida

### Durante o Desenvolvimento
- [ ] Seguir ordem dos blocos
- [ ] Testar cada funcionalidade antes de avançar
- [ ] Documentar decisões técnicas
- [ ] Commitar código regularmente
- [ ] Validar critérios de sucesso

### Após Cada Bloco
- [ ] Executar testes completos
- [ ] Deploy e validação em produção
- [ ] Atualizar documentação
- [ ] Revisar código
- [ ] Planejar próximo bloco

---

**Versão**: 1.0  
**Data**: Junho 2025  
**Status**: Pronto para implementação 