"""Max Agent - PDF summarization and context embedding for chat agents."""

from .pdf_summariser_app import PDFSummariserApp
from .pdf_processor import PDFProcessor
from .summariser import Summariser
from .config import Config

__version__ = "0.1.0"
__all__ = ["PDFSummariserApp", "PDFProcessor", "Summariser", "Config"]
