# Fundamentos de Segurança da Informação e AppSec

Este documento contém os conceitos essenciais de segurança da informação e segurança de aplicações (AppSec) utilizados pelo GuardAI.

---

## 1. Tríade Fundamental: Vulnerabilidade, Ameaça e Risco

- **Vulnerabilidade:** Uma fraqueza ou brecha no software, sistema operacional, protocolo ou configuração que pode ser explorada. Exemplo: um campo de texto que não valida caracteres especiais e concatena strings direto no SQL.
- **Ameaça (Threat):** Qualquer agente ou evento com potencial de explorar intencionalmente uma vulnerabilidade. Exemplo: um cibercriminoso, um bot automatizado de varredura ou um insider mal-intencionado.
- **Risco:** O impacto potencial resultante da concretização da ameaça explorando a vulnerabilidade.
  $$\text{Risco} = \text{Probabilidade} \times \text{Impacto}$$

---

## 2. A Tríade CIA (PILAR DA SEGURANÇA)

Toda análise de vulnerabilidade deve avaliar o impacto nos três pilares fundamentais:

- **Confidencialidade (Confidentiality):** Apenas pessoas e processos autorizados podem acessar os dados. Violada em vazamentos de dados, SQL Injection lendo senhas, e exfiltração por keylogger.
- **Integridade (Integrity):** Os dados e sistemas permanecem exatos, autênticos e livres de modificações não autorizadas. Violada quando um atacante altera valores no banco ou adultera binários.
- **Disponibilidade (Availability):** Os sistemas, serviços e dados estão operacionais e acessíveis quando solicitados pelos usuários legítimos. Violada por ataques de negação de serviço (DoS/DDoS) e criptografia por Ransomware.

---

## 3. Taxonomias de Mercado

- **OWASP Top 10:** As dez categorias de vulnerabilidades mais críticas em aplicações web (ex: *A01: Broken Access Control*, *A03: Injection*).
- **CWE (Common Weakness Enumeration):** Um catálogo padronizado com identificadores numéricos para tipos de fraquezas de software (ex: `CWE-89` para SQL Injection, `CWE-79` para XSS, `CWE-798` para Hardcoded Credentials).
- **MITRE ATT&CK:** Uma base de conhecimento global que mapeia táticas, técnicas e procedimentos (TTPs) reais utilizados por atacantes (ex: `T1190: Exploit Public-Facing Application`).

---

## 4. Princípios de Codificação Segura (Secure Coding)

1. **Nunca Confie na Entrada do Usuário:** Toda informação recebida via HTTP, parâmetros de URL, cabeçalhos, arquivos ou formulários é potencialmente hostil.
2. **Defesa em Profundidade (Defense in Depth):** Não dependa de uma única barreira. Combine validação no front-end, sanitização no back-end, WAF na rede e permissões mínimas no banco de dados.
3. **Princípio do Menor Privilégio (PoLP):** Aplicações e conexões de banco de dados devem rodar apenas com as permissões estritamente necessárias para sua operação.
4. **Tratamento Seguro de Falhas (Fail-Safe Defaults):** Em caso de erro, a aplicação deve falhar de forma fechada (acesso negado por padrão) e nunca expor stack traces ou mensagens internas do banco de dados ao usuário final.
