# pdf_generator.py
import os
import logging
from fpdf import FPDF
import unicodedata
import regex


class PDFGenerator:
    def __init__(self, font_dir):
        self.font_dir = font_dir
        self.pdf = self.setup_pdf()

    def setup_pdf(self):
        class PDF(FPDF):
            def header(self):
                # Ensure fonts are registered before setting them
                self.set_font("DejaVuSans", "B", 14)
                self.cell(
                    0,
                    10,
                    "Summarised PDF by Max_Agent",
                    border=False,
                    ln=True,
                    align="C",
                )
                self.ln(10)

            def footer(self):
                self.set_y(-15)
                self.set_font("DejaVuSans", "I", 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

        pdf = PDF()

        # Register fonts
        try:
            logging.info("Registering DejaVuSans fonts...")
            pdf.add_font(
                "DejaVuSans",
                "",
                os.path.join(self.font_dir, "DejaVuSans.ttf"),
                uni=True,
            )
            pdf.add_font(
                "DejaVuSans",
                "B",
                os.path.join(self.font_dir, "DejaVuSans-Bold.ttf"),
                uni=True,
            )
            pdf.add_font(
                "DejaVuSans",
                "I",
                os.path.join(self.font_dir, "DejaVuSans-Oblique.ttf"),
                uni=True,
            )
            pdf.add_font(
                "DejaVuSans",
                "BI",
                os.path.join(self.font_dir, "DejaVuSans-BoldOblique.ttf"),
                uni=True,
            )
            logging.info("DejaVuSans fonts registered successfully.")
        except Exception as e:
            logging.error(f"Failed to add fonts: {e}")
            raise

        # Add a page
        pdf.add_page()

        # Set the default font
        pdf.set_font("DejaVuSans", size=12)

        return pdf

    def replace_pua_characters(self, text, replacement="#"):
        """
        Replaces all Private Use Area (PUA) characters in the text with a
        specified replacement character.

        Parameters:
        - text (str): The input text containing potential PUA characters.
        - replacement (str): The character to replace PUA characters with.
          Default is '#'.

        Returns:
        - str: The sanitized text with PUA characters replaced.
        """
        # Define PUA range in Unicode (BMP PUA: U+E000 to U+F8FF)
        pua_pattern = regex.compile(r"[\uE000-\uF8FF]")

        # Replace each PUA character with the replacement character
        sanitized_text = pua_pattern.sub(replacement, text)

        logging.debug(f"Replaced PUA characters with '{replacement}'.")
        return sanitized_text

        # Trying to avoid unicode characters causing list index out of range errors

    def remove_non_ascii(self, text):
        return "".join(ch for ch in text if ord(ch) < 128)

    def add_text(self, text):
        # Normalize text
        text = unicodedata.normalize("NFKD", text)
        text = "".join(c for c in text if c.isprintable())

        # Replace multiple newlines with single newline
        text = regex.sub(r"\n+", "\n", text).strip()

        # Replace PUA characters
        text = self.replace_pua_characters(text)

        # Remove all non-ASCII characters as a last resort
        text = self.remove_non_ascii(text)

        logging.debug(f"Final sanitized text sample: {text[:100]}")

        lines = text.split("\n")
        logging.debug(f"Number of lines to add: {len(lines)}")

        for idx, line in enumerate(lines, 1):
            if line.strip():
                logging.debug(f"Adding line {idx}: '{line}'")
                try:
                    self.pdf.multi_cell(0, 10, line)
                except IndexError as e:
                    logging.error(f"IndexError while adding line {idx}: {e}")
                    print(f"Error: {e} while adding line {idx}.")
            else:
                logging.debug(f"Skipping empty line {idx}.")

    def save_pdf(self, output_pdf_path):
        try:
            self.pdf.output(output_pdf_path)
            logging.info(f"PDF saved to '{output_pdf_path}'.")
        except Exception as e:
            logging.error(f"Failed to save PDF '{output_pdf_path}': {e}")
