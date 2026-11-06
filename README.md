# GuardAI: Especialização do DIO Agent para Cibersegurança e AppSec
*Projeto prático desenvolvido para o Bootcamp Santander Cibersegurança — DIO*

Este repositório documenta a evolução do **DIO Agent** na persona especializada **GuardAI**: um mentor de cibersegurança e Application Security (AppSec) capaz de auditar códigos, avaliar riscos na Tríade CIA e orientar correções de forma investigativa, sem entregar respostas cegas para copiar e colar.

Diferente de um modelo de linguagem genérico que cospe blocos de código sem critério, o GuardAI foi arquitetado com base em arquivos de instrução e governança (`AGENTS.md`, `persona.md`, `knowledge/` e `skills/`). Nenhum peso de rede neural foi treinado: o agente aprendeu novos comportamentos exclusivamente por meio de contexto estruturado.

---

## 1. Por que a Especialização foi Criada

Em ambientes corporativos reais, a pessoa analista de segurança não chega dizendo "troque a linha 10 por isso". Ela precisa entender:
- Onde a aplicação roda (serviço interno ou exposto na borda da internet)?
- Qual o tipo e a criticidade dos dados manipulados?
- Qual o impacto real no negócio caso a falha seja explorada?

O objetivo desta especialização foi conferir ao agente a maturidade de um profissional sênior de segurança defensiva: ele faz perguntas de contexto antes de sugerir comandos, categoriza a ameaça por taxonomias padronizadas (CWE e MITRE ATT&CK) e ensina o desenvolvedor a corrigir a causa raiz.

---

## 2. Mapa de Arquivos Criados e Alterados

| Arquivo | Tipo | Descrição / Papel no Agente |
|---|---|---|
| `AGENTS.md` | Alterado | Fonte única de verdade do agente; registra as novas bases de conhecimento e a tabela de skills. |
| `agent/persona.md` | Alterado | Ajusta a identidade para o perfil de mentor AppSec, estabelecendo postura didática e investigativa. |
| `agent/knowledge/security-basics.md` | Criado | Fundamentos de segurança: Vulnerabilidade vs Ameaça vs Risco, Tríade CIA, CWE e OWASP. |
| `agent/knowledge/reverse-engineering-appsec.md` | Criado | Conhecimento avançado sobre descompilação de código gerenciado (.NET/CIL), nativo e hardening. |
| `skills/vulnerability-analysis/SKILL.md` | Criado | Roteiro do agente para conduzir auditorias de código e matriz de severidade. |
| `skills/vulnerability-analysis/README.md` | Criado | Documentação humana explicando o propósito e quando a skill entra em ação. |
| `skills/reverse-engineering-triage/SKILL.md` | Criado | Roteiro para triagem e auditoria de binários compilados (.exe/.dll) via descompilação estática. |
| `skills/reverse-engineering-triage/README.md` | Criado | Documentação humana sobre a skill de engenharia reversa para segurança. |
| `labs/01-sql-injection/` | Criado | Laboratório prático de SQL Injection (`app.py`, `app_fixed.py` e testes automatizados). |
| `labs/02-reverse-engineering/` | Criado | Laboratório de engenharia reversa com código C# (`InsecureLicenseManager.cs`) e auditor estático. |

---

## 3. Melhoria Escolhida: Triagem por Engenharia Reversa

Além do escopo básico solicitado no desafio (análise de SQL Injection em código-fonte), foi adicionada uma segunda capacidade de alto valor técnico: **Engenharia Reversa para Segurança de Aplicações**.

Muitas vezes o time de segurança precisa auditar pacotes de terceiros, bibliotecas legadas ou executáveis compilados em que o código-fonte original não está acessível. A skill `reverse-engineering-triage` orienta o agente a:
1. Identificar se o alvo é código gerenciado (.NET CIL / Java Bytecode) ou código nativo.
2. Inspecionar strings e tabelas de importação (IAT) em busca de segredos em texto puro (`CWE-798`).
3. Avaliar fluxos de validação lógica no cliente (`CWE-603`) e recomendar técnicas de hardening (ofuscação, assinaturas de código e validação centralizada em backend).

