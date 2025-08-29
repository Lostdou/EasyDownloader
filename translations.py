TRANSLATIONS = {
    'english': {
        'window_title': 'Easy Downloader',
        'url_label': 'URL:',
        'btn_video': 'Download Video',
        'btn_audio': 'Download Audio',
        'platform_unknown': 'Platform: Unknown',
        'platform_detected': 'Platform: {}',
        'error_no_url': 'Please enter a URL',
        'error_unsupported': 'Unsupported platform or invalid URL',
        'error_audio_only_yt': 'Audio download is only supported for YouTube',
        'success_download': 'Downloaded: {}',
        'paste_url': 'Paste URL',
        'cancel': 'Cancel',
        'open_folder': 'Open Folder',
        'more_info': 'More Information',
        'app_name': 'Easy Downloader',
        'developer': 'Developer',
        'app_version': 'Version: {}',
        'personal_site': 'Personal Website',
        'repo_link': 'GitHub Repository',
        'close': 'Close'
    },
    'espanol': {
        'window_title': 'Easy Downloader',
        'url_label': 'URL:',
        'btn_video': 'Descargar Video',
        'btn_audio': 'Descargar Audio',
        'platform_unknown': 'Plataforma: Desconocida',
        'platform_detected': 'Plataforma: {}',
        'error_no_url': 'Por favor, ingrese una URL',
        'error_unsupported': 'Plataforma no soportada o URL inválida',
        'error_audio_only_yt': 'La descarga de audio solo está disponible para YouTube',
        'success_download': 'Descargado: {}',
        'paste_url': 'Pegar URL',
        'cancel': 'Cancelar',
        'open_folder': 'Abrir Carpeta',
        'more_info': 'Más Información',
        'app_name': 'Easy Downloader',
        'developer': 'Desarrollador',
        'app_version': 'Versión: {}',
        'personal_site': 'Sitio Personal',
        'repo_link': 'Repositorio GitHub',
        'close': 'Cerrar'
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
