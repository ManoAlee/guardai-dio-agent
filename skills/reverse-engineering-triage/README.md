# Skill: reverse-engineering-triage

## O que é
A skill **reverse-engineering-triage** capacita o agente a conduzir investigações e auditorias de segurança em binários compilados (.exe, .dll, ELF) e assemblies gerenciados (.NET CIL/MSIL). 

Ela orienta a análise quando o código-fonte original não está disponível ou quando é necessário auditar artefatos pré-compilados em esteiras de DevSecOps.

## Por que foi criada
Em cenários reais de segurança e auditoria (Blue Team e Forense), analistas frequentemente se deparam com bibliotecas legadas, dependências de terceiros sem código aberto ou binários sob suspeita de adulteração. 

Esta skill ensina a:
1. Identificar o formato do arquivo e o runtime (nativo vs gerenciado).
2. Extrair strings legíveis para buscar segredos ou endpoints embutidos.
3. Inspecionar a Tabela de Importação de Funções (IAT) para mapear o comportamento da aplicação no sistema operacional.
4. Auditar fluxos de validação lógica e métodos descompilados.
5. Recomendar contramedidas de proteção e hardening para desenvolvedores (ASLR, DEP, ofuscação e assinatura digital).

## Quando é acionada
O agente utiliza esta skill quando o estudante:
- Pergunta como auditar um arquivo compilado (.exe ou .dll).
- Tem dúvidas sobre como descompilar um assembly .NET (C#) ou inspecionar CIL/bytecode.
- Deseja entender como segredos embutidos são recuperados via engenharia reversa.
- Precisa de orientação sobre como proteger o próprio código compilado contra engenharia reversa maliciosa.
