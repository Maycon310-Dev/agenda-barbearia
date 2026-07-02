from banco import conectar

conn = conectar()
cursor = conn.cursor()

cursor.execute("""
SELECT id, status
FROM agendamentos
""")

print(cursor.fetchall())

conn.close()