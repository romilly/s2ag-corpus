import logging
import os
from datetime import date

from s2ag_corpus.helpers.monitor import Monitor

os.makedirs('../logs', exist_ok=True)
filename = f'../logs/{date.today().isoformat()}.log'
log_format = '%(asctime)s - %(levelname)-7s - %(message)s'
logging.basicConfig(filename=filename, level=logging.INFO, format=log_format)


class LoggingMonitor(Monitor):
    def info(self, message: str) -> None:
        logging.info(message)

    def warn(self, message: str):
        logging.warning(message)

    def debug(self, message):
        logging.debug(message)

    def error(self, message):
        logging.error(message)
        print(message)