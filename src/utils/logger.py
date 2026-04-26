"""
Logging Configuration
Structured logging using Loguru
"""

import sys
from loguru import logger
from pathlib import Path


def setup_logging(log_level="INFO", log_file=None):
    """Configure structured logging for Ghost-OS"""
    
    # Remove default handler
    logger.remove()
    
    # Console handler with colors
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=log_level,
        colorize=True
    )
    
    # File handler (optional)
    if log_file:
        logger.add(
            log_file,
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function} - {message}",
            level="DEBUG",
            rotation="10 MB",
            retention="1 week",
            compression="zip"
        )
    
    logger.info("Logging configured")
    return logger
