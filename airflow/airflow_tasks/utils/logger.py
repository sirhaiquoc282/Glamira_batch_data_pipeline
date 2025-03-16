import os
import logging
from airflow_tasks.configs.settings import LOG_LEVEL, LOG_FILE


class Logger:
    def __init__(self, name="data_pipeline", log_file=LOG_FILE, log_level=LOG_LEVEL):
        self.log_file = log_file
        self.log_level = log_level if isinstance(log_level, int) else logging.INFO
        self.logger = logging.getLogger(name)
        self._init_logger()

    def _init_logger(self):

        log_dir = os.path.dirname(self.log_file)
        os.makedirs(log_dir, exist_ok=True)

        log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter = logging.Formatter(fmt=log_format, datefmt=date_format)

        self.logger.setLevel(self.log_level)

        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message):
        self.logger.info(message)

    def error(self, message):
        self.logger.error(message)

    def warning(self, message):
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)