---

## 4. Laboratórios Práticos Desenvolvidos

### Laboratório 1: Detecção e Mitigação de SQL Injection (`labs/01-sql-injection/`)
Demonstração de uma rota de autenticação vulnerável a injeção SQL clássica (`CWE-89` / MITRE `T1190`):

- **Código Vulnerável (`app.py`):** Concatenação direta de strings na query SQL.
  ```python
  query = f"SELECT usuario, perfil FROM usuarios WHERE usuario = '{usuario_input}' AND senha = '{senha_input}'"
  ```
- **Código Mitigado (`app_fixed.py`):** Utilização de consultas parametrizadas (*Prepared Statements*).
  ```python
  query = "SELECT usuario, perfil FROM usuarios WHERE usuario = ? AND senha = ?"
  cursor.execute(query, (usuario_input, senha_input))
  ```
- **Evidência do Teste Automatizado (`test_sql_injection.py`):**
  ```text
  [CENARIO 1] Executando ataque contra o login vulneravel (app.py):
  [DEBUG SQL GERADO]: SELECT usuario, perfil FROM usuarios WHERE usuario = 'admin' --' AND senha = '...'
    [RESULTADO]: BRECHA CONFIRMADA! Autenticado como 'admin' sem senha correta!

  [CENARIO 2] Executando o mesmo ataque contra o login seguro (app_fixed.py):
  [DEBUG SQL SEGURO]: SELECT usuario, perfil FROM usuarios WHERE usuario = ? AND senha = ?
    [RESULTADO]: PROTEGIDO! A consulta parametrizada tratou o payload como string literal.
  ```

---

### Laboratório 2: Auditoria de Binário Compilado via Engenharia Reversa (`labs/02-reverse-engineering/`)
Demonstração de como compiladores preservam constantes e metadados que revelam chaves estáticas:

- **Código C# (`InsecureLicenseManager.cs`):** Validação de acesso baseada em constante estática.
- **Auditoria de Descompilação (`audit_binary.py`):**
  ```text
  [*] Resultados da analise estatica de strings e metadados:
    [ALERTA CWE-798] String sensivel em texto puro: 'return key == MASTER_SECRET_KEY;'
  [!] DIAGNOSTICO DO GUARDAI:
    - Vulnerabilidade: CWE-798 (Use of Hardcoded Credentials)
    - Severidade: ALTA / CRITICA
    - Mitigacao: Nunca gravar chaves em constantes de binarios. Utilizar tokens efemeros via KMS.
  ```

---

## 5. Comparativo: Chat Genérico vs. GuardAI Especializado

| Cenário de Teste | Resposta de um Chatbot Genérico | Comportamento do GuardAI (com a Skill) |
|---|---|---|
| **Usuário envia código vulnerável** | Cospe imediatamente o código corrigido e manda copiar. | Pergunta onde o código roda e quais dados ele trafega antes de opinar. |
| **Classificação de Risco** | "Isso é perigoso." | Mapeia o CWE-89, associa à técnica MITRE ATT&CK T1190 e analisa a Tríade CIA. |
| **Condução Pedagógica** | Resolve o problema pelo usuário. | Explica o conceito de *Prepared Statements* e estimula o estudante a propor a correção. |

---

## 6. Como Executar o Agente no Hermes

1. Instale o **Hermes** conforme a documentação oficial da DIO.
2. Abra o terminal exatamente na pasta raiz deste repositório:
   ```bash
   cd dio-agent-guardai
   ```
3. Inicie o agente pelo terminal:
   ```bash
   hermes
   ```
4. Converse naturalmente:
   > *"Olá! Tenho uma função de login em Python que recebe dados de um formulário e faz um SELECT no SQLite. Como posso saber se ela está segura?"*
5. Observe o GuardAI aplicando a skill `vulnerability-analysis`, fazendo as perguntas de contexto antes de qualquer julgamento.
