import logging

from confronto import cerca_miglior_match

from database import (
    aggiungi_ban,
    utente_bannato,
    salva_utente,
    salva_username,
    cerca_username_storico,
    lista_bannati,
    utente_whitelist,
    aggiungi_whitelist,
    rimuovi_ban
)

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ChatMemberHandler,
    ContextTypes
)


TOKEN = "8520450461:AAE8SKExkzqA8yKx8hhfdm-Q_061JNhX2jw"


logging.basicConfig(
    format="%(asctime)s - %(message)s",
    level=logging.INFO
)


# ==========================
# CONTROLLO RISCHIO
# ==========================

def calcola_rischio(user):

    rischio = 0

    nome = user.first_name or ""
    username = user.username or ""

    if not username:
        rischio += 10

    if len(nome) <= 2:
        rischio += 20

    for _, username_bannato, _, _, _ in lista_bannati():

        if username_bannato:

            if username.lower() == username_bannato.lower():
                rischio += 50

    return rischio


# ==========================
# COMANDO /ban
# ==========================

async def ban_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Rispondi al messaggio dell'utente da bannare."
        )

        return

    user = update.message.reply_to_message.from_user

    motivo = " ".join(context.args)

    if not motivo:
        motivo = "Nessun motivo specificato"

    aggiungi_ban(
        user,
        motivo
    )

    await update.message.reply_text(
        f"🚫 Utente bannato definitivamente\n\n"
        f"Nome: {user.first_name}\n"
        f"ID: {user.id}\n"
        f"Motivo: {motivo}"
    )

    await update.message.chat.ban_member(
        user.id
    )


# ==========================
# CONTROLLO INGRESSI
# ==========================

