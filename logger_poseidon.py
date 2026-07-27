import logging
import os


if not os.path.exists("logs"):
    os.makedirs("logs")


logging.basicConfig(
    filename="logs/poseidon.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)


def scrivi_log(messaggio):

    logging.info(messaggio)