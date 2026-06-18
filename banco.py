import sqlite3

NOME_BANCO = 'barbearia.db'

def conectar():
    return sqlite3.connect (NOME_BANCO)

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    # clientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT,
        id_usuario INTEGER,
                   
        FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
        
    )
""")
        # PROFISSIONAIS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS profissionais (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT,
            id_usuario INTEGER,
            
            FOREIGN KEY(id_usuario) REFERENCES usuarios(id_usuario)
        )
    """)

    # SERVIÇOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            valor REAL NOT NULL,
            duracao INTEGER NOT NULL
        )
    """)

    # AGENDAMENTOS
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS agendamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cliente INTEGER NOT NULL,
            id_barbeiro INTEGER NOT NULL,
            id_servico INTEGER NOT NULL,
            data TEXT NOT NULL,
            hora TEXT NOT NULL,
            status TEXT DEFAULT 'AGENDADO',

            FOREIGN KEY(id_cliente) REFERENCES clientes(id),
            FOREIGN KEY(id_barbeiro) REFERENCES profissionais(id),
            FOREIGN KEY(id_servico) REFERENCES servicos(id)
        )
    """)
   
     #Usuario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id_usario INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            perfil TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


    print("Tabelas criadas com sucesso!")

