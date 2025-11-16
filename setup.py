from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="video-downloader",
    version="1.0.0",
    author="Video Downloader",
    description="Download videos from YouTube, Instagram, Facebook, and Telegram",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "yt-dlp>=2023.10.13",
        "tqdm>=4.66.0",
    ],
    entry_points={
        "console_scripts": [
            "video-downloader=video_downloader.cli:main",
        ],
    },
)
