"""Logging configuration for video downloader."""

import logging
from pathlib import Path


def setup_logging():
    """Configure logging to write errors and debug info to log file."""
    log_dir = Path.home() / ".video_downloader"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "video_downloader.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
        ]
    )
    
    return logging.getLogger('video_downloader')
