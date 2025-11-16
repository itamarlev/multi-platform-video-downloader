"""Platform detection for video downloader."""

from enum import Enum
import re


class Platform(Enum):
    """Supported video platforms."""
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TELEGRAM = "telegram"
    UNKNOWN = "unknown"


def detect_platform(url: str) -> Platform:
    """Detect the platform from URL.
    
    Args:
        url: URL to analyze.
    
    Returns:
        Platform enum value.
    """
    url_lower = url.lower()
    
    # YouTube patterns
    if re.search(r'(youtube\.com|youtu\.be)', url_lower):
        return Platform.YOUTUBE
    
    # Instagram patterns
    if re.search(r'instagram\.com', url_lower):
        return Platform.INSTAGRAM
    
    # Facebook patterns
    if re.search(r'facebook\.com', url_lower):
        return Platform.FACEBOOK
    
    # Telegram patterns
    if re.search(r'(t\.me|telegram\.org)', url_lower):
        return Platform.TELEGRAM
    
    return Platform.UNKNOWN
