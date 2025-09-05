# config.py
import os
import yaml

# Type hints removed as they weren't used


class Config:
    def __init__(self, config_file: str = "config.yaml") -> None:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)

        self.input_directory = config.get("input_directory", "./pdfs/")
        self.output_directory = config.get("output_directory", "./summarised_pdfs/")
        self.cleaned_text_directory = config.get(
            "cleaned_text_directory", "./cleaned_texts/"
        )
        self.font_directory = config.get("font_directory", "./dejavu-sans/")
        self.processed_files_log = config.get(
            "processed_files_log", "./processed_pdfs.txt"
        )
        self.log_file = config.get("log_file", "pdf_summariser.log")
        self.summarization_model_id = config.get(
            "summarization_model_id", "facebook/bart-large-cnn"
        )
        self.first_min_ratio = config.get("first_min_ratio", 0.25)
        self.first_max_ratio = config.get("first_max_ratio", 0.45)
        self.second_min_ratio = config.get("second_min_ratio", 0.60)
        self.second_max_ratio = config.get("second_max_ratio", 0.80)
        self.max_tokens = config.get("max_tokens", 1024)
        self.do_sample = config.get("do_sample", False)

    def create_directories(self) -> None:
        os.makedirs(self.output_directory, exist_ok=True)
        os.makedirs(self.cleaned_text_directory, exist_ok=True)
