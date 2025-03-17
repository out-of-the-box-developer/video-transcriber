# Video Transcriber

A command-line tool for transcribing video files using FFmpeg and OpenAI's Whisper model.

## Features

- Transcribe single video files or entire directories
- Generate both text and SRT subtitle files
- Support for multiple languages
- GPU acceleration (optional)
- Multiple Whisper model sizes for balancing speed vs. accuracy

## Installation

### Prerequisites

- Python 3.7+
- FFmpeg (see troubleshooting below if not installed)

### Quick Install

```bash
# Clone the repository
git clone https://github.com/yugoccp/video-transcriber.git
cd video-transcriber

# Install FFMpeg
python install-ffmpeg.py

# Install with pip
pip install -e .

# Or install with pipx for isolated environment (recommended)
pipx install .
```

## Usage

Basic usage:

```bash
# Transcribe a single video file
video-transcriber path/to/video.mp4

# Transcribe all videos in a directory
video-transcriber path/to/videos/
```

Advanced options:

```bash
# Choose model size (tiny, base, small, medium, large)
video-transcriber video.mp4 --model medium

# Specify output directory
video-transcriber video.mp4 --output transcripts/

# Specify language for better accuracy
video-transcriber video.mp4 --language en

# Use GPU acceleration
video-transcriber video.mp4 --device cuda

# Keep the extracted audio files
video-transcriber video.mp4 --keep-audio
```

Download Youtube videos to transcript:
```bash
python download-youtube.py <YOUTUBE_URL> --output youtube/

video-transcriber youtube/ --output transcripts/
```

## Supported Video Formats

- MP4 (.mp4)
- AVI (.avi)
- MOV (.mov)
- MKV (.mkv)
- WebM (.webm)
- WMV (.wmv)
- FLV (.flv)

## Troubleshooting

### FFmpeg Not Found

#### Windows
1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html)
2. Extract the files to a directory (e.g., `C:\ffmpeg`)
3. Add the bin directory to your PATH:
   - Right-click on "This PC" → Properties → Advanced system settings
   - Click on "Environment Variables"
   - Edit the "Path" variable and add the bin directory (e.g., `C:\ffmpeg\bin`)
   - Restart your command prompt

#### Linux
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# Fedora
sudo dnf install ffmpeg

# Arch Linux
sudo pacman -S ffmpeg
```

#### macOS
```bash
# Using Homebrew
brew install ffmpeg
```

### CUDA Issues

If you encounter errors when using `--device cuda`:
1. Verify you have a compatible NVIDIA GPU
2. Ensure you have the correct CUDA drivers installed
3. If issues persist, use `--device cpu` instead

### Memory Issues with Large Files

For very large video files:
1. Try using a smaller model: `--model base` or `--model small`
2. Ensure you have sufficient disk space for temporary files

### Missing Dependencies

If you see import errors:
```bash
pip install openai-whisper tqdm
```

## License

MIT