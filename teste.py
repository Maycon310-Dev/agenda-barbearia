from banco import conectar

conn = conectar()
cursor = conn.cursor()

print("\n=== CLIENTES ===")
cursor.execute("SELECT * FROM clientes")
for linha in cursor.fetchall():
    print(linha)

print("\n=== PROFISSIONAIS ===")
cursor.execute("SELECT * FROM profissionais")
for linha in cursor.fetchall():
    print(linha)

conn.close()