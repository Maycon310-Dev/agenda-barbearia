from banco import conectar

def cadastrar_usuario():

    usuario = input("Digite o usuário: ")
    senha = input("Digite a senha: ")
    perfil = input("Digite o perfil (ADMIN/BARBEIRO/CLIENTE): ").upper()

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (usuario, senha, perfil)
        VALUES (?, ?, ?)
    """, (usuario, senha, perfil))

    conn.commit()

    print("Usuário cadastrado com sucesso!")

    conn.close()

def listar_usuarios():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")

    usuarios = cursor.fetchall()

    print("\n=== USUÁRIOS ===")

    for usuario in usuarios:

        print("-" * 40)
        print(f"ID: {usuario[0]}")
        print(f"Usuário: {usuario[1]}")
        print(f"Senha: {usuario[2]}")
        print(f"Perfil: {usuario[3]}")

    conn.close()

def buscar_usuario():

    id_usuario = input("Digite o ID do usuário: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE id_usuario = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()

    if usuario:

        print("\n=== USUÁRIO ENCONTRADO ===")

        print(f"ID: {usuario[0]}")
        print(f"Usuário: {usuario[1]}")
        print(f"Senha: {usuario[2]}")
        print(f"Perfil: {usuario[3]}")

    else:

        print("Usuário não encontrado.")

    conn.close()

def excluir_usuario():

    id_usuario = input("Digite o ID do usuário: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM usuarios
        WHERE id_usuario = ?
    """, (id_usuario,))

    conn.commit()

    if cursor.rowcount > 0:
        print("Usuário excluído com sucesso.")
    else:
        print("Usuário não encontrado.")

    conn.close()

def atualizar_usuario():

    id_usuario = input("Digite o ID do usuário: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE id_usuario = ?
    """, (id_usuario,))

    usuario = cursor.fetchone()

    if usuario:

        novo_usuario = input(
            "Novo usuário (ENTER mantém): "
        )

        nova_senha = input(
            "Nova senha (ENTER mantém): "
        )

        novo_perfil = input(
            "Novo perfil (ENTER mantém): "
        )

        if novo_usuario == "":
            novo_usuario = usuario[1]

        if nova_senha == "":
            nova_senha = usuario[2]

        if novo_perfil == "":
            novo_perfil = usuario[3]

        cursor.execute("""
            UPDATE usuarios
            SET usuario = ?,
                senha = ?,
                perfil = ?
            WHERE id_usuario = ?
        """, (
            novo_usuario,
            nova_senha,
            novo_perfil,
            id_usuario
        ))

        conn.commit()

        print("Usuário atualizado com sucesso.")

    else:

        print("Usuário não encontrado.")

    conn.close()
