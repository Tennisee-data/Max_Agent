# file_tracker.py
import os
import logging


class FileTracker:
    def __init__(self, log_file):
        self.log_file = log_file
        self.processed_files = self.load_processed_files()

    def load_processed_files(self):
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as f:
                return set(line.strip() for line in f if line.strip())
        return set()

    def is_processed(self, filename):
        return filename in self.processed_files

    def mark_as_processed(self, filename):
        self.processed_files.add(filename)
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{filename}\n")
        logging.info(f"Marked '{filename}' as processed.")
