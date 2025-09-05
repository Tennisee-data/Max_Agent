# pdf_processor.py
import pdfplumber
import re
import logging

# from fpdf import FPDF  # Unused import
from typing import List, Tuple, Optional


class PDFProcessor:
    def __init__(self, font_dir: str, cleaned_text_dir: Optional[str] = None) -> None:
        self.font_dir = font_dir
        self.cleaned_text_dir = cleaned_text_dir

    def extract_raw_text(self, pdf_path: str) -> List[str]:
        extracted_text = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text(x_tolerance=1, y_tolerance=1)
                    if page_text:
                        extracted_text.append(page_text)
                    else:
                        logging.warning(
                            f"No text found on page {page_num} of {pdf_path}."
                        )
            logging.info(f"Extracted raw text from '{pdf_path}'.")
            return extracted_text
        except Exception as e:
            logging.error(f"Failed to extract text from {pdf_path}: {e}")
            return []

    def separate_glued_words(self, text: str) -> str:
        import wordsegment

        wordsegment.load()

        # First apply regex-based separation for common patterns
        # Add space between lowercase followed by uppercase
        text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)

        # Add space between uppercase letters followed by lowercase letters
        text = re.sub(r"([A-Z])([A-Z][a-z])", r"\1 \2", text)

        # Add space between letters and numbers (both directions)
        text = re.sub(r"([a-zA-Z])(\d)", r"\1 \2", text)
        text = re.sub(r"(\d)([a-zA-Z])", r"\1 \2", text)

        # Now split into words and handle remaining glued lowercase words
        words = text.split()
        result_words = []

        for word in words:
            # Check for words that might be glued (mixed case or long lowercase)
            if re.match(r"^[a-zA-Z]+$", word) and len(word) > 6:
                # Try wordsegment first
                segmented = wordsegment.segment(word.lower())
                if len(segmented) > 1:
                    # Capitalize first letter of first word if original was capitalized
                    if word[0].isupper() and segmented:
                        segmented[0] = segmented[0].capitalize()
                    result_words.extend(segmented)
                else:
                    result_words.append(word)
            else:
                result_words.append(word)

        # Join all words and normalize spaces
        result = " ".join(result_words)
        result = re.sub(r"\s{2,}", " ", result).strip()

        return result

    def clean_text(self, text: str) -> str:
        # Remove single newlines that break sentences but preserve paragraph
        # breaks (double newlines)
        text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

        # Separate glued words
        text = self.separate_glued_words(text)

        return text

    def final_text_cleaning(self, text: str) -> str:
        replacements = [
            (r"\s+\.", "."),  # Space followed by dot
            (r"\s+,", ","),  # Space followed by comma
            (r"\s+;", ";"),  # Space followed by semicolon
            (r"\s+\)", ")"),  # Space followed by closing parenthesis
            (r"\(\s+", "("),  # Open parenthesis followed by space
            (r":\s+", ":"),  # Colon followed by space
            (r"\s{2,}", " "),  # Replace multiple spaces with a single space
        ]

        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text)

        return text

    def extract_code_and_equations(
        self, pages: List[str]
    ) -> Tuple[str, List[str], List[str]]:
        cleaned_text = ""
        code_blocks = []
        equations = []

        # Define multiple patterns for code blocks and equations
        code_patterns = [
            re.compile(r"```(.*?)```", re.DOTALL),  # Triple backticks
            re.compile(r"<code>(.*?)</code>", re.DOTALL),  # <code> tags
            re.compile(r"(^|\n)\s{4,}(.*)", re.MULTILINE),  # Indented code blocks
        ]
        equation_patterns = [re.compile(r"\$\$?(.*?)\$\$?", re.DOTALL)]

        for page_num, page in enumerate(pages, 1):
            if not page:
                continue  # Skip empty pages

            # original_page = page  # Keep a copy for debugging

            # Extract code blocks using multiple patterns
            for pattern in code_patterns:
                codes = pattern.findall(page)
                if codes:
                    logging.info(
                        f"Extracted {len(codes)} code block(s) from page {page_num}."
                    )
                # Handle indented code blocks differently
                if pattern.pattern.startswith("(^|\\n)\\s{4,}"):
                    for code in codes:
                        code_blocks.append(code[1].strip())
                else:
                    code_blocks.extend([code.strip() for code in codes])
                page = pattern.sub("", page)

            # Extract equations using multiple patterns
            for pattern in equation_patterns:
                eqs = pattern.findall(page)
                if eqs:
                    logging.info(
                        f"Extracted {len(eqs)} equation(s) from page {page_num}."
                    )
                equations.extend([eq.strip() for eq in eqs])
                page = pattern.sub("", page)

            cleaned_text += page + "\n"

        logging.info(f"Total code blocks extracted: {len(code_blocks)}")
        logging.info(f"Total equations extracted: {len(equations)}")

        return cleaned_text, code_blocks, equations

    def save_cleaned_text(self, text: str, output_txt_path: str) -> None:
        try:
            with open(output_txt_path, "w", encoding="utf-8") as f:
                f.write(text)
            logging.info(f"Cleaned text saved to '{output_txt_path}'.")
        except Exception as e:
            logging.error(f"Failed to save cleaned text: {e}")

    def process_pdf(
        self,
        pdf_path: str,
        save_cleaned: bool = True,
        cleaned_txt_path: Optional[str] = None,
    ) -> Tuple[str, List[str], List[str]]:
        pages_text = self.extract_raw_text(pdf_path)
        cleaned_text, code_blocks, equations = self.extract_code_and_equations(
            pages_text
        )
        cleaned_text = self.clean_text(cleaned_text)
        cleaned_text = self.final_text_cleaning(cleaned_text)

        if save_cleaned and cleaned_txt_path:
            self.save_cleaned_text(cleaned_text, cleaned_txt_path)

        return cleaned_text, code_blocks, equations
