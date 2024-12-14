# test_pdf_processor.py
import unittest
from pdf_processor import PDFProcessor

class TestPDFProcessor(unittest.TestCase):
    def setUp(self):
        # Initialize the PDFProcessor object
        # Ensure arguments match actual class definition
        self.processor = PDFProcessor(font_dir="./dejavu-sans/", cleaned_text_dir="./cleaned_texts/")

    def test_extract_raw_text(self):
        # Replace with a simpler input for the test
        pdf_path = "./pdfs/Share your app - Streamlit Docs.pdf"

        try:
            text = self.processor.extract_raw_text(pdf_path)
            self.assertIsInstance(text, list)
        except FileNotFoundError:
            self.skipTest(f"PDF file '{pdf_path}' not found. Skipping test.")

        def test_separate_glued_words(self):
            text = "ThisIsATest123ExampleHopeitworksforyou"
            cleaned = self.processor.separate_glued_words(text)
            expected = "This Is A Test 123 Example Hope it works for you"
            
            # Normalize both strings to lowercase for case-insensitive comparison
            self.assertEqual(cleaned.lower(), expected.lower())


if __name__ == '__main__':
    unittest.main()
