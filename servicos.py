from banco import conectar

def cadastrar_servico():
    nome = input("Digite o nome do serviço: ")
    valor = float(input(f"Digite o valor do serviço: "))
    duracao = int(input("Digite a duração do serviço (em minutos): ")) 

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO SERVICOS (nome,valor, duracao) VALUES (?,?,?)""", (nome, valor, duracao))
    conn.commit()
    print("Serviço cadastrado com sucesso! ")
    conn.close()

def listar_servicos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicos")
    servicos = cursor.fetchall()

    print("\n=== SERVIÇOS ===")
    print("-"*70)
    print(f"{'ID':<5}{'NOME':<20}{'VALOR':<20}{'DURAÇÃO (min)'}")
    print("-"*70)

    for servico in servicos:
        print(
            f"{servico[0]:<5}"
            f"{servico[1]:<20}"
            f"R${servico[2]:<20.2f}"
            f"{servico[3]}"\
        )
        print("-"*70)
    conn.close()

def excluir_servico():
    id_servico = input("Didite o ID do serviço a ser excluido: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute ("DELETE FROM servicos WHERE id = ?", (id_servico))
    conn.commit()

    if cursor.rowcount > 0:
        print ("Serviço excluido com sucesso.")
    else:
        print("Serviço não encontrado. ")
    conn.close()

def atualizar_servico():
    id_servico = input("Digite o ID do serviço que deseja atualizar: ")
    conn = conectar ()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicos WHERE id = ?" , (id_servico))
    servico = cursor.fetchone()
    if servico:
        print("Cliente encontrado:")
        print(f"ID: {servico[0]}")
        print(f"Nome: {servico[1]}")
        print(f"valor: {servico[2]}")
        print(f"Duração: {servico[3]}")
        novo_nome = input("Digite o novo nome do serviço (deixe em branco para manter o atual): ")
        novo_valor = input("Digite o novo valor do serviço (deixe em branco para manter o atual): ")
        nova_duracao = input("Digite a nova duração do serviço (deixe em branco para manter o atual): ")
        if novo_nome == "":
            novo_nome = servico[1]
        if novo_valor == "":
            novo_valor = servico[2]
        if nova_duracao == "":
            nova_duracao = servico[3]
        cursor.execute("UPDATE servicos SET nome = ?, valor = ?, duracao = ? WHERE id = ?", (novo_nome, novo_valor, nova_duracao, id_servico))
        conn.commit()
    else:
        print("Serviço não encontrado.")

    if cursor.rowcount >0:
        print("Cliente atualizado com sucesso.")
    else:
        print("Nenhuma alteração realizada")
    conn.close()