# logger_setup.py
import logging


class LoggerSetup:
    def __init__(self, log_file="pdf_summariser.log"):
        self.log_file = log_file
        self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
            filemode="a",
        )
        # Also log to console
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        console.setFormatter(formatter)
        logging.getLogger().addHandler(console)