async def controllo_ingresso(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    nuovo = update.chat_member.new_chat_member

    if nuovo.status == "member":

        user = nuovo.user

        salva_utente(user)

        salva_username(user)


        if utente_whitelist(user.id):

            logging.info(
                f"Utente whitelist: {user.id}"
            )

            return

        rischio = calcola_rischio(user)

        simile = cerca_miglior_match(
            {
                "nome": user.first_name or "",
                "username": user.username or ""
            },
            lista_bannati()
        )

        storico_username = cerca_username_storico(
            user.username
        )

        logging.info(
            f"Nuovo ingresso: {user.id} rischio={rischio}"
        )

        # Se è già bannato per ID
        if utente_bannato(user.id):

            await update.chat_member.chat.ban_member(
                user.id
            )

            await update.chat_member.chat.send_message(
                f"🚨 Utente bloccato automaticamente\n\n"
                f"Nome: {user.first_name}\n"
                f"ID: {user.id}\n"
                f"Presente nella blacklist."
            )

        elif storico_username:

            await update.chat_member.chat.send_message(
                f"⚠️ USERNAME GIÀ PRESENTE NELLO STORICO\n\n"
                f"Utente:\n"
                f"Nome: {user.first_name}\n"
                f"Username: @{user.username or '-'}\n\n"
                f"Questo username è già stato utilizzato in passato."
            )    

        # Possibile rientro
        elif simile and simile["rischio"] >= 80:

            await update.chat_member.chat.send_message(
                f"⚠️ POSSIBILE RIENTRO\n\n"
                f"👤 Nuovo utente\n"
                f"Nome: {user.first_name}\n"
                f"Username: @{user.username or '-'}\n"
                f"ID: {user.id}\n\n"

                f"──────────────\n\n"

                f"Somiglia a:\n"
                f"Nome: {simile['nome']}\n"
                f"Username: @{simile['username'] or '-'}\n\n"

                f"📊 Nome: {simile['nome_score']}%\n"
                f"📊 Username: {simile['username_score']}%\n"
                f"🎯 Rischio totale: {simile['rischio']}%\n\n"

                f"📝 Motivo ban: {simile['motivo']}\n"
                f"📅 Data ban: {simile['data']}"
            )

        # Utente sospetto
        elif rischio >= 40:

            await update.chat_member.chat.send_message(
                f"⚠️ UTENTE SOSPETTO\n\n"
                f"Nome: {user.first_name}\n"
                f"Username: @{user.username or '-'}\n"
                f"Punteggio rischio: {rischio}"
            )

# ==========================
# TEST BAN
# ==========================

from types import SimpleNamespace


async def test_ban(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    utente_test = SimpleNamespace(
        id=123456789,
        first_name="Mario Test",
        username="mario_test"
    )

    aggiungi_ban(
        utente_test,
        "Test automatico"
    )

    await update.message.reply_text(
        "✅ Test ban completato.\n"
        "Utente finto aggiunto alla lista ban."
    )

# ==========================
# TEST SIMILITUDINE
# ==========================

async def test_simile(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    utente_test = {
        "nome": "Mario Testo",
        "username": "mario_test2"
    }

    risultato = cerca_miglior_match(
        utente_test,
        lista_bannati()
    )

    if risultato:

        await update.message.reply_text(
            f"⚠️ POSSIBILE RIENTRO TROVATO\n\n"
            f"Somiglia a:\n"
            f"Nome: {risultato['nome']}\n"
            f"Username: @{risultato['username']}\n\n"
            f"Rischio: {risultato['rischio']}%"
        )

    else:

        await update.message.reply_text(
            "✅ Nessuna similitudine trovata."
        )

# ==========================
# TEST CONTROLLO BAN
# ==========================

async def test_check(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    id_test = 123456789

    risultato = utente_bannato(id_test)

    presente = risultato is not None

    await update.message.reply_text(
        f"🔍 Controllo ID {id_test}\n\n"
        f"Bannato: {presente}\n\n"
        f"Dati trovati:\n{risultato}"
    )

# ==========================
# TEST RIENTRO
# ==========================

async def test_rientro(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    id_test = 123456789

    trovato = utente_bannato(id_test)

    if trovato:

        await update.message.reply_text(
            "🚨 TEST RIENTERRO\n\n"
            f"ID {id_test} trovato in blacklist.\n"
            "Il BAN automatico funzionerebbe."
        )

    else:

        await update.message.reply_text(
            "❌ Utente non trovato in blacklist."
        )

# ==========================
# LISTA BAN
# ==========================

async def lista_ban(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    utenti = lista_bannati()

    if not utenti:

        await update.message.reply_text(
            "Lista ban vuota."
        )

        return

    testo = "🚫 Lista bannati:\n\n"

    for u in utenti:

        testo += (
            f"ID: {u[0]}\n"
            f"Username: @{u[1] or '-'}\n"
            f"Nome: {u[2]}\n"
            f"Motivo: {u[3]}\n"
            f"Data: {u[4]}\n\n"
        )

    await update.message.reply_text(testo)

async def pulisci_test(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    rimuovi_ban(123456789)

    await update.message.reply_text(
        "✅ Record test eliminato."
    )

# ==========================
# TEST RISCHIO
# ==========================

async def test_rischio(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user = update.message.from_user

    rischio = calcola_rischio(user)

    await update.message.reply_text(
        f"🔍 Test controllo intelligente\n\n"
        f"Nome: {user.first_name}\n"
        f"Username: @{user.username or '-'}\n"
        f"Rischio calcolato: {rischio}"
    )

async def pulisci_test(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    rimuovi_ban(123456789)

    await update.message.reply_text(
        "✅ Utente test rimosso dalla blacklist."
    )

# ==========================
# VERIFICA MANUALE
# ==========================

async def verifica(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Rispondi al messaggio dell'utente da verificare."
        )

        return


    user = update.message.reply_to_message.from_user


    risultato = cerca_miglior_match(
        {
            "nome": user.first_name or "",
            "username": user.username or ""
        },
        lista_bannati()
    )


    if not risultato:

        await update.message.reply_text(
            "Nessun risultato trovato."
        )

        return


    await update.message.reply_text(
        f"🔍 ANALISI UTENTE\n\n"
        f"👤 Utente controllato\n"
        f"Nome: {user.first_name}\n"
        f"Username: @{user.username or '-'}\n\n"

        f"──────────────\n\n"

        f"🎯 Match migliore\n"
        f"Nome: {risultato['nome']}\n"
        f"Username: @{risultato['username'] or '-'}\n\n"

        f"📊 Somiglianza nome: {risultato['nome_score']}%\n"
        f"📊 Somiglianza username: {risultato['username_score']}%\n"
        f"⚠️ Rischio: {risultato['rischio']}%\n\n"

        f"📝 Motivo ban: {risultato['motivo']}\n"
        f"📅 Data ban: {risultato['data']}"
    )

# ==========================
# COMANDO /whitelist
# ==========================

async def whitelist_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message.reply_to_message:

        await update.message.reply_text(
            "Rispondi al messaggio dell'utente da mettere in whitelist."
        )

        return


    user = update.message.reply_to_message.from_user


    aggiungi_whitelist(user)


    await update.message.reply_text(
        f"✅ Utente aggiunto alla whitelist\n\n"
        f"Nome: {user.first_name}\n"
        f"ID: {user.id}"
    )

# ==========================
# AVVIO BOT
# ==========================

def main():

    app = (
        Application.builder()
        .token(TOKEN)
        .build()
    )

    app.add_error_handler(
        errore_handler
    )

    app.add_handler(
        CommandHandler(
            "ban",
            ban_command
        )
    )

   # app.add_handler(
   #     CommandHandler(
   #         "testban",
   #         test_ban
   #     )
   # )

   # app.add_handler(
   #     CommandHandler(
   #         "testsimile",
   #         test_simile
   #     )
   # )

   # app.add_handler(
   #     CommandHandler(
   #         "testrientro",
   #         test_rientro
   #     )
   # )

   # app.add_handler(
   #     CommandHandler(
   #         "testcheck",
   #         test_check
   #     )
   # )

    app.add_handler(
        CommandHandler(
            "pulisci",
            pulisci_test
        )
    )

    app.add_handler(
        CommandHandler(
            "lista_ban",
            lista_ban
        )
    )

    app.add_handler(
        CommandHandler(
            "test",
            test_rischio
        )
    )

    app.add_handler(
        CommandHandler(
            "whitelist",
            whitelist_command
        )
    )

    app.add_handler(
        CommandHandler(
            "verifica",
            verifica
        )
    )


    app.add_handler(
        ChatMemberHandler(
            controllo_ingresso,
            ChatMemberHandler.CHAT_MEMBER
        )
    )

    print("Bot attivo...")

    app.run_polling()


async def errore_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logging.error(
        "Errore:",
        exc_info=context.error
    )


if __name__ == "__main__":
    main()