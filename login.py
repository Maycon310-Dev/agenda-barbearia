from banco import conectar

def login():

    print("=" * 7, "LOGIN", "=" * 7)

    usuario = input("Digite o seu nome de usuário: ")
    senha = input("Digite sua senha: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario = ?
        AND senha = ?
    """, (usuario, senha))

    usuario_encontrado = cursor.fetchone()

    conn.close()

    if usuario_encontrado:

        print("Login realizado com sucesso!")

        return usuario_encontrado

    else:

        print("Usuário ou senha incorretos.")

        return None