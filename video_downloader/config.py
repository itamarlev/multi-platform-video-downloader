"""Configuration management for video downloader."""

import json
import os
from pathlib import Path
from typing import Optional


class Config:
    """Manage user preferences and application settings."""
    
    DEFAULT_CONFIG_DIR = Path.home() / ".video_downloader"
    DEFAULT_CONFIG_FILE = DEFAULT_CONFIG_DIR / "config.json"
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.
        
        Args:
            config_path: Optional path to config file. Uses default if not provided.
        """
        self.config_path = Path(config_path) if config_path else self.DEFAULT_CONFIG_FILE
        self.config_data = self._load_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file or create default."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                # If config is corrupted, return default
                return self._get_default_config()
        else:
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration."""
        return {
            "download_directory": str(Path.home() / "Downloads" / "VideoDownloader")
        }
    
    def get_download_directory(self) -> str:
        """Get configured download directory.
        
        Returns:
            Path to download directory as string.
        """
        return self.config_data.get("download_directory", 
                                   self._get_default_config()["download_directory"])
    
    def set_download_directory(self, path: str) -> None:
        """Update download directory preference.
        
        Args:
            path: New download directory path.
        """
        self.config_data["download_directory"] = path
    
    def save(self) -> None:
        """Persist configuration to file."""
        # Ensure config directory exists
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config_data, f, indent=2)
