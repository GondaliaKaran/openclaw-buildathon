"""
Logging configuration and utilities.
"""

import logging
import sys
from pathlib import Path
from config import config


def setup_logging():
    """Setup logging configuration."""
    log_level = getattr(logging, config.logging.level.upper(), logging.INFO)
    log_file = config.logging.log_file
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # Reduce noise from external libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.INFO)
    
    logging.info("Logging initialized")
    logging.info(f"Log level: {config.logging.level}")
    logging.info(f"Log file: {log_file}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)
