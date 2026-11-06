# Engenharia Reversa Aplicada à Segurança de Aplicações (AppSec)

Este documento fundamenta a atuação do GuardAI na análise de artefatos compilados, binários nativos e assemblies gerenciados.

---

## 1. Código Gerenciado (.NET CIL) vs. Código Nativo

### Código Gerenciado (.NET C# e Java Bytecode)
- **Como funciona:** O código C# compila para uma linguagem intermediária chamada CIL (Common Intermediate Language) / MSIL, que empacota metadados completos de classes, métodos, nomes de parâmetros e estruturas.
- **Descompilação:** Ferramentas como ILSpy, dnSpy e decompiladores CIL conseguem reconstruir quase 100% da lógica original em C#.
- **Risco de Segurança:** Se um desenvolvedor colocar uma chave privada, senha mestra ou lógica de validação crítica no assembly, qualquer pessoa que tiver o arquivo `.dll` ou `.exe` poderá abrir o descompilador e ler o segredo em texto puro em menos de 10 segundos.

### Código Nativo (C, C++, Rust, Go)
- **Como funciona:** Compila diretamente para instruções de máquina (x86, x64, ARM) e chamadas da API do sistema operacional.
- **Descompilação:** Exige ferramentas como Ghidra ou IDA Pro, que convertem o bytecode binário em pseudocódigo C aproximado.
- **Risco de Segurança:** Erros de gerenciamento manual de memória, como estouro de buffer (Buffer Overflow), uso após liberação (Use-After-Free) e estouro de inteiros.

---

## 2. Padrões de Falhas Descobertas via Engenharia Reversa

1. **CWE-798: Uso de Credenciais Embutidas (Hardcoded Credentials)**
   - Ocorre quando tokens de autenticação, senhas de banco ou chaves de criptografia estão escritas como constantes no código compilado.
2. **CWE-603: Mecanismo de Autenticação Inseguro no Lado do Cliente**
   - Validações que tomam a decisão final de permitir ou negar acesso dentro do binário cliente, permitindo que a inversão de um único byte de instrução (`jne` para `je`) burle todo o sistema.
3. **CWE-242: Uso de Funções Inseguras da API do Sistema**
   - Binários que chamam funções depreciadas de manipulação de strings (`strcpy`, `sprintf`, `gets`) vulneráveis a corrupção de memória.

---

## 3. Diretrizes de Hardening para Desenvolvedores

- **Externalização de Segredos:** Utilize cofres de chaves (HashiCorp Vault, Azure Key Vault, AWS Secrets Manager).
- **Validação Centralizada no Servidor:** A regra de negócio e a decisão de acesso pertencem exclusivamente ao backend corporativo, nunca ao cliente compilado.
- **Ofuscação de Assemblies:** Para aplicações de desktop ou mobile, utilize ferramentas que transformem nomes de classes e métodos em caracteres aleatórios e quebrem o fluxo linear de controle.
- **Assinatura Digital (Code Signing):** Garanta a integridade do executável com certificados digitais válidos, permitindo que o sistema operacional impeça a execução de binários modificados.
