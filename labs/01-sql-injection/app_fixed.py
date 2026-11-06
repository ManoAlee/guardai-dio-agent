import sqlite3

def inicializar_banco():
    conexao = sqlite3.connect(":memory:")
    cursor = conexao.cursor()
    cursor.execute("CREATE TABLE usuarios (id INTEGER PRIMARY KEY, usuario TEXT, senha TEXT, perfil TEXT)")
    cursor.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES ('admin', 'Sup3rS3cr3t!', 'Administrador')")
    cursor.execute("INSERT INTO usuarios (usuario, senha, perfil) VALUES ('dev_user', 'DevPass123', 'Desenvolvedor')")
    conexao.commit()
    return conexao

def login_seguro(conexao, usuario_input, senha_input):
    """
    CORRECAO SEGURA: Prepared Statements / Consultas Parametrizadas
    O motor do banco de dados trata usuario_input e senha_input puramente como dados literais,
    nunca como codigo executavel. O SQL Injection e neutralizado.
    """
    cursor = conexao.cursor()
    query = "SELECT usuario, perfil FROM usuarios WHERE usuario = ? AND senha = ?"
    print(f"[DEBUG SQL SEGURO]: {query} | Parametros: ({usuario_input}, [OCULTO])")
    cursor.execute(query, (usuario_input, senha_input))
    return cursor.fetchone()

if __name__ == "__main__":
    banco = inicializar_banco()
    print("--- Teste de Login Seguro ---")
    resultado = login_seguro(banco, "admin", "Sup3rS3cr3t!")
    if resultado:
        print(f"[+] Login bem-sucedido! Bem-vindo, {resultado[0]} (Perfil: {resultado[1]})")
    else:
        print("[-] Falha na autenticacao: credenciais invalidas.")
