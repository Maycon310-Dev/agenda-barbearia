from banco import conectar
from profissionais import (listar_barbeiros)
from servicos import (listar_servicos)
from datetime import datetime, timedelta

def agendar_horario(id_usuario):

    print("\n=== BARBEIROS DISPONÍVEIS ===")
    listar_barbeiros()

    print("\n=== SERVIÇOS DISPONÍVEIS ===")
    listar_servicos()
    
    print("\n=== BARBEIROS DISPONÍVEIS ===")
    listar_barbeiros()

    id_barbeiro = input("Digite o ID do barbeiro: ")

    print("\n=== SERVIÇOS DISPONÍVEIS ===")
    listar_servicos()

    id_servico = input("Digite o ID do serviço: ")

    data = input("Digite a data (dd/mm/aaaa): ")

    horarios_livres = mostrar_horarios_disponiveis(
        id_barbeiro,
        data
    )

    hora = input("Digite a hora (hh:mm): ")

    if hora not in horarios_livres:

        print("Escolha um horário disponível da lista!")
        return
    # ==========================
    # VALIDAÇÃO DA DATA
    # ==========================

    try:

        data_agendamento = datetime.strptime(
            data,
            "%d/%m/%Y"
        )

    except ValueError:

        print("Data inválida!")
        return

    dia_semana = data_agendamento.weekday()

    if dia_semana == 0:
        print("A barbearia não funciona às segundas-feiras!")
        return

    if dia_semana == 6:
        print("A barbearia não funciona aos domingos!")
        return

    hoje = datetime.now()

    if data_agendamento.date() < hoje.date():
        print("Não é possível agendar em datas passadas!")
        return

    # ==========================
    # VALIDAÇÃO DA HORA
    # ==========================

    try:

        hora_agendamento = datetime.strptime(
            hora,
            "%H:%M"
        )

    except ValueError:

        print("Hora inválida!")
        return

    # ==========================
    # REGRAS DE FUNCIONAMENTO
    # ==========================

    # Sábado
    if dia_semana == 5:

        if hora_agendamento.hour < 8 or hora_agendamento.hour > 17:

            print("Aos sábados atendemos apenas das 08:00 às 17:00!")
            return

    # Terça a Sexta
    elif dia_semana in [1, 2, 3, 4]:

        if hora_agendamento.hour < 8 or hora_agendamento.hour > 19:

            print("Horário fora do expediente!")
            return

    conn = conectar()
    cursor = conn.cursor()

    # ==========================
    # CLIENTE LOGADO
    # ==========================

    cursor.execute("""
        SELECT id
        FROM clientes
        WHERE id_usuario = ?
    """, (id_usuario,))

    cliente = cursor.fetchone()

    if not cliente:
        print("Cliente não encontrado!")
        conn.close()
        return

    id_cliente = cliente[0]

    # ==========================
    # VERIFICA BARBEIRO
    # ==========================

    cursor.execute("""
        SELECT id
        FROM profissionais
        WHERE id = ?
    """, (id_barbeiro,))

    profissional = cursor.fetchone()

    if not profissional:
        print("Barbeiro não encontrado!")
        conn.close()
        return

    # ==========================
    # VERIFICA SERVIÇO
    # ==========================

    cursor.execute("""
        SELECT id
        FROM servicos
        WHERE id = ?
    """, (id_servico,))

    servico = cursor.fetchone()

    if not servico:
        print("Serviço não encontrado!")
        conn.close()
        return
    
    # Busca a duração do serviço

    cursor.execute("""
        SELECT duracao
        FROM servicos
        WHERE id = ?
    """, (id_servico,))

    duracao_servico = cursor.fetchone()[0]

    inicio_novo = datetime.strptime(
    f"{data} {hora}",
    "%d/%m/%Y %H:%M"
    )

    fim_novo = inicio_novo + timedelta(
    minutes=duracao_servico
    )

    print(f"Serviço selecionado: {duracao_servico} minutos")

