#!/usr/bin/env python3
"""Command Line Interface for Max Agent PDF Summarization."""

import logging
import argparse
import os
import sys
from pathlib import Path
from typing import Optional

from .pdf_summariser_app import PDFSummariserApp


def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging configuration."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler("max_agent.log")
        ]
    )


def find_config_file() -> Optional[str]:
    """Find the config.yaml file in various locations."""
    possible_locations = [
        "config.yaml",
        "src/max_agent/config.yaml",
        Path(__file__).parent / "config.yaml",
    ]
    
    for location in possible_locations:
        if Path(location).exists():
            return str(location)
    
    return None


def main() -> None:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Max Agent - PDF Summarization Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  max-agent                     # Use default config.yaml
  max-agent --config my.yaml   # Use custom config file
  max-agent --log-level DEBUG  # Enable debug logging
        """
    )
    
    parser.add_argument(
        "--config",
        type=str,
        help="Path to the YAML configuration file"
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level (default: INFO)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Max Agent v0.1.0"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    # Find config file
    config_file = args.config
    if not config_file:
        config_file = find_config_file()
        if not config_file:
            logger.error(
                "No config.yaml file found. Please create one or specify with --config"
            )
            sys.exit(1)
    
    if not os.path.exists(config_file):
        logger.error(f"Config file not found: {config_file}")
        sys.exit(1)
    
    logger.info(f"Using config file: {config_file}")
    
    try:
        # Initialize and run the PDF summarizer
        app = PDFSummariserApp(config_file=config_file)
        app.run()
        logger.info("PDF summarization completed successfully.")
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user.")
        sys.exit(130)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        if args.log_level == "DEBUG":
            import traceback
            logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()