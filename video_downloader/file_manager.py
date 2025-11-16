"""File management utilities for video downloader."""

import os
import re
from pathlib import Path


def ensure_download_directory(path: str) -> None:
    """Create download directory if it doesn't exist.
    
    Args:
        path: Directory path to create.
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename.
    
    Args:
        filename: Original filename.
    
    Returns:
        Sanitized filename safe for file system.
    """
    # Remove invalid characters for Windows/Unix: < > : " / \ | ? *
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    
    # Replace multiple spaces with single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Trim whitespace
    sanitized = sanitized.strip()
    
    # Limit filename length (255 is typical max, leave room for extension)
    max_length = 200
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length].strip()
    
    # If filename is empty after sanitization, use default
    if not sanitized:
        sanitized = "video"
    
    return sanitized


def resolve_filename_conflict(filepath: str) -> str:
    """Generate unique filename if file already exists.
    
    Args:
        filepath: Original file path.
    
    Returns:
        Unique file path that doesn't exist.
    """
    if not os.path.exists(filepath):
        return filepath
    
    path = Path(filepath)
    directory = path.parent
    stem = path.stem
    extension = path.suffix
    
    counter = 1
    while True:
        new_filename = f"{stem} ({counter}){extension}"
        new_filepath = directory / new_filename
        
        if not new_filepath.exists():
            return str(new_filepath)
        
        counter += 1


def get_default_download_path() -> str:
    """Get default download directory path.
    
    Returns:
        Path to default download directory.
    """
    return str(Path.home() / "Downloads" / "VideoDownloader")
