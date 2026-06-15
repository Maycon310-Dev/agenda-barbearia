from banco import conectar

def agendar_horario():

    cliente_id = input("Digite o ID do cliente: ")
    profissional_id = input("Digite o ID do barbeiro: ")
    servico_id = input("Digite o ID do serviço: ")
    data = input("Digite a data (dd/mm/aaaa): ")
    hora = input("Digite a hora (hh:mm): ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM agendamentos
        WHERE profissional_id = ?
        AND data = ?
        AND hora = ?
    """, (
        profissional_id,
        data,
        hora
    ))

    conflito = cursor.fetchone()

    if conflito:
        print("Horário já está ocupado!")

    else:
        cursor.execute("""
            INSERT INTO agendamentos
            (
                cliente_id,
                profissional_id,
                servico_id,
                data,
                hora
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            cliente_id,
            profissional_id,
            servico_id,
            data,
            hora
        ))

        conn.commit()

        print("Agendamento realizado com sucesso!")

    conn.close()
    
def listar_agendamentos():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM agendamentos")

    agendamentos = cursor.fetchall()

    print("\n=== AGENDAMENTOS ===")

    for agendamento in agendamentos:
        print("-" * 40)
        print(f"ID Agendamento: {agendamento[0]}")
        print(f"Cliente ID: {agendamento[1]}")
        print(f"Barbeiro ID: {agendamento[2]}")
        print(f"Serviço ID: {agendamento[3]}")
        print(f"Data: {agendamento[4]}")
        print(f"Hora: {agendamento[5]}")
        print(f"Status: {agendamento[6]}")

    conn.close()

def cancelar_agendamento():
    id_agendamento = input("Digite o ID de agendamento para cancelamento: ")
    conn = conectar()
    cursor= conn.cursor()

    cursor.execute ("DELETE FROM agendamentos WHERE id = ?" , (id_agendamento,))
    conn.commit()

    if cursor.rowcount > 0:
        print ("Agendamento excluido com sucesso.")
    else:
        print("Agendamento não encontrado. ")
    conn.close()

def buscar_agendamento():
    id_agendamento = input("Digite o ID do agendamento: ")

    conn = conectar()
    cursor =conn.cursor()

    cursor.execute(
        "SELECT * FROM agendamentos WHERE id = ?" , (id_agendamento,))
    
    agendamento = cursor.fetchone()

    if agendamento:
        print("-" * 40)
        print(f"ID Agendamento: {agendamento[0]}")
        print(f"Cliente ID: {agendamento[1]}")
        print(f"Barbeiro ID: {agendamento[2]}")
        print(f"Serviço ID: {agendamento[3]}")
        print(f"Data: {agendamento[4]}")
        print(f"Hora: {agendamento[5]}")
        print(f"Status: {agendamento[6]}")

    else :
        print("Agendamento não encontrado! ")

    conn.close()

def atualizar_agendamento():

    id_agendamento = input("Digite o ID do agendamento a ser atualizado: ")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM agendamentos WHERE id = ?",
        (id_agendamento,)
    )

    agendamento = cursor.fetchone()

    if agendamento:

        print("\n=== AGENDAMENTO ENCONTRADO ===")
        print(f"ID: {agendamento[0]}")
        print(f"Cliente ID: {agendamento[1]}")
        print(f"Barbeiro ID: {agendamento[2]}")
        print(f"Serviço ID: {agendamento[3]}")
        print(f"Data: {agendamento[4]}")
        print(f"Hora: {agendamento[5]}")
        print(f"Status: {agendamento[6]}")

        novo_cliente = input(
            "Novo ID do cliente (ENTER para manter): "
        )

        novo_barbeiro = input(
            "Novo ID do barbeiro (ENTER para manter): "
        )

        novo_servico = input(
            "Novo ID do serviço (ENTER para manter): "
        )

        nova_data = input(
            "Nova data (ENTER para manter): "
        )

        nova_hora = input(
            "Nova hora (ENTER para manter): "
        )

        novo_status = input(
            "Novo status (ENTER para manter): "
        )

        if novo_cliente == "":
            novo_cliente = agendamento[1]

        if novo_barbeiro == "":
            novo_barbeiro = agendamento[2]

        if novo_servico == "":
            novo_servico = agendamento[3]

        if nova_data == "":
            nova_data = agendamento[4]

        if nova_hora == "":
            nova_hora = agendamento[5]

        if novo_status == "":
            novo_status = agendamento[6]

        cursor.execute("""
            UPDATE agendamentos
            SET
                cliente_id = ?,
                profissional_id = ?,
                servico_id = ?,
                data = ?,
                hora = ?,
                status = ?
            WHERE id = ?
        """, (
            novo_cliente,
            novo_barbeiro,
            novo_servico,
            nova_data,
            nova_hora,
            novo_status,
            id_agendamento
        ))

        conn.commit()

        if cursor.rowcount > 0:
            print("Agendamento atualizado com sucesso!")
        else:
            print("Nenhuma alteração realizada.")

    else:
        print("Agendamento não encontrado.")

    conn.close()

def listar_agendamentoJoin():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        ag.id,
        cli.nome AS cliente,
        prof.nome AS barbeiro,
        serv.nome AS servico,
        ag.data,
        ag.hora,
        ag.status

    FROM agendamentos ag

    INNER JOIN clientes cli
        ON ag.cliente_id = cli.id

    INNER JOIN profissionais prof
        ON ag.profissional_id = prof.id

    INNER JOIN servicos serv
        ON ag.servico_id = serv.id
""")

    agendamentos = cursor.fetchall()

    print("\n=== AGENDAMENTOS ===")
    print("-" * 90)

    for agendamento in agendamentos:

        print(f"ID: {agendamento[0]}")
        print(f"Cliente: {agendamento[1]}")
        print(f"Barbeiro: {agendamento[2]}")
        print(f"Serviço: {agendamento[3]}")
        print(f"Data: {agendamento[4]}")
        print(f"Hora: {agendamento[5]}")
        print(f"Status: {agendamento[6]}")
        print("-" * 90)

    conn.close()