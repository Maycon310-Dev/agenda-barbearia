from banco import conectar

def cadastrar_cliente_com_usuario():

    usuario = input("Usuário: ")
    senha = input("Senha: ")

    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("Email: ")

    conn = conectar()
    cursor = conn.cursor()

    # cria usuário
    cursor.execute("""
        INSERT INTO usuarios
        (usuario, senha, perfil)
        VALUES (?, ?, ?)
    """, (usuario, senha, "CLIENTE"))

    id_usuario = cursor.lastrowid

    # cria cliente
    cursor.execute("""
        INSERT INTO clientes
        (nome, telefone, email, id_usuario)
        VALUES (?, ?, ?, ?)
    """, (
        nome,
        telefone,
        email,
        id_usuario
    ))

    conn.commit()

    print(f"Cliente {nome} cadastrado com sucesso!")

    conn.close()

def cadastrar_barbeiro_com_usuario():
    
    usuario = input("Usuário: ")
    senha = input("Senha: ")

    nome = input("Nome: ")
    telefone = input("Telefone: ")
    email = input("Email: ")

    conn = conectar()
    cursor = conn.cursor()

    # cria usuário
    cursor.execute("""
        INSERT INTO usuarios
        (usuario, senha, perfil)
        VALUES (?, ?, ?)
    """, (usuario, senha, "BARBEIRO"))

    id_usuario = cursor.lastrowid

    # cria barbeiro
    cursor.execute("""
        INSERT INTO profissionais
        (nome, telefone, email, id_usuario)
        VALUES (?, ?, ?, ?)
    """, (
        nome,
        telefone,
        email,
        id_usuario
    ))

    conn.commit()

    print(f"Barbeiro {nome} cadastrado com sucesso!")

    conn.close()
