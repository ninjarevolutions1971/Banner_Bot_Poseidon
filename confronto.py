import re
import unicodedata
from difflib import SequenceMatcher


def normalizza(testo):
    if not testo:
        return ""

    testo = str(testo)

    # rimuove accenti
    testo = unicodedata.normalize("NFKD", testo)
    testo = "".join(c for c in testo if not unicodedata.combining(c))

    testo = testo.lower()

    # lascia solo lettere e numeri
    testo = re.sub(r"[^a-z0-9]", "", testo)

    return testo


def similarita(a, b):

    a = normalizza(a)
    b = normalizza(b)

    if not a or not b:
        return 0

    return round(
        SequenceMatcher(None, a, b).ratio() * 100
    )


def calcola_rischio(nome1, user1, nome2, user2):

    nome = similarita(nome1, nome2)
    username = similarita(user1, user2)

    rischio = round(
        nome * 0.60 +
        username * 0.40
    )

    return nome, username, rischio


def cerca_miglior_match(nuovo, bannati):

    migliore = None

    for ban in bannati:

        uid, username, nome, motivo, data = ban

        score_nome, score_user, rischio = calcola_rischio(
            nuovo["nome"],
            nuovo["username"],
            nome,
            username
        )

        if migliore is None or rischio > migliore["rischio"]:

            migliore = {

                "user_id": uid,
                "nome": nome,
                "username": username,
                "motivo": motivo,
                "data": data,

                "nome_score": score_nome,
                "username_score": score_user,
                "rischio": rischio

            }

    return migliore