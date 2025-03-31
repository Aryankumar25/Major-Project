import logging
from config import LOG_FILE

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(asctime)s - %(message)s")

def log_event(message):
    print(message)
    logging.info(message)
