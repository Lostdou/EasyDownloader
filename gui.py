from kivy.uix.widget import Widget  # Cambiar esta línea
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.core.clipboard import Clipboard
from kivy.clock import Clock, mainthread
from kivy.uix.modalview import ModalView
from kivy.metrics import dp
from kivy.uix.image import Image  # Añadir este import al principio
import webbrowser
import os
import re

class InfoModal(ModalView):
    def __init__(self, translator, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.6)
        self.setup_content(translator)

    def setup_content(self, translator):
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # App icon
        icon = Image(
            source='assets/icon.jpeg',
            size_hint=(None, None),
            size=(dp(100), dp(100)),
            pos_hint={'center_x': 0.5}
        )
        layout.add_widget(icon)
        
        # App info
        layout.add_widget(Label(
            text=translator.get('app_name'),
            font_size='24sp',
            size_hint_y=None,
            height=dp(40)
        ))
        
        info_text = f"""{translator.get('developer')}: Lostdou
{translator.get('app_version', '1.2.0')}"""
        
        layout.add_widget(Label(
            text=info_text,
            size_hint_y=None,
            height=dp(60)
        ))
        
        # Links
        for text, url in [
            (translator.get('personal_site'), 'https://lostdou.dev.ar'),
            (translator.get('repo_link'), 'https://github.com/Lostdou/EasyDownloader')
        ]:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=dp(40)
            )
            btn.url = url
            btn.bind(on_press=lambda btn: webbrowser.open(btn.url))
            layout.add_widget(btn)
        
        # Close button
        close_btn = Button(
            text=translator.get('close'),
            size_hint_y=None,
            height=dp(40)
        )
        close_btn.bind(on_press=self.dismiss)
        layout.add_widget(close_btn)
        
        self.add_widget(layout)

