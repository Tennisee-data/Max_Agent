# main.py
import logging
import argparse
from .pdf_summariser_app import PDFSummariserApp


def parse_arguments():
    parser = argparse.ArgumentParser(description="PDF Summariser Max_Agent")
    parser.add_argument(
        "--config",
        type=str,
        default="config.yaml",
        help="Path to the YAML configuration file (default: config.yaml)",
    )
    return parser.parse_args()


def main():
    logging.basicConfig(
        filename="pdf_summariser.log",
        level=logging.DEBUG,  # Set to DEBUG to capture all levels
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    args = parse_arguments()
    app = PDFSummariserApp(config_file=args.config)
    app.run()


if __name__ == "__main__":
    main()
