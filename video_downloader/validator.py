"""URL validation for video downloader."""

from urllib.parse import urlparse
import re


def validate_url(url: str) -> tuple[bool, str]:
    """Validate if the provided string is a valid URL.
    
    Args:
        url: URL string to validate.
    
    Returns:
        Tuple of (is_valid, error_message). If valid, error_message is empty.
    """
    if not url or not isinstance(url, str):
        return False, "URL cannot be empty"
    
    url = url.strip()
    
    try:
        result = urlparse(url)
        
        # Check if URL has scheme and netloc
        if not result.scheme:
            return False, "Invalid URL format: missing protocol (http:// or https://)"
        
        if not result.netloc:
            return False, "Invalid URL format: missing domain name"
        
        # Check if scheme is http or https
        if result.scheme not in ['http', 'https']:
            return False, f"Invalid URL protocol: {result.scheme}. Only http and https are supported"
        
        return True, ""
        
    except Exception as e:
        return False, f"Invalid URL format: {str(e)}"


def is_supported_platform(url: str) -> bool:
    """Check if URL is from a supported platform.
    
    Args:
        url: URL to check.
    
    Returns:
        True if platform is supported, False otherwise.
    """
    supported_patterns = [
        r'(youtube\.com|youtu\.be)',
        r'instagram\.com',
        r'facebook\.com',
        r'(t\.me|telegram\.org)',
    ]
    
    url_lower = url.lower()
    
    for pattern in supported_patterns:
        if re.search(pattern, url_lower):
            return True
    
    return False
