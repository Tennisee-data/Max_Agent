# Max Agent - Professional PDF Summarization Tool

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)
![GitHub stars](https://img.shields.io/github/stars/Tennisee-data/Max_Agent)
![GitHub forks](https://img.shields.io/github/forks/Tennisee-data/Max_Agent)

A modern, production-ready Python package for intelligent PDF summarization with AI-powered text processing. Designed to condense large PDF documents while preserving critical information like code blocks and equations.

## Features

- **Smart Text Processing**: Enhanced word separation and text cleaning algorithms
- **AI-Powered Summarization**: Uses Facebook BART model for high-quality summaries  
- **Professional CLI**: Easy-to-use command-line interface with `max-agent` command
- **Flexible Configuration**: YAML-based settings for complete customization
- **Quality Output**: Generates clean, formatted PDF summaries
- **Modern Packaging**: Proper Python package with pip installation support
- **Fully Tested**: Comprehensive test suite with type hints throughout

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Tennisee-data/Max_Agent.git
cd Max_Agent

# Install the package
pip install -e .

# Run with your PDFs
max-agent --help
max-agent --log-level INFO
```

## Perfect For

- **ChatGPT Agent Optimization**: Condense support documents to maximize token efficiency
- **Document Analysis**: Quickly extract key information from large PDFs
- **Research Workflows**: Summarize academic papers and technical documents
- **Content Preparation**: Process documents for AI agent configurations

## Project Structure

```
src/max_agent/              # Main package
├── __init__.py             # Package initialization
├── cli.py                  # Command-line interface  
├── config.py               # Configuration management
├── pdf_processor.py        # Enhanced PDF processing
├── summariser.py           # AI summarization engine
├── pdf_generator.py        # PDF output generation
├── file_tracker.py         # Processing state management
└── config.yaml             # Default configuration

tests/                      # Test suite
├── test_pdf_processor.py   # Core functionality tests
└── ...

pyproject.toml             # Modern Python packaging
requirements.txt           # Dependencies
README.md                  # This file
```

## Configuration

Customize processing via `config.yaml`:

```yaml
# Input/Output directories
input_directory: "./pdfs/"
output_directory: "./summarised_pdfs/"
cleaned_text_directory: "./cleaned_texts/"

# AI Model settings
summarization_model_id: "facebook/bart-large-cnn"
max_tokens: 1024

# Summarization ratios
first_min_ratio: 0.25
first_max_ratio: 0.45
second_min_ratio: 0.60
second_max_ratio: 0.80
```

## Usage Examples

```bash
# Basic usage
max-agent

# Custom configuration
max-agent --config my_config.yaml

# Debug mode
max-agent --log-level DEBUG

# Check version
max-agent --version
```

## ChatGPT Agent Optimization

Originally designed to overcome ChatGPT's **20 PDF / 2M token limitations** by intelligently condensing source documents:

- **Token Efficiency**: Reduce document size while preserving key information
- **Smart Processing**: Handles complex document structures
- **Quality Preservation**: Maintains code blocks, equations, and critical details
- **Optimal Format**: Works best with single-column text PDFs (OpenAI recommended)

## Technical Details

- **Text Extraction**: Advanced PDF processing with `pdfplumber`
- **AI Model**: Facebook BART-large-CNN for summarization
- **Word Segmentation**: Intelligent text separation with `wordsegment`
- **Output Format**: Professional PDF generation with DejaVu fonts
- **Code Quality**: Black formatted, type-hinted, fully tested

## Requirements

- Python 3.8+
- Dependencies automatically installed via pip
- Compatible with CPU and GPU processing

## Development

```bash
# Install development dependencies
pip install -e .

# Run tests
python -m pytest tests/

# Code formatting
black src/max_agent/

# Linting
flake8 src/max_agent/
```

## How It Works

1. **PDF Ingestion**: Extracts text while preserving document structure
2. **Text Cleaning**: Advanced word separation and content cleaning
3. **Smart Chunking**: Divides content into optimal token-sized segments
4. **AI Summarization**: Uses BART model for intelligent condensation
5. **Content Preservation**: Maintains code blocks and equations separately
6. **PDF Generation**: Creates professional formatted summary documents

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**François REEVES** - [francois@reevesnco.com](mailto:francois@reevesnco.com)

## Acknowledgments

- Built with modern Python packaging standards
- Uses Facebook's BART model for summarization
- Powered by the transformers library
- Enhanced text processing with wordsegment

---

**Star this repo if Max Agent helped you optimize your ChatGPT agents!**