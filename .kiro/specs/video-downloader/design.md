# Design Document

## Overview

The video downloader application will be built as a command-line interface (CLI) tool using Python, leveraging existing libraries like `yt-dlp` (a maintained fork of youtube-dl) which supports multiple platforms including YouTube, Instagram, Facebook, and Telegram. The application will provide a simple interface for users to input URLs and download videos in the best available quality.

The architecture follows a modular design with clear separation between URL validation, platform detection, download orchestration, and user interface components.

## Architecture

### High-Level Architecture

```
┌─────────────────┐
│   CLI Interface │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  URL Validator  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Platform Detector│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│Download Manager │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  File Manager   │
└─────────────────┘
```

### Technology Stack

- **Language**: Python 3.8+
- **Core Library**: yt-dlp (supports YouTube, Instagram, Facebook, Telegram, and 1000+ other sites)
- **CLI Framework**: argparse (built-in) or click for enhanced CLI experience
- **Progress Display**: tqdm for progress bars
- **URL Validation**: urllib.parse (built-in) and regex patterns

### Key Design Decisions

1. **Use yt-dlp instead of building custom scrapers**: yt-dlp is actively maintained, handles authentication, bypasses restrictions, and supports automatic quality selection. Building custom scrapers would require constant maintenance as platforms change their APIs.

2. **CLI-first approach**: Start with a command-line interface for simplicity and reliability. Can be extended to GUI later.

3. **Synchronous downloads**: Handle one download at a time to avoid complexity and resource issues. Future enhancement could add concurrent downloads.

4. **Local configuration file**: Store user preferences (download directory, quality preferences) in a JSON config file.

## Components and Interfaces

### 1. CLI Interface (`cli.py`)

**Responsibility**: Handle user input, display output, and coordinate the download workflow.

**Interface**:
```python
def main():
    """Entry point for the CLI application"""
    pass

def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments"""
    pass

def display_progress(progress_data: dict) -> None:
    """Display download progress to user"""
    pass

def display_error(error_message: str, error_type: str) -> None:
    """Display formatted error messages"""
    pass
```

### 2. URL Validator (`validator.py`)

**Responsibility**: Validate URL format and basic structure.

**Interface**:
```python
def validate_url(url: str) -> tuple[bool, str]:
    """
    Validate if the provided string is a valid URL
    Returns: (is_valid, error_message)
    """
    pass

def is_supported_platform(url: str) -> bool:
    """Check if URL is from a supported platform"""
    pass
```

### 3. Platform Detector (`detector.py`)

**Responsibility**: Identify which platform a URL belongs to.

**Interface**:
```python
class Platform(Enum):
    YOUTUBE = "youtube"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    TELEGRAM = "telegram"
    UNKNOWN = "unknown"

def detect_platform(url: str) -> Platform:
    """Detect the platform from URL"""
    pass
```

### 4. Download Manager (`downloader.py`)

**Responsibility**: Orchestrate the download process using yt-dlp, handle quality selection, and manage download lifecycle.

**Interface**:
```python
class DownloadManager:
    def __init__(self, download_dir: str):
        """Initialize download manager with target directory"""
        pass
    
    def download_video(self, url: str, progress_callback: callable) -> DownloadResult:
        """
        Download video from URL
        Returns: DownloadResult with status and file path
        """
        pass
    
    def get_video_info(self, url: str) -> dict:
        """Fetch video metadata without downloading"""
        pass
    
    def cancel_download(self) -> None:
        """Cancel ongoing download"""
        pass

class DownloadResult:
    success: bool
    file_path: str
    error_message: str
    video_title: str
```

### 5. File Manager (`file_manager.py`)

**Responsibility**: Handle file system operations, naming, and conflict resolution.

**Interface**:
```python
def ensure_download_directory(path: str) -> None:
    """Create download directory if it doesn't exist"""
    pass

def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    pass

def resolve_filename_conflict(filepath: str) -> str:
    """Generate unique filename if file already exists"""
    pass

def get_default_download_path() -> str:
    """Get default download directory path"""
    pass
```

### 6. Configuration Manager (`config.py`)

**Responsibility**: Manage user preferences and application settings.

