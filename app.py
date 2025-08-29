from kivy.app import App
from kivy.core.window import Window
from downloader import VideoDownloader
from translations import Translator
from gui import DownloaderScreen
import os

class EasyDownloaderApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.translator = Translator('english')
        self.downloader = VideoDownloader(self.translator)

    def build(self):
        self.icon = 'assets/icon.ico'
        Window.size = (400, 600)
        screen = DownloaderScreen(self.translator)
        self.downloader.set_callbacks(
            screen.update_progress,
            None  # Removemos el callback de la consola
        )
        screen.set_download_callback(self.handle_download)
        return screen

    def handle_download(self, url, mode):
        from kivy.clock import mainthread

        @mainthread
        def update_ui(progress):
            self.root.update_progress(progress)

        @mainthread
        def download_complete(success, message):
            self.root.show_result(success, message)

        def download():
            try:
                self.downloader.set_callbacks(update_ui, None)
                success, message = (
                    self.downloader.download_video(url)
                    if mode == "video"
                    else self.downloader.download_audio(url)
                )
                download_complete(success, message)
            except Exception as e:
                download_complete(False, str(e))

        from threading import Thread
        Thread(target=download, daemon=True).start()

if __name__ == "__main__":
    EasyDownloaderApp().run()

