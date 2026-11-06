---
name: reverse-engineering-triage
description: Use quando o estudante precisa auditar ou investigar um binário, executável, biblioteca (.dll) ou assembly compilado (.NET / Win32 / ELF) sem acesso direto ao código-fonte original, aplicando técnicas de engenharia reversa estática e descompilação de segurança.
---

# Skill: Triagem e Auditoria por Engenharia Reversa

Esta skill orienta o agente a atuar como um auditor de engenharia reversa e análise de binários para segurança defensiva. Ela é aplicada quando um software precisa ser avaliado e não há código-fonte aberto disponível, ou quando se deseja verificar o que realmente foi empacotado no binário final de produção.

## Princípio Fundamental

Engenharia reversa em segurança não é sobre pirataria ou quebra irresponsável de software; é sobre **verificação de conformidade, análise forense e garantia de integridade**. O agente conduz a análise focando em identificar riscos arquiteturais que o compilador não esconde: segredos embutidos em texto puro, bibliotecas de terceiros desatualizadas e rotinas frágeis de validação.

---

## Passo a Passo da Investigação

### 1. Identificação do Formato e Alvo
Antes de analisar instruções de baixo nível, determine:
- **Formato do arquivo:** PE (Windows .exe/.dll), ELF (Linux), Mach-O (macOS) ou APK/DEX (Android).
- **Runtime:** Código nativo (C/C++, Rust, Go) ou gerenciado (.NET CIL/MSIL, Java Bytecode)?
  - *Dica didática:* Códigos gerenciados (.NET e Java) preservam metadados ricos e podem ser descompilados quase de volta ao código-fonte original (via ferramentas como ILSpy, dnSpy ou Jadx). Códigos nativos exigem desassembladores e descompiladores como Ghidra ou IDA.

---

### 2. Triagem de Superfície (Strings e Metadados)
Incentive o estudante a inspecionar as informações visíveis sem precisar desassemblar todo o binário:
- **Extração de Strings:** Procurar por URLs de endpoints internos, chaves de API embutidas, senhas de banco de dados ou mensagens de erro reveladoras.
- **Tabela de Importação (IAT):** Quais funções da API do sistema o binário chama? (Ex: chamadas para `socket`, `HttpSendRequest`, `VirtualAlloc` ou `SetWindowsHookEx` fornecem pistas claras do comportamento da aplicação).

---

### 3. Análise de Descompilação e Fluxo de Controle
Quando o código é descompilado (por exemplo, inspecionando métodos CIL em C#):
- Localize rotinas de autenticação e validação de licenças/tokens.
- Mostre onde o código comete erros comuns:
  - Validações que podem ser burladas por simples inversão lógica (`if (!isValid)` tornando-se `nop` ou invertido).
  - Algoritmos criptográficos implementados de forma caseira em vez de bibliotecas padrão do sistema.
  - Armazenamento de segredos em constantes do código (`const string MasterKey = "..."`).

---

### 4. Recomendações de Hardening para o Desenvolvedor
A função do mentor é ensinar a proteger o binário legítimo contra engenharia reversa maliciosa:
1. **Nunca coloque segredos no binário:** Chaves privadas e senhas devem ser injetadas via cofres de segredos (Vault / AWS KMS) ou consultadas via backend seguro.
2. **Ofuscação de Código:** Empregar ferramentas de ofuscação de fluxo e renomeação de símbolos para código gerenciado.
3. **Assinatura Digital de Código (Code Signing):** Garantir que qualquer modificação indevida de bytes no binário quebre a assinatura e impeça a execução pelo sistema operacional.
4. **Habilitação de Proteções do Compilador:** Ativar ASLR (Address Space Layout Randomization), DEP/NX e flags de integridade (`/guard:cf`).
