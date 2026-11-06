import re
import os
import sys

def extrair_strings_ascii_unicode(caminho_arquivo, min_len=4):
    """
    Simula uma analise estatica de engenharia reversa extraindo strings
    ASCII e UTF-16 (comuns em binarios Windows e assemblies .NET).
    """
    with open(caminho_arquivo, "rb") as f:
        conteudo = f.read()

    # Busca strings ASCII
    padrao_ascii = re.compile(rb"[\x20-\x7E]{" + str(min_len).encode() + rb",}")
    strings_encontradas = [s.decode("latin1", errors="ignore") for s in padrao_ascii.findall(conteudo)]

    return strings_encontradas


def auditar_artefato_compilado(caminho_arquivo):
    print("=" * 70)
    print("TRIAGEM DE SEGURANCA POR ENGENHARIA REVERSA — GuardAI")
    print("=" * 70)
    print(f"[*] Alvo: {caminho_arquivo}")

    if not os.path.exists(caminho_arquivo):
        print(f"[!] Arquivo '{caminho_arquivo}' nao encontrado.")
        return

    strings = extrair_strings_ascii_unicode(caminho_arquivo)
    print(f"[*] Total de strings extraidas: {len(strings)}")

    # Padroes de segredos suspeitos (chaves de licenca, senhas, tokens)
    padroes_risco = [
        r"(TOKEN|SECRET|KEY|PASSWORD|SENHA|API_KEY)",
        r"(GUARD-AI-[A-Z0-9\-]+)"
    ]

    print("\n[*] Resultados da analise estatica de strings e metadados:")
    vulnerabilidades = []

    for s in strings:
        for p in padroes_risco:
            if re.search(p, s, re.IGNORECASE) and len(s) < 80:
                print(f"  [ALERTA CWE-798] String sensivel em texto puro: '{s}'")
                vulnerabilidades.append(s)
                break

    print("\n" + "=" * 70)
    if vulnerabilidades:
        print("[!] DIAGNOSTICO DO GUARDAI:")
        print("  - Vulnerabilidade: CWE-798 (Use of Hardcoded Credentials)")
        print("  - Severidade: ALTA / CRITICA")
        print("  - Causa Raiz: A aplicacao armazena segredos criptograficos diretamente no binario.")
        print("  - Mitigacao: Nunca gravar chaves em constantes de codigo gerenciado ou nativo.")
        print("              Utilizar tokens de curta duracao obtidos via backend autenticado.")
    else:
        print("[+] Nenhum segredo em texto puro identificado.")
    print("=" * 70)


if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "InsecureLicenseManager.cs"
    auditar_artefato_compilado(alvo)
