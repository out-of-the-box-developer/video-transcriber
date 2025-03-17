from setuptools import setup

setup(
    name="video-transcriber",
    version="0.1.0",
    py_modules=["video_transcriber"],
    install_requires=[
        "openai-whisper",
        "tqdm",
        "yt_dlp",
    ],
    entry_points={
        "console_scripts": [
            "video-transcriber=video_transcriber:main",
        ],
    },
)