#!/usr/bin/env python3
import os
import argparse
import subprocess
from typing import Optional

def download_youtube(self, url: str, output_dir: Optional[str] = None) -> str:
    """
    Download a YouTube video using yt-dlp.
    
    Args:
        url: YouTube URL
        output_dir: Directory to save the downloaded video (optional)
        
    Returns:
        Path to the downloaded video file
    """
    try:
        # Check if yt-dlp is installed
        subprocess.run(['yt-dlp', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: yt-dlp is not installed. Installing now...")
        try:
            subprocess.run(['pip', 'install', 'yt-dlp'], check=True)
            print("yt-dlp installed successfully!")
        except subprocess.CalledProcessError:
            raise RuntimeError("Failed to install yt-dlp. Please install it manually: pip install yt-dlp")
    
    if output_dir is None:
        output_dir = os.getcwd()
    
    os.makedirs(output_dir, exist_ok=True)
    
    output_template = os.path.join(output_dir, '%(title)s.%(ext)s')
    
    # Get video info first to get the title
    info_command = [
        'yt-dlp',
        '--print', 'filename',
        '--print', 'title',
        '--skip-download',
        '--output', output_template,
        url
    ]
    
    print(f"Fetching video information from YouTube...")
    result = subprocess.run(info_command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output_lines = result.stdout.strip().split('\n')
    if len(output_lines) < 2:
        raise RuntimeError("Failed to get video information")
    
    expected_filename = output_lines[0]
    video_title = output_lines[1]
    print(f"Video title: {video_title}")
    
    # Download the actual video
    download_command = [
        'yt-dlp',
        '--format', 'mp4',  # Force mp4 format
        '--output', output_template,
        url
    ]
    
    print(f"Downloading video from YouTube...")
    subprocess.run(download_command, check=True)
    
    # The filename might have been sanitized by yt-dlp
    # Look for the file that matches the expected title
    for file in os.listdir(output_dir):
        file_path = os.path.join(output_dir, file)
        if os.path.isfile(file_path) and any(file.endswith(ext) for ext in self.supported_extensions):
            if video_title.lower() in file.lower() or expected_filename.endswith(file):
                print(f"Video downloaded to {file_path}")
                return file_path
    
    raise FileNotFoundError(f"Downloaded video file not found in {output_dir}")


def main():
    parser = argparse.ArgumentParser(description='Download Youtube Video')
    parser.add_argument('url', type=str, help='YouTube URL')
    parser.add_argument('--output', '-o', type=str, help='Output directory for video')

    args = parser.parse_args()

    download_youtube(args.url, args.output)

    return 0

if __name__ == "__main__":
    exit(main())
