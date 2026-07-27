import sqlite3


db = sqlite3.connect(
    "banlist.db",
    check_same_thread=False
)


cursor = db.cursor()



# ==========================
# UTENTI BANNATI
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS blacklist (

    user_id INTEGER PRIMARY KEY,
    username TEXT,
    nome TEXT,
    motivo TEXT,
    data TEXT

)
""")



# ==========================
# STORICO INGRESSI
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS utenti (

    user_id INTEGER PRIMARY KEY,
    username TEXT,
    nome TEXT,
    ingressi INTEGER DEFAULT 1

)
""")



# ==========================
# STORICO USERNAME
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS username_storici (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    data TEXT

)
""")



# ==========================
# WHITELIST
# ==========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS whitelist (

    user_id INTEGER PRIMARY KEY,
    nome TEXT,
    data TEXT

)
""")



db.commit()





# ==========================
# SALVA UTENTE
# ==========================

def salva_utente(user):

    cursor.execute("""
    INSERT INTO utenti
    (user_id, username, nome)

    VALUES (?, ?, ?)

    ON CONFLICT(user_id)

    DO UPDATE SET

    ingressi = ingressi + 1,
    username = excluded.username,
    nome = excluded.nome

    """,
    (
        user.id,
        user.username,
        user.first_name
    ))


    db.commit()





# ==========================
# SALVA STORICO USERNAME
# ==========================

def salva_username(user):

    if not user.username:
        return


    cursor.execute(
        """
        SELECT *
        FROM username_storici
        WHERE user_id=?
        AND LOWER(username)=LOWER(?)
        """,
        (
            user.id,
            user.username
        )
    )


    esiste = cursor.fetchone()


    if not esiste:

        cursor.execute(
            """
            INSERT INTO username_storici
            (user_id, username, data)

            VALUES (?, ?, datetime('now'))
            """,
            (
                user.id,
                user.username
            )
        )


        db.commit()





# ==========================
# CONTROLLO BAN ID
# ==========================

def utente_bannato(user_id):

    cursor.execute(
        """
        SELECT *
        FROM blacklist
        WHERE user_id=?
        """,
        (user_id,)
    )


    return cursor.fetchone()





# ==========================
# AGGIUNGI BAN
# ==========================

def aggiungi_ban(user, motivo):

    cursor.execute(
    """
    INSERT OR REPLACE INTO blacklist

    VALUES (?,?,?,?,datetime('now'))

    """,
    (
        user.id,
        user.username,
        user.first_name,
        motivo
    ))


    db.commit()


def rimuovi_ban(user_id):

    cursor.execute(
        """
        DELETE FROM blacklist
        WHERE user_id = ?
        """,
        (user_id,)
    )

    db.commit()

    print("Eliminato:", user_id)


# ==========================
# LISTA BANNATI
# ==========================

def lista_bannati():

    cursor.execute(
        """
        SELECT

            user_id,
            username,
            nome,
            motivo,
            data

        FROM blacklist
        """
    )


    return cursor.fetchall()





# ==========================
# LISTA USERNAME STORICI
# ==========================

def lista_username_storici(user_id):

    cursor.execute(
        """
        SELECT username

        FROM username_storici

        WHERE user_id=?

        """,
        (user_id,)
    )


    return cursor.fetchall()





# ==========================
# CERCA USERNAME STORICO
# ==========================

def cerca_username_storico(username):

    if not username:
        return []


    cursor.execute(
        """
        SELECT 
            user_id,
            username

        FROM username_storici

        WHERE LOWER(username)=LOWER(?)

        """,
        (username,)
    )


    return cursor.fetchall()





# ==========================
# WHITELIST
# ==========================

def aggiungi_whitelist(user):

    cursor.execute(
        """
        INSERT OR REPLACE INTO whitelist

        VALUES (?, ?, datetime('now'))

        """,
        (
            user.id,
            user.first_name
        )
    )


    db.commit()





def utente_whitelist(user_id):

    cursor.execute(
        """
        SELECT *

        FROM whitelist

        WHERE user_id=?

        """,
        (user_id,)
    )


    return cursor.fetchone()

    print("TEST DATABASE AVVIATO")

    rimuovi_ban(123456789)

    print("BAN TEST ELIMINATO")