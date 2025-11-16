# Video Downloader

A simple command-line tool to download videos from YouTube, Instagram, Facebook, and Telegram in the best available quality.

## Features

- 🎥 Download videos from multiple platforms (YouTube, Instagram, Facebook, Telegram)
- 🎯 Automatically selects the best quality available
- 📊 Real-time download progress with speed and ETA
- 📁 Automatic file naming and conflict resolution
- 🔧 Configurable download directory
- 📝 Detailed logging for troubleshooting

## Supported Platforms

- **YouTube** (youtube.com, youtu.be) - Up to 4K resolution
- **Instagram** (instagram.com) - Posts and videos
- **Facebook** (facebook.com) - Public videos
- **Telegram** (t.me, telegram.org) - Channel videos

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- **FFmpeg** (required for merging video and audio streams)

### Install FFmpeg

FFmpeg is required to merge video and audio streams for the best quality downloads.

**Windows:**
1. Download from https://ffmpeg.org/download.html or use Chocolatey:
   ```bash
   choco install ffmpeg
   ```
2. Or use winget:
   ```bash
   winget install ffmpeg
   ```

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Linux (Fedora):**
```bash
sudo dnf install ffmpeg
```

Verify FFmpeg installation:
```bash
ffmpeg -version
```

### Install from source

1. Clone or download this repository
2. Navigate to the project directory
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Install the package:

```bash
pip install -e .
```

## Usage

### Basic Usage

Download a video by providing its URL:

```bash
video-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Custom Download Directory

Specify a custom output directory:

```bash
video-downloader https://www.instagram.com/p/ABC123/ --output-dir ~/Videos
```

Or use the short form:

```bash
video-downloader https://t.me/channel/123 -o ~/Videos
```

### Using as Python Module

You can also run the downloader as a Python module:

```bash
python -m video_downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

## Examples

### YouTube Video
```bash
video-downloader https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### Instagram Post
```bash
video-downloader https://www.instagram.com/p/ABC123/
```

### Facebook Video
```bash
video-downloader https://www.facebook.com/watch?v=123456789
```

### Telegram Video
```bash
video-downloader https://t.me/channel/123
```

## Configuration

The application stores configuration in `~/.video_downloader/config.json`.

Default download directory: `~/Downloads/VideoDownloader`

You can change the download directory using the `--output-dir` flag, or by editing the config file directly.

## Troubleshooting

### Common Issues

**"Downloaded video has no audio"**
- FFmpeg is not installed or not in your system PATH
- Install FFmpeg following the instructions above
- Restart your terminal after installation
- Verify with: `ffmpeg -version`

**"Video is private, restricted, or unavailable"**
- The video may require authentication or is not publicly accessible
- Try accessing the video in your browser first to verify it's available

**"Video not found or has been deleted"**
- The URL may be incorrect or the video has been removed
- Verify the URL is correct and the video still exists

**"Network error: Please check your internet connection"**
- Check your internet connection
- Some platforms may have rate limiting - try again later
- Your IP may be blocked by the platform

**"Unsupported platform"**
- The URL is from a platform not currently supported
- Supported platforms: YouTube, Instagram, Facebook, Telegram

### Logs

Detailed logs are stored in `~/.video_downloader/video_downloader.log`

Check the log file for more information about errors:

```bash
# On Windows
type %USERPROFILE%\.video_downloader\video_downloader.log

# On macOS/Linux
cat ~/.video_downloader/video_downloader.log
```

### Platform-Specific Notes

**YouTube:**
- Age-restricted videos may require additional authentication
- Some videos may be geo-restricted

**Instagram:**
- Private accounts require authentication
- Stories have limited availability

**Facebook:**
- Private videos cannot be downloaded
- Some videos may require login

**Telegram:**
- Public channel videos work best
- Private channels may require authentication

## Dependencies

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video download engine
- [tqdm](https://github.com/tqdm/tqdm) - Progress bar display

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Disclaimer

This tool is for personal use only. Please respect copyright laws and the terms of service of the platforms you're downloading from. Only download content you have the right to download.
