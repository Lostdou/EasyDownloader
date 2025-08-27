import yt_dlp
import re

class VideoDownloader:
    def __init__(self, translator):
        self.translator = translator
        self.base_opts = {
            "noplaylist": True,
            "outtmpl": "output/%(title)s.%(ext)s",
            "ffmpeg_location": r"C:\FFmpeg\bin",
        }
        self.progress_callback = None
        self.console_callback = None

    def set_callbacks(self, progress_callback, console_callback):
        self.progress_callback = progress_callback
        self.console_callback = console_callback

    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            if 'total_bytes' in d:
                progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
            elif 'total_bytes_estimate' in d:
                progress = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
            else:
                progress = 0
            
            if self.progress_callback:
                self.progress_callback(progress)
            
            if self.console_callback:
                self.console_callback(f"Downloading... {progress:.1f}%")

    def validate_url(self, url):
        patterns = {
            'youtube': r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)',
            'twitter': r'(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)',
            'instagram': r'(?:https?:\/\/)?(?:www\.)?(?:instagram\.com)'
        }
        
        for platform, pattern in patterns.items():
            if re.match(pattern, url):
                return platform
        return None

    def _get_platform_opts(self, platform):
        if platform == 'twitter':
            return {
                'format': 'best',
                'merge_output_format': 'mp4',
            }
        elif platform == 'instagram':
            return {
                'format': 'best',
                'merge_output_format': 'mp4',
            }
        # YouTube usa las opciones por defecto
        return {}

    def download_video(self, url):
        platform = self.validate_url(url)
        if not platform:
            return False, self.translator.get('error_unsupported')

        opts = self.base_opts.copy()
        platform_opts = self._get_platform_opts(platform)
        opts.update(platform_opts)
        
        if platform in ['youtube']:
            opts.update({
                "format": "bestvideo+bestaudio",
                "merge_output_format": "mp4",
                "postprocessor_args": [
                    "-c:v", "copy",
                    "-c:a", "aac",
                    "-b:a", "192k"
                ],
            })
        
        if self.console_callback:
            self.console_callback(f"Detected platform: {platform}")
        
        return self._perform_download(url, opts)

    def download_audio(self, url):
        platform = self.validate_url(url)
        if not platform:
            return False, self.translator.get('error_unsupported')
            
        if platform not in ['youtube']:
            return False, self.translator.get('error_audio_only_yt')

        opts = self.base_opts.copy()
        opts.update({
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }]
        })
        
        return self._perform_download(url, opts)

    def _perform_download(self, url, opts):
        try:
            opts['progress_hooks'] = [self._progress_hook]
            if self.console_callback:
                opts['logger'] = Logger(self.console_callback)
                
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                return True, f"Downloaded: {info['title']}.{info['ext']}"
        except Exception as e:
            return False, str(e)

class Logger:
    def __init__(self, callback):
        self.callback = callback

    def debug(self, msg):
        if msg.startswith('[download]'):
            self.callback(msg)

    def warning(self, msg):
        self.callback(f"WARNING: {msg}")

    def error(self, msg):
        self.callback(f"ERROR: {msg}")
