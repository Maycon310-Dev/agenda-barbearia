from banco import conectar

def dashboard():

    conn = conectar()
    cursor = conn.cursor()

    # Clientes

    cursor.execute("""
        SELECT COUNT(*)
        FROM clientes
    """)

    total_clientes = cursor.fetchone()[0]

    # Barbeiros

    cursor.execute("""
        SELECT COUNT(*)
        FROM profissionais
    """)

    total_barbeiros = cursor.fetchone()[0]

    # Serviços

    cursor.execute("""
        SELECT COUNT(*)
        FROM servicos
    """)

    total_servicos = cursor.fetchone()[0]

    # Agendamentos

    from datetime import datetime

    hoje = datetime.now().strftime("%d/%m/%Y")

    # Total de agendamentos

    cursor.execute("""
        SELECT COUNT(*)
        FROM agendamentos
    """)

    total_agendamentos = cursor.fetchone()[0]

    # Agendamentos de hoje

    cursor.execute("""
        SELECT COUNT(*)
        FROM agendamentos
        WHERE data = ?
    """, (hoje,))

    agendamentos_hoje = cursor.fetchone()[0]

    print("\n" + "=" * 40)
    print("           DASHBOARD")
    print("=" * 40)

    print(
        f"Clientes cadastrados: {total_clientes}"
    )

    print(
        f"Barbeiros cadastrados: {total_barbeiros}"
    )

    print(
        f"Serviços cadastrados: {total_servicos}"
    )

    print(
        f"Agendamentos: {total_agendamentos}"
    )

    print(
    f"Agendamentos hoje: {agendamentos_hoje}"
)

    print("=" * 40)

    conn.close()

def relatorio_financeiro():

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.nome,
            COUNT(*),
            SUM(s.valor)

        FROM agendamentos a

        INNER JOIN servicos s
            ON a.id_servico = s.id

        GROUP BY s.nome

        ORDER BY s.nome
    """)

    resultados = cursor.fetchall()

    print("\n" + "=" * 40)
    print("      RELATÓRIO FINANCEIRO")
    print("=" * 40)

    total_geral = 0

    for nome, quantidade, valor_total in resultados:

        print(
            f"{nome:<20}"
            f"{quantidade}x"
            f"    R${valor_total:.2f}"
        )

        total_geral += valor_total

    print("\n" + "=" * 40)

    print(
        f"TOTAL PREVISTO: R${total_geral:.2f}"
    )

    print("=" * 40)

    conn.close()

def relatorio_por_periodo():

    data_inicial = input(
        "Digite a data inicial (dd/mm/aaaa): "
    )

    data_final = input(
        "Digite a data final (dd/mm/aaaa): "
    )

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.nome,
            COUNT(*),
            SUM(s.valor)

        FROM agendamentos a

        INNER JOIN servicos s
            ON a.id_servico = s.id

        WHERE a.data >= ?
        AND a.data <= ?

        GROUP BY s.nome

        ORDER BY s.nome
    """, (
        data_inicial,
        data_final
    ))

    resultados = cursor.fetchall()

    print("\n" + "=" * 40)
    print("     RELATÓRIO POR PERÍODO")
    print("=" * 40)

    total_geral = 0

    for nome, quantidade, valor_total in resultados:

        print(
            f"{nome:<20}"
            f"{quantidade}x"
            f"    R${valor_total:.2f}"
        )

        total_geral += valor_total

    print("\n" + "=" * 40)

    print(
        f"TOTAL: R${total_geral:.2f}"
    )

    print("=" * 40)

    conn.close()