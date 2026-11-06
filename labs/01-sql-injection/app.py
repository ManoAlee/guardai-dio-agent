import sqlite3

def inicializar_banco():
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT, perfil TEXT)")
    cursor.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES ('admin', 'Sup3rS3cr3t!', 'Administrador')")
    cursor.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES ('dev_user', 'DevPass123', 'Desenvolvedor')")
    conexao.commit()
    return conexao

def login_vulneravel(conexao, usuario_input, senha_input):
    """
    VULNERABILIDADE: CWE-89 (SQL Injection)
    A query e montada concatenando diretamente a entrada do usuario.
    Um atacante pode manipular a logica booleana com: ' OR '1'='1
    """
    cursor = conexao.cursor()
    query = f"SELECT usuario, perfil FROM usuarios WHERE usuario = '{usuario_input}' AND senha = '{senha_input}'"
    print(f"[DEBUG SQL GERADO]: {query}")
    cursor.execute(query)
    return cursor.fetchone()

if __name__ == "__main__":
    banco = inicializar_banco()
    print("--- Teste de Login Vulneravel ---")
    user = input("Usuario: ") if sys.stdin.isatty() else "admin"
    passw = input("Senha: ") if sys.stdin.isatty() else "Sup3rS3cr3t!"
    resultado = login_vulneravel(banco, user, passw)
    if resultado:
        print(f"[+] Login bem-sucedido! Bem-vindo, {resultado[0]} (Perfil: {resultado[1]})")
    else:
        print("[-] Falha na autenticacao: credenciais invalidas.")
