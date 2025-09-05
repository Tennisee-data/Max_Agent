# pdf_summariser_app.py
import re
import os
import sys
import logging
import torch
import unicodedata
from .config import Config
from .logger_setup import LoggerSetup
from .file_tracker import FileTracker
from .pdf_processor import PDFProcessor
from .summariser import Summariser
from .pdf_generator import PDFGenerator


class PDFSummariserApp:
    def __init__(self, config_file="config.yaml"):
        self.config = Config(config_file)
        LoggerSetup(self.config.log_file)
        logging.info("Logger initialised.")
        self.config.create_directories()
        logging.info("Directories ensured.")
        self.file_tracker = FileTracker(self.config.processed_files_log)
        logging.info("File tracker initialised.")
        self.pdf_processor = PDFProcessor(
            font_dir=self.config.font_directory,
            cleaned_text_dir=self.config.cleaned_text_directory,
        )
        self.summariser = Summariser(
            model_id=self.config.summarization_model_id,
            device=0 if torch.cuda.is_available() else -1,
        )
        logging.info("Summariser initialised.")
        self.pdf_generator = PDFGenerator(font_dir=self.config.font_directory)

    def process_pdf(self, pdf_filename):
        pdf_path = os.path.join(self.config.input_directory, pdf_filename)
        name, ext = os.path.splitext(pdf_filename)
        output_pdf_filename = f"{name}_cond{ext}"
        output_pdf_path = os.path.join(
            self.config.output_directory, output_pdf_filename
        )
        cleaned_txt_filename = f"{name}_cleaned.txt"
        cleaned_txt_path = os.path.join(
            self.config.cleaned_text_directory, cleaned_txt_filename
        )

        logging.info(f"Processing '{pdf_filename}'...")

        # Process PDF
        cleaned_text, code_blocks, equations = self.pdf_processor.process_pdf(
            pdf_path=pdf_path, save_cleaned=True, cleaned_txt_path=cleaned_txt_path
        )

        # Summarise
        chunks = self.bin_text(cleaned_text)
        summary = self.summariser.summarise(
            chunks=chunks,
            first_min_ratio=self.config.first_min_ratio,
            first_max_ratio=self.config.first_max_ratio,
            second_min_ratio=self.config.second_min_ratio,
            second_max_ratio=self.config.second_max_ratio,
        )

        # Reintegrate code and equations
        final_summary = self.reintegrate_code_equations(summary, code_blocks, equations)

        # Generate PDF
        self.pdf_generator.add_text(final_summary)
        self.pdf_generator.save_pdf(output_pdf_path)

        # Mark as processed
        self.file_tracker.mark_as_processed(pdf_filename)

        logging.info(
            f"'{pdf_filename}' has been summarised by Max_Agent and saved as "
            f"'{output_pdf_filename}'."
        )

    def bin_text(self, text):
        # Split text into sentences
        sentences = re.split(r"(?<=[.!?]) +", text)
        chunks = []
        current_chunk = ""
        current_length = 0

        for sentence in sentences:
            sentence_length = self.summariser.count_tokens(sentence)
            if current_length + sentence_length <= self.config.max_tokens:
                current_chunk += " " + sentence
                current_length += sentence_length
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = sentence
                current_length = sentence_length

        if current_chunk:
            chunks.append(current_chunk.strip())

        logging.info(f"Total chunks created: {len(chunks)}")
        return chunks

    def reintegrate_code_equations(self, summary, code_blocks, equations):
        # Normalise text to remove problematic Unicode characters
        summary = unicodedata.normalize("NFKD", summary)
        summary = "".join(c for c in summary if c.isprintable())

        final_text = summary
        if code_blocks:
            final_text += "\n\n# Code Blocks\n" + "\n".join(code_blocks)
        if equations:
            final_text += "\n\n# Equations\n" + "\n".join(equations)
        return final_text

    def run(self):
        # List all PDF files in the input directory
        all_pdfs = [
            f
            for f in os.listdir(self.config.input_directory)
            if f.lower().endswith(".pdf")
        ]

        # Filter out PDFs that have already been processed
        new_pdfs = [f for f in all_pdfs if not self.file_tracker.is_processed(f)]

        if not new_pdfs:
            logging.info("As far as I can see, no new PDFs to process.")
            sys.exit(0)

        logging.info(f"Good, found {len(new_pdfs)} new PDF(s) to process.")

        for pdf_filename in new_pdfs:
            self.process_pdf(pdf_filename)
