# test_pdf_processor.py
import unittest
from src.max_agent.pdf_processor import PDFProcessor

class TestPDFProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = PDFProcessor(font_dir="./dejavu-sans/", cleaned_text_dir="./cleaned_texts/")
    
    def test_extract_raw_text(self):
        pdf_path = "./pdfs/Share your app - Streamlit Docs.pdf"
        text = self.processor.extract_raw_text(pdf_path)
        self.assertIsInstance(text, list)
    
    def test_separate_glued_words(self):
        text = "ThisIsATest123ExampleHopeitworksforyou"
        cleaned = self.processor.separate_glued_words(text)
        self.assertEqual(cleaned, "This Is A Test 123 Example Hope it works for you")

if __name__ == '__main__':
    unittest.main()