**Interface**:
```python
class Config:
    def __init__(self):
        """Load configuration from file or create default"""
        pass
    
    def get_download_directory(self) -> str:
        """Get configured download directory"""
        pass
    
    def set_download_directory(self, path: str) -> None:
        """Update download directory preference"""
        pass
    
    def save(self) -> None:
        """Persist configuration to file"""
        pass
```

## Data Models

### DownloadResult
```python
@dataclass
class DownloadResult:
    success: bool
    file_path: Optional[str]
    error_message: Optional[str]
    video_title: str
    file_size: int  # in bytes
    duration: float  # in seconds
    platform: Platform
```

### VideoInfo
```python
@dataclass
class VideoInfo:
    title: str
    duration: float
    thumbnail_url: str
    available_qualities: list[str]
    platform: Platform
    uploader: str
```

### DownloadProgress
```python
@dataclass
class DownloadProgress:
    downloaded_bytes: int
    total_bytes: int
    speed: float  # bytes per second
    eta: float  # seconds remaining
    percentage: float
```

## Error Handling

### Error Categories

1. **Validation Errors**: Invalid URL format, unsupported platform
2. **Network Errors**: No internet connection, timeout, DNS failure
3. **Access Errors**: Private video, geo-restricted content, deleted video
4. **File System Errors**: Permission denied, disk full, invalid path
5. **Download Errors**: Interrupted download, corrupted file, extraction failure

### Error Handling Strategy

```python
class VideoDownloaderError(Exception):
    """Base exception for video downloader"""
    pass

class ValidationError(VideoDownloaderError):
    """URL validation failed"""
    pass

class NetworkError(VideoDownloaderError):
    """Network-related errors"""
    pass

class AccessError(VideoDownloaderError):
    """Video access denied or unavailable"""
    pass

class FileSystemError(VideoDownloaderError):
    """File system operation failed"""
    pass
```

Each component will:
- Catch specific exceptions and convert them to appropriate custom exceptions
- Log errors with full context for debugging
- Return user-friendly error messages
- Clean up partial downloads on failure

## Testing Strategy

### Unit Tests

- **URL Validator**: Test valid/invalid URLs, edge cases, malformed inputs
- **Platform Detector**: Test detection for each platform, edge cases
- **File Manager**: Test filename sanitization, conflict resolution, directory creation
- **Config Manager**: Test loading, saving, default values

### Integration Tests

- **Download Flow**: Test complete download workflow with mock yt-dlp responses
- **Error Handling**: Test error propagation through the system
- **Progress Callbacks**: Test progress reporting mechanism

### Manual Testing

- Test with real URLs from each platform (YouTube, Instagram, Facebook, Telegram)
- Test with various video qualities and formats
- Test error scenarios (private videos, deleted videos, network issues)
- Test on different operating systems (Windows, macOS, Linux)

### Test Data

- Create a set of test URLs for each platform (public videos that are unlikely to be deleted)
- Mock yt-dlp responses for predictable testing
- Test with various filename edge cases (special characters, long names, unicode)

## Implementation Notes

### yt-dlp Configuration

The download manager will configure yt-dlp with these options:
```python
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # Best quality
    'outtmpl': '%(title)s.%(ext)s',  # Output template
    'progress_hooks': [progress_callback],  # Progress tracking
    'quiet': False,  # Show output
    'no_warnings': False,  # Show warnings
    'extract_flat': False,  # Extract full info
}
```

### Quality Selection Priority

1. Best video + best audio (merged)
2. Best single file with video and audio
3. Best available format

### File Naming Convention

- Use video title as base filename
- Sanitize special characters: `< > : " / \ | ? *`
- Limit filename length to 255 characters
- Append platform name if title is generic
- Add counter suffix for duplicates: `video.mp4`, `video (1).mp4`, `video (2).mp4`

### Progress Reporting

- Update progress every 0.5 seconds
- Display: `[████████░░] 80% | 15.2 MB/s | ETA: 00:05`
- Show final message: `✓ Downloaded: video_title.mp4 (125.5 MB)`

### Platform-Specific Considerations

- **YouTube**: May require cookies for age-restricted content
- **Instagram**: Stories vs posts have different URL patterns
- **Facebook**: May require authentication for private videos
- **Telegram**: Direct file downloads, simpler than other platforms
