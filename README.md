# EasyDownloader

A simple and user-friendly video/audio downloader with support for multiple platforms like YouTube, Twitter, and Instagram.


## Features

- Download videos from:
  - YouTube
  - Twitter/X
  - Instagram
- Extract audio from YouTube videos (MP3)
- Multi-language support (English/Spanish)
- Progress bar and console output
- Simple and intuitive interface

## Requirements

- Python 3.7+
- Required Python packages:
  ```
  yt-dlp
  Pillow
  ```

  Note: FFmpeg binaries should be installed in the `assets/FFmpeg` folder. `../assets/FFmpeg/bin` 
  being the final route. The binaries i used are [here](https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-2025-08-25-git-1b62f9d3ae-full_build.7z). (Win x64)

## Installation

1. Clone the repository
   ```
   git clone https://github.com/Lostdou/EasyDownloader.git
   cd EasyDownloader
   ```

2. Create and activate virtual environment (optional but recommended)
   ```
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install required packages
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python app.py
   ```

2. Enter a valid URL from a supported platform
3. Choose between video or audio download (audio only available for YouTube)
4. Wait for the download to complete
5. Files will be saved in the `output` folder
3. Choose between video or audio download (audio only available for YouTube)
4. Wait for the download to complete
5. Files will be saved in the `output` folder

