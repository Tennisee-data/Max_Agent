Max_Agent 
PDF Summariser App

A tool to summarise PDF documents, preserving important elements like code blocks and equations. Ideal for quickly understanding large documents or extracting key information without losing critical details (varies with settings and sources). It is originally intended to save on "tokens" when using support PDFs in the configuration of a ChatGPT Agent, limited to 20 PDFs or 2 million tokens. OpenAI says that one column of text PDFs work best as support documents for their agents. They ignore multimedia, images, audio and urls when tokenization occur. When they BPE (Byte Pair Encoding) your content, text content is extracted and tokenized. We are also told that the parser cannot understand context for text in columns like in a PowerPoint. The idea here is to let you tweak and experiment with PDFs such that you can push the limits of your ChatGPT Agent limitations by "condensing" your source documents.


Table of Contents
Features
Installation
Configuration
Usage
Attribution
Acknowledgments
Contributing
License
Contact


Features
Automated Summarisation: Quickly condense lengthy PDFs into concise summaries.
Preserves Code and Equations: Maintains critical code blocks and mathematical equations in the summaries.
Customisable Summarisation Ratios: Fine-tune the level of detail in summaries to suit your needs.
Logging and Tracking: Keep track of processed files and maintain logs for transparency. You can keep adding PDFs in between runs. 
PDFs already processed will be ignored.
User-Friendly Configuration: Easily configure directories, models, and settings via YAML files.
GPU Support: Utilise CUDA-enabled GPUs for faster processing if available.

Text Extraction:
Uses pdfplumber to extract raw text from each page of the PDF.

Text Cleaning and Normalisation:
Functions like separate_glued_words, clean_and_normalise_text, and final_text_cleaning are used to fix spacing issues, remove unwanted characters, and ensure proper formatting.

Code and Equation Extraction:
Extracts code blocks and equations from the text using regex patterns.

Text Binning:
Splits the cleaned text into manageable chunks based on token counts to comply with model limitations.

Summarisation:
Utilises a transformer-based summarisation model (facebook/bart-large-cnn) to summarise each chunk.

PDF Generation:
Uses FPDF to generate the final summarised PDF, ensuring proper font registration and handling.

Logging and Process Tracking:
Implements logging to track the process flow and maintains a log of processed PDFs to avoid reprocessing.


Installation
Prerequisites
Python 3.10 or higher (3.10 is ideal for torch)
Conda (optional but recommended for managing environments)


Steps
Clone the Repository


git clone https://github.com/yourusername/pdf-summariser-app.git
cd pdf-summariser-app
Create a Virtual Environment

Using Conda:

conda create -n pdf_summariser python=3.10
conda activate pdf_summariser

Or using venv:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies
pip install -r requirements.txt

Download Required Fonts
Ensure that the dejavu-sans directory contains the necessary .ttf files:

DejaVuSans.ttf
DejaVuSans-Bold.ttf
DejaVuSans-Oblique.ttf
DejaVuSans-BoldOblique.ttf

If these files are missing, download them from the DejaVu Fonts Repository and place them in the dejavu-sans directory.

Configuration
Customise your summarisation settings by editing the config.yaml file.

# config.yaml

input_directory: "./pdfs/"
output_directory: "./summarised_pdfs/"
cleaned_text_directory: "./cleaned_texts/"
font_directory: "./dejavu-sans/"
processed_files_log: "./processed_pdfs.txt"
log_file: "pdf_summariser.log"
summarization_model_id: "facebook/bart-large-cnn"
first_min_ratio: 0.25
first_max_ratio: 0.45
second_min_ratio: 0.60
second_max_ratio: 0.80
max_tokens: 1024
do_sample: false

Configuration Parameters
input_directory: Directory containing PDFs to summarise. 
output_directory: Directory to save summarised PDFs.
cleaned_text_directory: Directory to save cleaned text files.
font_directory: Directory containing font files.
processed_files_log: File to track processed PDFs.
log_file: File to store logs.
summarization_model_id: Model identifier for "summarization" parameter.
first_min_ratio / first_max_ratio: Ratios for initial summarisation.
second_min_ratio / second_max_ratio: Ratios for secondary summarisation.
max_tokens: Maximum number of tokens per summary chunk.
do_sample: Whether to use sampling in summarisation.

Usage
Running the Application
To start the PDF summariser, use the following command:

python main.py --config config.yaml
Command-Line Arguments
--config: Path to the YAML configuration file. Defaults to config.yaml if not specified.

Example:

python main.py --config custom_config.yaml

Attribution
If you use or reference this project in your work, please consider the following ways to give credit:

Cite this repository: Include a link to the repository URL in your project's documentation or acknowledgments.
Mention the author: Attribute the project to François REEVES.

This project is based on PDF Summariser App by François REEVES.

Acknowledgments
OpenAI: For providing foundational AI models.
ChatGPT: For being so verbose in the mini mode... you're almost a friend. ;)
DejaVu Fonts: For supplying the fonts used in the application. https://dejavu-fonts.github.io/
Community Contributors: Special thanks to all the contributors who help improve the project.
Inspirations: Inspired by various PDF processing and summarisation tools and best practices. The idea came when I wanted to pack and optimise the PDFs 
I could use to provide context in the configuration of an OpenAI ChatGPT Agent specialised in Python and Streamlit. 

Contributing
Contributions are welcome! Please follow these steps to contribute to the project:

Fork the Repository

Click the Fork button at the top-right corner of this page.

Create a New Branch

git checkout -b feature/YourFeature
Commit Your Changes

git commit -m "Add Your Feature"
Push to the Branch

git push origin feature/YourFeature
Open a Pull Request

Navigate to the original repository and open a pull request with a detailed description of your changes.

Contribution Guidelines
Code Quality: Ensure your code follows the project's coding standards and is well-documented.
Testing: Include tests for new features or bug fixes.
Documentation: Update the README or other documentation as necessary.
License
This project is licensed under the MIT License.

Contact
For any inquiries, support, or contributions, please contact François REEVES or open an issue in the repository.