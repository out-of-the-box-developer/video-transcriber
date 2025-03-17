#!/usr/bin/env python3
import argparse
from pytube import YouTube

def download_video(url, path='.'):
    try:
        yt = YouTube(url)
        # Select the highest resolution stream available
        stream = yt.streams.get_lowest_resolution()
        print(f"Downloading: {yt.title}")
        stream.download(output_path=path)
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")


def download_audio(url, path='.'):
    try:
        yt = YouTube(url)
        # Filter streams to get only audio streams and pick the first available
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream is None:
            print("No audio stream found for this video.")
            return
        print(f"Downloading audio for: {yt.title}")
        audio_stream.download(output_path=path)
        print("Download completed!")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(description='Download Youtube Video')
    parser.add_argument('url', type=str, help='YouTube URL')
    parser.add_argument('--output', '-o', type=str, help='Output directory for video')

    args = parser.parse_args()

    download_audio(url=args.url, path=args.output)

    return 0

if __name__ == "__main__":
    exit(main())
