#!/usr/bin/env python3
import os
import argparse
import subprocess
import tempfile
import time
from typing import List, Optional
import whisper
from tqdm import tqdm


class VideoTranscriber:
    """A class to handle video transcription using ffmpeg and OpenAI's Whisper."""

    def __init__(self, model_size: str = "medium", device: str = "cpu"):
        """
        Initialize the transcriber with the specified model size.
        
        Args:
            model_size: Size of the Whisper model to use ('tiny', 'base', 'small', 'medium', 'large')
            device: Device to run the model on ('cpu' or 'cuda' for GPU)
        """
        print(f"Loading Whisper model '{model_size}'...")
        self.model = whisper.load_model(model_size, device=device)
        self.supported_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.wmv', '.flv']
        print(f"Model loaded and ready to transcribe!")

    def extract_audio(self, video_path: str, output_path: Optional[str] = None) -> str:
        """
        Extract audio from a video file using ffmpeg.
        
        Args:
            video_path: Path to the video file
            output_path: Path to save the extracted audio (optional)
            
        Returns:
            The path to the extracted audio file
        """
        if output_path is None:
            # Create a temporary file with .wav extension
            fd, output_path = tempfile.mkstemp(suffix='.wav')
            os.close(fd)

        command = [
            'ffmpeg',
            '-i', video_path,
            '-q:a', '0',
            '-map', 'a',
            '-y',  # Overwrite output file if it exists
            output_path
        ]

        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return output_path
        except subprocess.CalledProcessError as e:
            print(f"Error extracting audio: {e}")
            if os.path.exists(output_path):
                os.remove(output_path)
            raise

    def transcribe_audio(self, audio_path: str, language: Optional[str] = None) -> dict:
        """
        Transcribe audio using Whisper.
        
        Args:
            audio_path: Path to the audio file
            language: Language code for transcription (optional)
            
        Returns:
            The transcription result
        """
        transcribe_options = {}
        if language:
            transcribe_options["language"] = language
            
        return self.model.transcribe(audio_path, **transcribe_options)

    def transcribe_video(self, video_path: str, output_dir: Optional[str] = None, 
                        language: Optional[str] = None, keep_audio: bool = False) -> str:
        """
        Transcribe a video file.
        
        Args:
            video_path: Path to the video file
            output_dir: Directory to save the transcription (optional)
            language: Language code for transcription (optional)
            keep_audio: Whether to keep the extracted audio file
            
        Returns:
            Path to the transcription file
        """
        video_path = os.path.abspath(video_path)
        video_filename = os.path.basename(video_path)
        video_name = os.path.splitext(video_filename)[0]
        
        if output_dir is None:
            output_dir = os.path.dirname(video_path)
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Extract audio
        print(f"Extracting audio from {video_filename}...")
        audio_path = os.path.join(output_dir, f"{video_name}.wav") if keep_audio else None
        audio_path = self.extract_audio(video_path, audio_path)
        
        # Transcribe audio
        print(f"Transcribing audio...")
        start_time = time.time()
        result = self.transcribe_audio(audio_path, language)
        end_time = time.time()
        
        # Clean up temporary audio file if we're not keeping it
        if not keep_audio and audio_path.startswith(tempfile.gettempdir()):
            os.remove(audio_path)
            
        # Save transcription
        transcription_path = os.path.join(output_dir, f"{video_name}.txt")
        with open(transcription_path, 'w', encoding='utf-8') as f:
            f.write(result["text"])
            
        # Also save timestamps if available
        if "segments" in result:
            srt_path = os.path.join(output_dir, f"{video_name}.srt")
            with open(srt_path, 'w', encoding='utf-8') as f:
                for i, segment in enumerate(result["segments"], 1):
                    start = self._format_timestamp(segment["start"])
                    end = self._format_timestamp(segment["end"])
                    f.write(f"{i}\n")
                    f.write(f"{start} --> {end}\n")
                    f.write(f"{segment['text'].strip()}\n\n")
        
        print(f"Transcription completed in {end_time - start_time:.2f} seconds")
        print(f"Transcription saved to {transcription_path}")
        return transcription_path
        
    def transcribe_directory(self, directory: str, output_dir: Optional[str] = None, 
                           language: Optional[str] = None, keep_audio: bool = False) -> List[str]:
        """
        Transcribe all video files in a directory.
        
        Args:
            directory: Path to the directory containing video files
            output_dir: Directory to save the transcriptions (optional)
            language: Language code for transcription (optional)
            keep_audio: Whether to keep the extracted audio files
            
        Returns:
            List of paths to the transcription files
        """
        directory = os.path.abspath(directory)
        if output_dir is None:
            output_dir = directory
            
        os.makedirs(output_dir, exist_ok=True)
        
        transcription_paths = []
        video_files = []
        
        # Find all video files
        for root, _, files in os.walk(directory):
            for file in files:
                if any(file.lower().endswith(ext) for ext in self.supported_extensions):
                    video_files.append(os.path.join(root, file))
        
        if not video_files:
            print(f"No video files found in {directory}")
            return []
        
        print(f"Found {len(video_files)} video files to transcribe")
        
        # Transcribe each video
        for video_path in tqdm(video_files, desc="Transcribing videos"):
            try:
                transcription_path = self.transcribe_video(
                    video_path, output_dir, language, keep_audio
                )
                transcription_paths.append(transcription_path)
            except Exception as e:
                print(f"Error transcribing {video_path}: {e}")
                
        return transcription_paths
    
    def _format_timestamp(self, seconds: float) -> str:
        """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
        hours = int(seconds // 3600)
        seconds %= 3600
        minutes = int(seconds // 60)
        seconds %= 60
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d},{milliseconds:03d}"


def main():
    parser = argparse.ArgumentParser(description='Transcribe video files using Whisper')
    parser.add_argument('path', type=str, help='Path to video file or directory')
    parser.add_argument('--output', '-o', type=str, help='Output directory for transcriptions')
    parser.add_argument('--model', '-m', type=str, default='medium',
                        choices=['tiny', 'base', 'small', 'medium', 'large'],
                        help='Whisper model size')
    parser.add_argument('--language', '-l', type=str, help='Language code (optional)')
    parser.add_argument('--keep-audio', '-k', action='store_true', 
                        help='Keep extracted audio files')
    parser.add_argument('--device', '-d', type=str, default='cpu',
                        choices=['cpu', 'cuda'], help='Device to run Whisper on')
    
    args = parser.parse_args()
    
    try:
        # Check if ffmpeg is installed
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: ffmpeg is not installed or not in PATH. Please install ffmpeg.")
        return 1
    
    # Initialize the transcriber
    transcriber = VideoTranscriber(model_size=args.model, device=args.device)
    
    # Check if the path is a file or directory
    path = os.path.abspath(args.path)
    if os.path.isfile(path):
        # Transcribe a single file
        if not any(path.lower().endswith(ext) for ext in transcriber.supported_extensions):
            print(f"Error: The file {path} is not a supported video format.")
            return 1
        
        transcriber.transcribe_video(
            path, args.output, args.language, args.keep_audio
        )
    elif os.path.isdir(path):
        # Transcribe all videos in the directory
        transcriber.transcribe_directory(
            path, args.output, args.language, args.keep_audio
        )
    else:
        print(f"Error: The path {path} does not exist.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())