import sys
import logging
from logging import StreamHandler
from logging.handlers import RotatingFileHandler


def setupLogWriter():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(
        'output.log', maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler = StreamHandler()
    stream_handler.setLevel(logging.INFO)

    logging.getLogger().addHandler(file_handler)
    logging.getLogger().addHandler(stream_handler)
    sys.stdout = LogWriter(logging.getLogger(), level=logging.INFO)


class LogWriter:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level

    def write(self, message):
        if message.strip():  # Avoid logging empty messages
            self.logger.log(self.level, message.strip())

    def flush(self):
        pass  # No need to flush
