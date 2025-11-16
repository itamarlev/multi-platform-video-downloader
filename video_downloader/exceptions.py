"""Custom exceptions for video downloader."""


class VideoDownloaderError(Exception):
    """Base exception for video downloader."""
    pass


class ValidationError(VideoDownloaderError):
    """URL validation failed."""
    pass


class NetworkError(VideoDownloaderError):
    """Network-related errors."""
    pass


class AccessError(VideoDownloaderError):
    """Video access denied or unavailable."""
    pass


class FileSystemError(VideoDownloaderError):
    """File system operation failed."""
    pass
