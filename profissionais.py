from banco import conectar

def cadastrar_barbeiro():
    nome = input("Digite o nome do barbeiro: ")
    telefone = (input("Digite o telefone do barbeiro: "))
    email = input("Digite o email do barbeiro: ")

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute ("""INSERT INTO profissionais(nome, telefone, email) VALUES (?,?,?)""", (nome,telefone, email))
    conn.commit ()
    print("Barbeiro cadastrado com sucesso!")
    conn.close()

def listar_barbeiros():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profissionais")
    profissionais = cursor.fetchall()

    print("\n=== BARBEIROS ===")
    print("-" * 70)
    print(f"{'ID':<5}{'NOME':<20}{'TELEFONE':<20}{'EMAIL'}")
    print("-" * 70)

    for barbeiro in profissionais:
        print(
            f"{barbeiro[0]:<5}"
            f"{barbeiro[1]:<20}"
            f"{barbeiro[2]:<20}"
            f"{barbeiro[3]}"
        )
    conn.close()

def buscar_barbeiro():
    id_barbeiro = input("Digite o ID do barbeiro: ")

    conn=conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM profissionais WHERE id = ?" , (id_barbeiro))
    barbeiro = cursor.fetchone()

    if barbeiro:
        print("\n===== Barbeiro encontrado =====")
        print(f"ID: {barbeiro[0]}")
        print(f"Nome: {barbeiro[1]}")
        print(f"Telefone: {barbeiro[2]}")
        print(f"Email: {barbeiro[3]}")
    else:
        print("Barbeiro não encontrado.")
    conn.close()
