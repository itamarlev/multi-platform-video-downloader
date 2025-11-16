"""Command-line interface for video downloader."""

import argparse
import sys
import os
from typing import Optional

from .config import Config
from .validator import validate_url, is_supported_platform
from .detector import detect_platform, Platform
from .downloader import DownloadManager
from .exceptions import ValidationError
from .logger import setup_logging

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        # Try to set UTF-8 encoding for Windows console
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description='Download videos from YouTube, Instagram, Facebook, and Telegram',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Supported Platforms:
  - YouTube (youtube.com, youtu.be)
  - Instagram (instagram.com)
  - Facebook (facebook.com)
  - Telegram (t.me, telegram.org)

Examples:
  video-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ
  video-downloader https://www.instagram.com/p/ABC123/ --output-dir ~/Videos
  video-downloader https://t.me/channel/123
        """
    )
    
    parser.add_argument(
        'url',
        help='Video URL to download'
    )
    
    parser.add_argument(
        '--output-dir',
        '-o',
        dest='output_dir',
        help='Custom download directory (default: ~/Downloads/VideoDownloader)',
        default=None
    )
    
    return parser.parse_args()


def display_progress(progress_data: dict) -> None:
    """Display download progress to user.
    
    Args:
        progress_data: Progress information from yt-dlp.
    """
    if progress_data.get('status') == 'downloading':
        downloaded = progress_data.get('downloaded_bytes', 0)
        total = progress_data.get('total_bytes') or progress_data.get('total_bytes_estimate', 0)
        speed = progress_data.get('speed', 0)
        eta = progress_data.get('eta', 0)
        
        if total > 0:
            percentage = (downloaded / total) * 100
            
            # Format speed
            speed_str = f"{speed / 1024 / 1024:.1f} MB/s" if speed else "N/A"
            
            # Format ETA
            if eta:
                mins, secs = divmod(eta, 60)
                eta_str = f"{int(mins):02d}:{int(secs):02d}"
            else:
                eta_str = "N/A"
            
            # Create progress bar with safe characters
            bar_length = 30
            filled = int(bar_length * percentage / 100)
            
            # Use ASCII characters for Windows compatibility
            try:
                bar = '█' * filled + '░' * (bar_length - filled)
            except UnicodeEncodeError:
                # Fallback to ASCII characters
                bar = '#' * filled + '-' * (bar_length - filled)
            
            # Print progress (use \r to overwrite line)
            try:
                print(f"\r[{bar}] {percentage:.1f}% | {speed_str} | ETA: {eta_str}", end='', flush=True)
            except UnicodeEncodeError:
                # Fallback without special characters
                bar = '#' * filled + '-' * (bar_length - filled)
                print(f"\r[{bar}] {percentage:.1f}% | {speed_str} | ETA: {eta_str}", end='', flush=True)


def display_success(file_path: str, video_title: str) -> None:
    """Display success message.
    
    Args:
        file_path: Path to downloaded file.
        video_title: Title of the video.
    """
    try:
        print(f"\n✓ Downloaded: {video_title}")
    except UnicodeEncodeError:
        print(f"\n[OK] Downloaded: {video_title}")
    print(f"  Location: {file_path}")


def display_error(error_message: str, error_type: str = "error") -> None:
    """Display formatted error messages.
    
    Args:
        error_message: Error message to display.
        error_type: Type of error (for categorization).
    """
    try:
        print(f"\n✗ Error: {error_message}", file=sys.stderr)
    except UnicodeEncodeError:
        print(f"\n[ERROR] {error_message}", file=sys.stderr)


def main():
    """Entry point for the CLI application."""
    # Setup logging
    logger = setup_logging()
    
    try:
        # Parse arguments
        args = parse_arguments()
        url = args.url.strip()
        logger.info(f"Starting download for URL: {url}")
        
        # Load configuration
        config = Config()
        download_dir = args.output_dir if args.output_dir else config.get_download_directory()
        
        # Validate URL
        is_valid, error_msg = validate_url(url)
        if not is_valid:
            logger.error(f"URL validation failed: {error_msg}")
            display_error(error_msg)
            sys.exit(1)
        
        # Check if platform is supported
        if not is_supported_platform(url):
            platform = detect_platform(url)
            error_msg = f"Unsupported platform: {platform.value}"
            logger.error(error_msg)
            display_error(
                f"Unsupported platform: {platform.value}. "
                f"Supported platforms: YouTube, Instagram, Facebook, Telegram"
            )
            sys.exit(1)
        
        # Detect platform
        platform = detect_platform(url)
        print(f"Detected platform: {platform.value.capitalize()}")
        print(f"Download directory: {download_dir}")
        print(f"\nStarting download...")
        
        # Initialize download manager
        manager = DownloadManager(download_dir)
        
        # Download video
        result = manager.download_video(url, progress_callback=display_progress)
        
        # Display result
        if result.success:
            logger.info(f"Download successful: {result.video_title} -> {result.file_path}")
            display_success(result.file_path, result.video_title)
            sys.exit(0)
        else:
            logger.error(f"Download failed: {result.error_message}")
            display_error(result.error_message)
            sys.exit(1)
    
    except KeyboardInterrupt:
        logger.info("Download cancelled by user")
        print("\n\nDownload cancelled by user.")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Unexpected error: {str(e)}")
        display_error(f"Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
