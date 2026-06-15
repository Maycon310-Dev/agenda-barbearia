from banco import conectar

def cadastrar_cliente():
    nome = input("Digite o nome do cliente: ")
    telefone = input("Digite o telefone do cliente: ") 
    email = input("Digite o email do cliente: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO CLIENTES (nome, telefone, email) VALUES (?,?,?)""", (nome, telefone, email))
    conn.commit()
    print("Cliente cadastrado com sucesso!")
    conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()

    print("\n=== CLIENTES ===")
    print("-" * 70)
    print(f"{'ID':<5}{'NOME':<20}{'TELEFONE':<20}{'EMAIL'}")
    print("-" * 70)

    for cliente in clientes:
        print(
            f"{cliente[0]:<5}"
            f"{cliente[1]:<20}"
            f"{cliente[2]:<20}"
            f"{cliente[3]}"
        )
    conn.close()

def buscar_cliente():
    id_cliente = input("Digite o ID do cliente: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM clientes WHERE id = ?", (id_cliente,))

    cliente = cursor.fetchone()

    if cliente:
        print("\n===== Cliente encontrado =====")
        print(f"ID: {cliente[0]}")
        print(f"Nome: {cliente[1]}")
        print(f"Telefone: {cliente[2]}")
        print(f"Email: {cliente[3]}")
    
    conn.close()

def excluir_cliente():
    id_cliente = input("Digite o ID do cliente a ser excluído: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = ?", (id_cliente,))
    conn.commit()

    if cursor.rowcount > 0:
        print("Cliente excluído com sucesso.")
    else:
        print("Cliente não encontrado.")
        
    conn.close()

def atualizar_cliente():
    id_cliente = input("Digite o ID do cliente a ser atualizado:")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes WHERE id = ?", (id_cliente,))
    cliente = cursor.fetchone()
    if cliente:
        print("Cliente encontrado:")
        print(f"ID: {cliente[0]}")
        print(f"Nome: {cliente[1]}")
        print(f"Telefone: {cliente[2]}")
        print(f"Email: {cliente[3]}")
        novo_nome = input("Digite o novo nome do cliente (deixe em branco para manter o atual): ")
        novo_telefone = input("Digite o novo telefone do cliente (deixe em branco para manter o atual): ")
        novo_email = input("Digite o novo email do cliente (deixe em branco para manter o atual): ")
        if novo_nome == "":
            novo_nome = cliente[1]
        if novo_telefone == "":
            novo_telefone = cliente[2]
        if novo_email == "":
            novo_email = cliente[3]
        cursor.execute("UPDATE clientes SET nome = ?, telefone = ?, email = ? WHERE id = ?", (novo_nome, novo_telefone, novo_email, id_cliente))
        conn.commit()
        print("Cliente atualizado com sucesso.")
    else:
        print("Cliente não encontrado.")

    if cursor.rowcount > 0:
        print("Cliente atualizado com sucesso.")
    else:
        print("Nenhuma alteração realizada.")
    conn.close()