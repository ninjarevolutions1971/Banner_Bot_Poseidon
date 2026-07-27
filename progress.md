# Banner Bot Poseidon - Progress

Data ultimo aggiornamento:
27/07/2026

## Stato progetto

Bot Telegram anti-rientro funzionante.

Obiettivo:
Creare un sistema intelligente che riconosce utenti bannati che rientrano con nuovi account.

---

# Completato ✅

## Database

File:
- database.py
- banlist.db

Struttura database attuale:

## blacklist

Campi:

- user_id
- username
- nome
- motivo
- data


Funzioni presenti:

- aggiungi_ban()
- utente_bannato()
- lista_bannati()


## utenti

Storico ingressi:

- user_id
- username
- nome
- ingressi


Funzione presente:

- salva_utente()

---

# Ban system ✅

Comando:

/ban

Funzionamento:

L'amministratore deve rispondere al messaggio dell'utente:

Esempio:

/ban spam

Il bot salva:

- ID
- Username
- Nome
- Motivo
- Data


Poi esegue:

ban permanente Telegram

---

# Lista ban ✅

Comando:

/lista_ban

Mostra gli utenti presenti nello storico.

---

# Test rischio ✅

Comando:

/test

Funzionante.

Controlla:

- presenza username
- lunghezza nome
- confronto username bannati


---

# Anti ingresso base ✅

Quando entra un utente:

1. salva ingresso
2. controlla se ID già bannato
3. blocca automaticamente se presente nella blacklist
4. calcola rischio


---

# Ultima modifica fatta

Aggiunta funzione:

lista_bannati()

in database.py


Aggiunto import:

from database import (
    aggiungi_ban,
    utente_bannato,
    salva_utente,
    lista_bannati
)


---

# Prossimo lavoro 🔜

Implementare controllo intelligente rientro.

Obiettivo:

Se un utente bannato torna con altro account:

Esempio:

BAN STORICO:

Nome:
Mario Rossi

Username:
@mario88


NUOVO ACCOUNT:

Nome:
Mario_Rossi

Username:
@mario90


Il bot deve generare:

⚠️ POSSIBILE RIENTRO

Nuovo utente:
Mario_Rossi
@mario90

Somiglia a:
Mario Rossi
@mario88

Somiglianza: XX%

---

# Miglioramenti futuri

Possibili aggiunte:

- confronto nome + cognome
- confronto username modificati
- storico cambi username
- punteggio rischio avanzato
- pannello amministratore
- comando /verifica
- whitelist utenti fidati
- log completo eventi


---

# File principali

anti_rientro_bot.py
    ↓
Gestione bot Telegram

database.py
    ↓
Gestione SQLite

banlist.db
    ↓
Database storico


---

# Nota importante

Prima di continuare:
fare backup:

banlist.db

e mantenere una copia funzionante del bot.