class DownloaderScreen(Screen):
    def __init__(self, translator, **kwargs):
        super().__init__(**kwargs)
        self.translator = translator
        self.current_platform = None
        self.setup_ui()

    def setup_ui(self):
        main_layout = BoxLayout(orientation='vertical')
        
        # Language selector (top)
        lang_layout = BoxLayout(size_hint_y=None, height=dp(40), padding=dp(10))
        lang_layout.add_widget(Label(text='Language:', size_hint_x=0.3))
        self.lang_spinner = Spinner(
            text='english',
            values=('english', 'espanol'),
            size_hint_x=0.7
        )
        self.lang_spinner.bind(text=self.on_language_change)
        lang_layout.add_widget(self.lang_spinner)
        main_layout.add_widget(lang_layout)
        
        # Central content con espaciadores flexibles
        content_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        
        # Espaciador superior con peso flexible
        content_layout.add_widget(Widget(size_hint_y=1))
        
        # Main content (centered)
        central_layout = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        central_layout.bind(minimum_height=central_layout.setter('height'))
        
        # Title and main controls
        central_layout.add_widget(Label(
            text='EasyDownloader',
            font_size='20sp',
            size_hint_y=None,
            height=dp(50)
        ))
        
        # URL input
        self.url_input = TextInput(
            multiline=False,
            hint_text='Enter URL here',
            size_hint_y=None,
            height=40
        )
        self.url_input.bind(text=self.on_url_change)
        central_layout.add_widget(self.url_input)

        # Platform label
        self.platform_label = Label(
            size_hint_y=None,
            height=30
        )
        central_layout.add_widget(self.platform_label)

        # Download buttons
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        self.video_btn = Button(
            text=self.translator.get('btn_video'),
            size_hint_y=None,
            height=40
        )
        self.video_btn.bind(on_release=lambda x: self.on_download("video"))
        
        self.audio_btn = Button(
            text=self.translator.get('btn_audio'),
            size_hint_y=None,
            height=40
        )
        self.audio_btn.bind(on_release=lambda x: self.on_download("audio"))
        
        btn_layout.add_widget(self.video_btn)
        btn_layout.add_widget(self.audio_btn)
        central_layout.add_widget(btn_layout)

        # Progress bar
        self.progress_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=50)
        self.progress_bar = ProgressBar(max=100)
        self.progress_label = Label(text="0%")
        self.progress_layout.add_widget(self.progress_bar)
        self.progress_layout.add_widget(self.progress_label)
        central_layout.add_widget(self.progress_layout)
        self.progress_layout.opacity = 0

        content_layout.add_widget(central_layout)
        
        # Espaciador inferior con peso flexible
        content_layout.add_widget(Widget(size_hint_y=1))
        
        main_layout.add_widget(content_layout)
        
        # Bottom buttons
        bottom_layout = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10), padding=dp(10))
        self.folder_btn = Button(text="Files installed >>")
        self.info_btn = Button(
            text=self.translator.get('more_info'),
            on_press=self.show_info_modal
        )
        bottom_layout.add_widget(self.folder_btn)
        bottom_layout.add_widget(self.info_btn)
        main_layout.add_widget(bottom_layout)
        
        self.add_widget(main_layout)

    def set_download_callback(self, callback):
        self.download_callback = callback

    def on_url_change(self, instance, value):
        if hasattr(self, '_check_url_event'):
            self._check_url_event.cancel()
        self._check_url_event = Clock.schedule_once(lambda dt: self.check_url(value), 1)

    def check_url(self, url):
        if url.strip():
            platform = None
            patterns = {
                'youtube': r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)',
                'twitter': r'(?:https?:\/\/)?(?:www\.)?(?:twitter\.com|x\.com)',
                'instagram': r'(?:https?:\/\/)?(?:www\.)?(?:instagram\.com)',
                'tiktok': r'(?:https?:\/\/)?(?:www\.)?(?:tiktok\.com)'
            }
            
            for p, pattern in patterns.items():
                if re.match(pattern, url):
                    platform = p
                    break

            self.update_platform(platform)
            self.audio_btn.disabled = platform != "youtube"
        else:
            self.update_platform(None)

    def update_platform(self, platform):
        self.current_platform = platform
        if platform:
            self.platform_label.text = self.translator.get('platform_detected', platform)
        else:
            self.platform_label.text = self.translator.get('platform_unknown')

    def on_download(self, mode):
        url = self.url_input.text.strip()
        if not url:
            from kivy.uix.popup import Popup
            from kivy.uix.label import Label
            popup = Popup(
                title='Error',
                content=Label(text=self.translator.get('error_no_url')),
                size_hint=(None, None),
                size=(300, 150)
            )
            popup.open()
            return
        
        self.disable_inputs()
        self.download_callback(url, mode)

    def disable_inputs(self):
        self.url_input.disabled = True
        self.video_btn.disabled = True
        self.audio_btn.disabled = True

    def enable_inputs(self):
        self.url_input.disabled = False
        self.video_btn.disabled = False
        self.check_url(self.url_input.text)

    @mainthread
    def update_progress(self, progress):
        self.progress_layout.opacity = 1
        self.progress_bar.value = progress
        self.progress_label.text = f"{progress:.1f}%"

    @mainthread
    def show_result(self, success, message):
        self.enable_inputs()
        self.progress_layout.opacity = 0
        self.progress_bar.value = 0
        self.progress_label.text = "0%"
        
        from kivy.uix.popup import Popup
        from kivy.uix.button import Button
        
        content = BoxLayout(orientation='vertical')
        content.add_widget(Label(text=message))
        if success:
            btn = Button(text='Open Folder', size_hint_y=None, height=40)
            btn.bind(on_press=lambda x: self.open_output_folder())
            content.add_widget(btn)
        
        Popup(title='Success' if success else 'Error',
              content=content,
              size_hint=(None, None), size=(300, 200)).open()

    def update_texts(self):
        self.video_btn.text = self.translator.get('btn_video')
        self.audio_btn.text = self.translator.get('btn_audio')
        self.folder_btn.text = "Downloads >>" if self.lang_spinner.text == 'english' else "Descargas >>"
        self.info_btn.text = self.translator.get('more_info')
        
        if self.current_platform:
            self.update_platform(self.current_platform)

    def show_info_modal(self, instance):
        modal = InfoModal(self.translator)
        modal.open()

    def open_github(self, *args):
        webbrowser.open("https://github.com/Lostdou/EasyDownloader")

    def open_output_folder(self, *args):
        folder_path = os.path.abspath("output")
        os.startfile(folder_path) if os.name == 'nt' else os.system(f'xdg-open "{folder_path}"')
        self.enable_inputs()
        self.progress_layout.opacity = 0
        self.progress_bar.value = 0
        self.progress_label.text = "0%"

    def on_language_change(self, instance, value):
        self.translator.set_language(value)
        self.update_texts()

    def update_texts(self):
        self.video_btn.text = self.translator.get('btn_video')
        self.audio_btn.text = self.translator.get('btn_audio')
        self.folder_btn.text = "Downloads >>" if self.lang_spinner.text == 'english' else "Descargas >>"
        self.info_btn.text = self.translator.get('more_info')
        
        if self.current_platform:
            self.update_platform(self.current_platform)

    def show_info_modal(self, instance):
        modal = InfoModal(self.translator)
        modal.open()

    def open_output_folder(self, *args):
        folder_path = os.path.abspath("output")
        os.startfile(folder_path) if os.name == 'nt' else os.system(f'xdg-open "{folder_path}"')
        self.enable_inputs()
        self.progress_layout.opacity = 0
        self.progress_bar.value = 0
        self.progress_label.text = "0%"
    def open_github(self, *args):
        webbrowser.open("https://github.com/Lostdou/EasyDownloader")

    def open_output_folder(self, *args):
        folder_path = os.path.abspath("output")
        os.startfile(folder_path) if os.name == 'nt' else os.system(f'xdg-open "{folder_path}"')
