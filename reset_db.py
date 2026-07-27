import sqlite3

conn = sqlite3.connect("banlist.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM blacklist")
cursor.execute("DELETE FROM utenti")

conn.commit()
conn.close()

print("Database ripulito correttamente")