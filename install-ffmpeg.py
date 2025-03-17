def check_ffmpeg():
    """Check if FFmpeg is installed and available in PATH."""
    import subprocess
    import platform
    import os
    from pathlib import Path
    
    try:
        subprocess.run(['ffmpeg', '-version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("FFmpeg not found. Attempting to install or provide instructions...")
        
        system = platform.system().lower()
        
        if system == 'linux':
            # Linux installation instructions
            try:
                print("Attempting to install FFmpeg using apt-get...")
                subprocess.run(['sudo', 'apt-get', 'update'], check=True)
                subprocess.run(['sudo', 'apt-get', 'install', '-y', 'ffmpeg'], check=True)
                print("FFmpeg installed successfully!")
                return True
            except:
                print("\nAutomatic installation failed. Please install FFmpeg manually:")
                print("For Ubuntu/Debian: sudo apt-get install ffmpeg")
                print("For Fedora: sudo dnf install ffmpeg")
                print("For Arch Linux: sudo pacman -S ffmpeg")
        elif system == 'darwin':
            # MacOS installation instructions
            try:
                # Check if Homebrew is installed
                subprocess.run(['brew', '--version'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("Attempting to install FFmpeg using Homebrew...")
                subprocess.run(['brew', 'install', 'ffmpeg'], check=True)
                print("FFmpeg installed successfully!")
                return True
            except:
                print("\nAutomatic installation failed. Please install FFmpeg manually:")
                print("Install Homebrew from https://brew.sh/ then run: brew install ffmpeg")
        elif system == 'windows':
            # Windows installation instructions
            print("\nPlease install FFmpeg manually:")
            print("1. Download FFmpeg from https://ffmpeg.org/download.html")
            print("2. Extract the files to a directory (e.g., C:\\ffmpeg)")
            print("3. Add the bin directory to your PATH environment variable")
            print("   (e.g., C:\\ffmpeg\\bin)")
        
        return False
    
if __name__ == "__main__":
    check_ffmpeg()