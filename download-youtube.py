import os
import argparse
import yt_dlp

def download_audio(url, output_dir):
    # yt-dlp options:
    # - 'format': selects the best available audio format
    # - 'outtmpl': output file template (you can include directory and filename)
    # - 'postprocessors': extracts audio and converts to MP3 (requires ffmpeg installed)
    filename = '/%(title)s.%(ext)s'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, filename),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def main():
    parser = argparse.ArgumentParser(description='Download Youtube Audio')
    parser.add_argument('url', type=str, help='YouTube URL')
    parser.add_argument('--output', '-o', type=str, default=".", help='Output directory for audio')

    args = parser.parse_args()

    download_audio(url=args.url, output_dir=args.output)

    return 0

if __name__ == "__main__":
    exit(main())
