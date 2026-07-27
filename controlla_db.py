import sqlite3

conn = sqlite3.connect("banlist.db")
cursor = conn.cursor()

print("Blacklist:")

cursor.execute("SELECT * FROM blacklist")

righe = cursor.fetchall()

for riga in righe:
    print(riga)

print("\nUtenti:")

cursor.execute("SELECT * FROM utenti")

righe = cursor.fetchall()

for riga in righe:
    print(riga)

conn.close()