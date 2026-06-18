from banco import conectar

conn = conectar()
cursor = conn.cursor()

cursor.execute("DELETE FROM agendamentos")

conn.commit()

print("Agenda limpa!")

conn.close()