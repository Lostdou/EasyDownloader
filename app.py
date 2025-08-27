import tkinter as tk
import threading
from window import DownloaderWindow
from downloader import VideoDownloader
from translations import Translator

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.translator = Translator('english')  # Changed from 'en' to 'english'
        self.window = DownloaderWindow(self.root, self.translator)
        self.downloader = VideoDownloader(self.translator)
        self.window.set_download_callback(self.handle_download)
        self.downloader.set_callbacks(
            self.window.update_progress,
            self.window.add_console_text
        )
        self.url_check_after = None
        self.window.url_entry.bind('<KeyRelease>', self.on_url_change)

    def on_url_change(self, event=None):
        if self.url_check_after:
            self.root.after_cancel(self.url_check_after)
        
        self.url_check_after = self.root.after(1000, self.check_url)

    def check_url(self):
        url = self.window.url_entry.get().strip()
        if url:
            platform = self.downloader.validate_url(url)
            self.window.update_platform(platform)
            self.window.audio_btn.config(state="normal" if platform == "youtube" else "disabled")
        else:
            self.window.update_platform(None)

    def handle_download(self, url, mode):
        def download_thread():
            success, message = (
                self.downloader.download_video(url)
                if mode == "video"
                else self.downloader.download_audio(url)
            )
            self.root.after(0, lambda: self.window.show_result(success, message))

        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = App()
    app.run()