# ==========================
# VERIFICA CONFLITO
# ==========================

    cursor.execute("""
    SELECT
        ag.hora,
        serv.duracao

    FROM agendamentos ag

    INNER JOIN servicos serv
        ON ag.id_servico = serv.id

    WHERE ag.id_barbeiro = ?
    AND ag.data = ?
    """, (
        id_barbeiro,
        data
    ))

    agendamentos_existentes = cursor.fetchall()


    conflito = False

    for hora_existente, duracao_existente in agendamentos_existentes:

        inicio_existente = datetime.strptime(
            f"{data} {hora_existente}",
            "%d/%m/%Y %H:%M"
        )

        fim_existente = inicio_existente + timedelta(
            minutes=duracao_existente
        )


        if (
            inicio_novo < fim_existente
            and
            fim_novo > inicio_existente
        ):
            conflito = True
            break

    if conflito:

        print("Horário já está ocupado!")

    else:

        cursor.execute("""
            INSERT INTO agendamentos
            (
                id_cliente,
                id_barbeiro,
                id_servico,
                data,
                hora
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            id_cliente,
            id_barbeiro,
            id_servico,
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

def cancelar_agendamento(id_usuario):

    conn = conectar()
    cursor = conn.cursor()

    # Descobre o cliente logado

    cursor.execute("""
        SELECT id
        FROM clientes
        WHERE id_usuario = ?
    """, (id_usuario,))

    cliente = cursor.fetchone()

    if not cliente:

        print("Cliente não encontrado!")
        conn.close()
        return

    id_cliente = cliente[0]

    # Lista apenas os agendamentos dele

    cursor.execute("""
        SELECT
            ag.id,
            serv.nome,
            ag.data,
            ag.hora

        FROM agendamentos ag

        INNER JOIN servicos serv
            ON ag.id_servico = serv.id

        WHERE ag.id_cliente = ?
    """, (id_cliente,))

    agendamentos = cursor.fetchall()

    if not agendamentos:

        print("Você não possui agendamentos.")
        conn.close()
        return

    print("\n=== SEUS AGENDAMENTOS ===")

    for agendamento in agendamentos:

        print(
            f"ID: {agendamento[0]} | "
            f"{agendamento[1]} | "
            f"{agendamento[2]} | "
            f"{agendamento[3]}"
        )

    id_agendamento = input(
        "\nDigite o ID do agendamento para cancelar: "
    )

    cursor.execute("""
        DELETE FROM agendamentos
        WHERE id = ?
        AND id_cliente = ?
    """, (
        id_agendamento,
        id_cliente
    ))

    conn.commit()

    if cursor.rowcount > 0:

        print("Agendamento cancelado com sucesso!")

    else:

        print("Agendamento não encontrado!")

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
                id_cliente = ?,
                id_barbeiro = ?,
                id_servico = ?,
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

def atualizar_meu_agendamento(id_usuario):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id
        FROM clientes
        WHERE id_usuario = ?
    """, (id_usuario,))

    cliente = cursor.fetchone()

    if not cliente:

        print("Cliente não encontrado!")
        conn.close()
        return

    id_cliente = cliente[0]

    cursor.execute("""
        SELECT
            ag.id,
            serv.nome,
            ag.data,
            ag.hora

        FROM agendamentos ag

        INNER JOIN servicos serv
            ON ag.id_servico = serv.id

        WHERE ag.id_cliente = ?
    """, (id_cliente,))

    agendamentos = cursor.fetchall()

    if not agendamentos:

        print("Você não possui agendamentos.")
        conn.close()
        return

    print("\n=== SEUS AGENDAMENTOS ===")

    for agendamento in agendamentos:

        print(
            f"ID: {agendamento[0]} | "
            f"{agendamento[1]} | "
            f"{agendamento[2]} | "
            f"{agendamento[3]}"
        )

    id_agendamento = input(
        "\nDigite o ID do agendamento para atualizar: "
    )
    cursor.execute("""
        SELECT *
        FROM agendamentos
        WHERE id = ?
        AND id_cliente = ?
    """, (
        id_agendamento,
        id_cliente
    ))

    agendamento = cursor.fetchone()

    if not agendamento:

        print("Agendamento não encontrado!")
        conn.close()
        return
    
    print("\n=== DADOS ATUAIS ===")
    print(f"Data: {agendamento[4]}")
    print(f"Hora: {agendamento[5]}")

    nova_data = input(
        "\nDigite a nova data (dd/mm/aaaa): "
    )
    mostrar_horarios_disponiveis(
    agendamento[2],
    nova_data
    )

    nova_hora = input(
    "\nDigite a nova hora (hh:mm): "
    )
    cursor.execute("""
        UPDATE agendamentos
        SET
            data = ?,
            hora = ?
        WHERE id = ?
    """, (
        nova_data,
        nova_hora,
        id_agendamento
    ))

    conn.commit()

    if cursor.rowcount > 0:

        print(
            "Agendamento atualizado com sucesso!"
        )

    else:

        print(
            "Nenhuma alteração realizada."
        )

    conn.close()


