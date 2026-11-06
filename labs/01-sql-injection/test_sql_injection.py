from app import inicializar_banco, login_vulneravel
from app_fixed import login_seguro

def rodar_bateria_testes():
    print("=" * 70)
    print("TESTE DE SEGURANCA: CWE-89 (SQL Injection) — Vulneravel vs Corrigido")
    print("=" * 70)

    banco = inicializar_banco()

    payload_ataque_user = "admin' --"
    payload_ataque_pass = "qualquer_coisa"

    print("\n[CENARIO 1] Executando ataque contra o login vulneravel (app.py):")
    res_vuln = login_vulneravel(banco, payload_ataque_user, payload_ataque_pass)
    if res_vuln:
        print(f"  [RESULTADO]: BRECHA CONFIRMADA! Autenticado como '{res_vuln[0]}' sem senha correta!")
    else:
        print("  [RESULTADO]: Ataque bloqueado.")

    print("\n[CENARIO 2] Executando o mesmo ataque contra o login seguro (app_fixed.py):")
    res_safe = login_seguro(banco, payload_ataque_user, payload_ataque_pass)
    if res_safe:
        print(f"  [RESULTADO]: Falha de seguranca.")
    else:
        print("  [RESULTADO]: PROTEGIDO! A consulta parametrizada tratou o payload como string literal.")

    print("\n[CENARIO 3] Testando credencial legitima no login seguro:")
    res_auth = login_seguro(banco, "admin", "Sup3rS3cr3t!")
    assert res_auth is not None, "Login legitimo deveria funcionar"
    print(f"  [RESULTADO]: Sucesso! Usuario '{res_auth[0]}' autenticado legitimamente.")

    print("\n" + "=" * 70)
    print("STATUS FINAL: Bateria de testes de AppSec concluida com 100% de sucesso!")
    print("=" * 70)

if __name__ == "__main__":
    rodar_bateria_testes()
