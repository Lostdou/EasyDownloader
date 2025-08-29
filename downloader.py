import yt_dlp
import re

class VideoDownloader:
    def __init__(self, translator):
        self.translator = translator
        self.base_opts = {
            "noplaylist": True,
            "outtmpl": "output/%(title)s.%(ext)s",
            "ffmpeg_location": r"assets\FFmpeg\bin",
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
            'instagram': r'(?:https?:\/\/)?(?:www\.)?(?:instagram\.com)',
            'tiktok': r'(?:https?:\/\/)?(?:www\.)?(?:tiktok\.com)'
        }
        
        for platform, pattern in patterns.items():
            if re.match(pattern, url):
                return platform
        return None

    def _get_platform_opts(self, platform):
        base_video_opts = {
            'format': 'best',
            'merge_output_format': 'mp4',
            'postprocessor_args': [
                '-c:v', 'libx264',  
                '-preset', 'medium',
                '-c:a', 'aac', 
                '-b:a', '192k', 
                '-movflags', '+faststart'
            ],
        }

        if platform == 'twitter':
            return base_video_opts
        elif platform == 'instagram':
            return base_video_opts
        elif platform == 'tiktok':
            opts = base_video_opts.copy()
            opts.update({
                'legacy_server_connect': True,
                'extractor_args': {
                    'tiktok': {
                        'download_timeout': 60,
                        'encoding': 'utf-8'
                    }
                },
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Upgrade-Insecure-Requests': '1'
                }
            })
            return opts
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
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-c:a', 'aac',
                    '-b:a', '192k',
                    '-movflags', '+faststart'
                ],
            })
        
        if platform == 'tiktok':
            url = url.split('?')[0]
            if not url.startswith('http'):
                url = 'https://' + url
        
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