def listar_agendamentoJoin(id_usuario=None, perfil=None):

    conn = conectar()
    cursor = conn.cursor()

    if perfil == "CLIENTE":

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
            ON ag.id_cliente = cli.id

        INNER JOIN profissionais prof
            ON ag.id_barbeiro = prof.id

        INNER JOIN servicos serv
            ON ag.id_servico = serv.id

        WHERE cli.id_usuario = ?
        """, (id_usuario,))

    elif perfil == "BARBEIRO":

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
            ON ag.id_cliente = cli.id

        INNER JOIN profissionais prof
            ON ag.id_barbeiro = prof.id

        INNER JOIN servicos serv
            ON ag.id_servico = serv.id

        WHERE prof.id_usuario = ?
        """, (id_usuario,))

    else:

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
            ON ag.id_cliente = cli.id

        INNER JOIN profissionais prof
            ON ag.id_barbeiro = prof.id

        INNER JOIN servicos serv
            ON ag.id_servico = serv.id
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

def mostrar_horarios_disponiveis(id_barbeiro, data):

    print("\n=== HORÁRIOS DISPONÍVEIS ===")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT
        ag.hora,
        serv.duracao

    FROM agendamentos ag

    INNER JOIN servicos serv
        ON ag.id_servico = serv.id

    WHERE ag.id_barbeiro = ?
    AND ag.data = ?
    """, (
        id_barbeiro,
        data
    ))

    horarios_ocupados = []

    horarios_livres = []

    for hora_agendada, duracao in cursor.fetchall():

        inicio = datetime.strptime(
            f"{data} {hora_agendada}",
            "%d/%m/%Y %H:%M"
        )

        fim = inicio + timedelta(
            minutes=duracao
        )

        atual = inicio

        while atual < fim:

            horarios_ocupados.append(
                atual.strftime("%H:%M")
            )

            atual += timedelta(minutes=30)

    for hora in range(8, 20):

        horario_cheio = f"{hora:02d}:00"

        if horario_cheio not in horarios_ocupados:

            print(horario_cheio)

            horarios_livres.append(
                horario_cheio
            )

        horario_meia = f"{hora:02d}:30"

        if horario_meia not in horarios_ocupados:

            print(horario_meia)

            horarios_livres.append(
                horario_meia
            )
    conn.close()
    return horarios_livres

def gerenciar_status_agendamentos():

    conn = conectar()
    cursor = conn.cursor()

    print("\n=== GERENCIAR STATUS DE AGENDAMENTOS ===")

    cursor.execute("""
        SELECT id, data, hora, status
        FROM agendamentos
        ORDER BY data, hora
    """)

    agendamentos = cursor.fetchall()

    if not agendamentos:
        print("Nenhum agendamento encontrado.")
        conn.close()
        return

    for agendamento in agendamentos:
        print(
            f"ID: {agendamento[0]} | "
            f"{agendamento[1]} | "
            f"{agendamento[2]} | "
            f"{agendamento[3]}"
        )

    print("\n=== ALTERAR STATUS ===")
    print("1 - AGENDADO")
    print("2 - CONCLUIDO")
    print("3 - FALTOU")
    print("0 - Cancelar")

    opcao = input("\nEscolha o novo status: ")

    status_map = {
        "1": "AGENDADO",
        "2": "CONCLUIDO",
        "3": "FALTOU"
    }

    if opcao == "0":
        print("Operação cancelada.")
        conn.close()
        return

    if opcao not in status_map:
        print("Opção inválida.")
        conn.close()
        return

    novo_status = status_map[opcao]

    id_agendamento = input("\nDigite o ID do agendamento: ")

    cursor.execute("""
        UPDATE agendamentos
        SET status = ?
        WHERE id = ?
    """, (
        novo_status,
        id_agendamento
    ))

    conn.commit()

    if cursor.rowcount > 0:
        print(f"Status alterado para {novo_status}!")
    else:
        print("Agendamento não encontrado!")

    conn.close()