"""Download manager for video downloader."""

from dataclasses import dataclass
from typing import Optional, Callable
import yt_dlp
from pathlib import Path
import shutil

from .detector import Platform, detect_platform
from .file_manager import sanitize_filename, resolve_filename_conflict, ensure_download_directory


def check_ffmpeg() -> tuple[bool, str]:
    """Check if FFmpeg is installed.
    
    Returns:
        Tuple of (is_installed, path_or_message)
    """
    ffmpeg_path = shutil.which('ffmpeg')
    if ffmpeg_path:
        return True, ffmpeg_path
    else:
        return False, "FFmpeg not found. Install it from https://ffmpeg.org/download.html"


@dataclass
class DownloadResult:
    """Result of a download operation."""
    success: bool
    file_path: Optional[str]
    error_message: Optional[str]
    video_title: str
    file_size: int = 0
    duration: float = 0.0
    platform: Platform = Platform.UNKNOWN


@dataclass
class VideoInfo:
    """Video metadata information."""
    title: str
    duration: float
    thumbnail_url: str
    available_qualities: list[str]
    platform: Platform
    uploader: str


class DownloadManager:
    """Manage video download operations using yt-dlp."""
    
    def __init__(self, download_dir: str):
        """Initialize download manager with target directory.
        
        Args:
            download_dir: Directory where videos will be saved.
        """
        self.download_dir = download_dir
        self._cancel_requested = False
        ensure_download_directory(download_dir)
        
        # Check for FFmpeg
        self.has_ffmpeg, self.ffmpeg_info = check_ffmpeg()
        if not self.has_ffmpeg:
            print(f"Warning: {self.ffmpeg_info}")
            print("Videos may not have audio merged properly without FFmpeg.")
    
    def get_video_info(self, url: str) -> VideoInfo:
        """Fetch video metadata without downloading.
        
        Args:
            url: Video URL.
        
        Returns:
            VideoInfo object with metadata.
        
        Raises:
            Exception: If unable to fetch video info.
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            # Get available formats/qualities
            qualities = []
            if 'formats' in info:
                for fmt in info['formats']:
                    if fmt.get('height'):
                        qualities.append(f"{fmt['height']}p")
            
            return VideoInfo(
                title=info.get('title', 'Unknown'),
                duration=info.get('duration', 0.0),
                thumbnail_url=info.get('thumbnail', ''),
                available_qualities=list(set(qualities)),
                platform=detect_platform(url),
                uploader=info.get('uploader', 'Unknown')
            )
    
    def download_video(self, url: str, progress_callback: Optional[Callable] = None, audio_only: bool = False) -> DownloadResult:
        """Download video from URL.
        
        Args:
            url: Video URL to download.
            progress_callback: Optional callback function for progress updates.
            audio_only: If True, download only audio and convert to MP3.
        
        Returns:
            DownloadResult with status and file information.
        """
        platform = detect_platform(url)
        self._cancel_requested = False
        
        def progress_hook(d):
            """Hook for yt-dlp progress updates."""
            if self._cancel_requested:
                raise Exception("Download cancelled by user")
            
            if progress_callback and d['status'] == 'downloading':
                progress_callback(d)
        
        # Sanitize output template
        output_template = str(Path(self.download_dir) / '%(title)s.%(ext)s')
        
        if audio_only:
            # Audio-only configuration
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'progress_hooks': [progress_hook],
                'quiet': False,
                'no_warnings': False,
                'extract_flat': False,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'prefer_ffmpeg': True,
            }
        else:
            # Video with audio configuration
            ydl_opts = {
                # Format selection: prefer formats with both video and audio
                # If separate streams, merge them. Fallback to best single file.
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best',
                'outtmpl': output_template,
                'progress_hooks': [progress_hook],
                'quiet': False,
                'no_warnings': False,
                'extract_flat': False,
                'merge_output_format': 'mp4',
                # Post-processing to ensure audio is merged
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                # Prefer formats with audio
                'prefer_ffmpeg': True,
            }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the actual downloaded file path
                filename = ydl.prepare_filename(info)
                
                # Handle filename conflicts
                final_path = resolve_filename_conflict(filename)
                if final_path != filename and Path(filename).exists():
                    Path(filename).rename(final_path)
                
                return DownloadResult(
                    success=True,
                    file_path=final_path,
                    error_message=None,
                    video_title=info.get('title', 'Unknown'),
                    file_size=info.get('filesize', 0) or info.get('filesize_approx', 0),
                    duration=info.get('duration', 0.0),
                    platform=platform
                )
        
        except Exception as e:
            error_msg = str(e)
            
            # Provide user-friendly error messages
            if 'private' in error_msg.lower() or 'unavailable' in error_msg.lower():
                error_msg = "Video is private, restricted, or unavailable"
            elif 'not found' in error_msg.lower() or '404' in error_msg:
                error_msg = "Video not found or has been deleted"
            elif 'network' in error_msg.lower() or 'connection' in error_msg.lower():
                error_msg = "Network error: Please check your internet connection"
            elif 'cancelled' in error_msg.lower():
                error_msg = "Download cancelled by user"
            
            return DownloadResult(
                success=False,
                file_path=None,
                error_message=error_msg,
                video_title='',
                platform=platform
            )
    
    def cancel_download(self) -> None:
        """Cancel ongoing download and clean up partial files."""
        self._cancel_requested = True
