TRANSLATIONS = {
    'english': {
        'window_title': 'Easy Downloader',
        'url_label': 'URL:',
        'btn_video': 'Download Video',
        'btn_audio': 'Download Audio',
        'show_console': 'Show Console Output',
        'platform_unknown': 'Platform: Unknown',
        'platform_detected': 'Platform: {}',
        'error_no_url': 'Please enter a URL',
        'error_unsupported': 'Unsupported platform or invalid URL',
        'error_audio_only_yt': 'Audio download is only supported for YouTube',
        'success_download': 'Downloaded: {}',
    },
    'espanol': {
        'window_title': 'Easy Downloader',
        'url_label': 'URL:',
        'btn_video': 'Descargar Video',
        'btn_audio': 'Descargar Audio',
        'show_console': 'Mostrar Consola',
        'platform_unknown': 'Plataforma: Desconocida',
        'platform_detected': 'Plataforma: {}',
        'error_no_url': 'Por favor, ingrese una URL',
        'error_unsupported': 'Plataforma no soportada o URL inválida',
        'error_audio_only_yt': 'La descarga de audio solo está disponible para YouTube',
        'success_download': 'Descargado: {}',
    }
}

LANGUAGE_CODES = {
    'english': 'en',
    'espanol': 'es'
}

class Translator:
    def __init__(self, language='english'):
        self.language = language

    def set_language(self, language):
        if language in TRANSLATIONS:
            self.language = language

    def get(self, key, *args):
        translation = TRANSLATIONS[self.language].get(key, key)
        if args:
            return translation.format(*args)
        return translation
