import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
from PIL import Image, ImageTk

class DownloaderWindow:
    def __init__(self, master, translator):
        self.translator = translator
        self.master = master
        self.master.title(self.translator.get('window_title'))
        self.master.geometry("500x400")
        self.master.resizable(False, False)
        self.master.iconbitmap("assets/icon.ico")

        # Selector idioma
        self.lang_frame = ttk.Frame(master)
        self.lang_frame.pack(pady=5, padx=10, fill="x")
        ttk.Label(self.lang_frame, text="Language:").pack(side="left")
        self.lang_var = tk.StringVar(value='english')
        self.lang_combo = ttk.Combobox(
            self.lang_frame, 
            values=['english', 'espanol'],
            textvariable=self.lang_var,
            state='readonly',
            width=10
        )
        self.lang_combo.pack(side="left", padx=5)
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)

        # Title Label
        self.title_frame = ttk.Frame(master)
        self.title_frame.pack(pady=10, padx=10, fill="x")
        title_label = ttk.Label(
            self.title_frame, 
            text="EasyDownloader by Lostdou",
            font=('Helvetica', 12, 'bold')
        )
        title_label.pack(anchor="center")
        
        # Input URL 
        self.url_frame = ttk.Frame(master)
        self.url_frame.pack(pady=10, padx=10, fill="x")
        
        ttk.Label(self.url_frame, text=self.translator.get('url_label')).pack(side="left")
        self.url_entry = ttk.Entry(self.url_frame)
        self.url_entry.pack(side="left", expand=True, fill="x", padx=(5, 0))
        
        # Label de plataforma
        self.platform_label = ttk.Label(self.url_frame, text="")
        self.platform_label.pack(side="left", padx=5)
        self.platform_label.pack_forget()  # Inicialmente oculto
        
        # Botones descarga
        self.btn_frame = ttk.Frame(master)
        self.btn_frame.pack(pady=20)
        
        self.video_btn = ttk.Button(
            self.btn_frame, 
            text=self.translator.get('btn_video'),
            command=lambda: self.on_download("video")
        )
        self.video_btn.pack(side="left", padx=5)
        
        self.audio_btn = ttk.Button(
            self.btn_frame,
            text=self.translator.get('btn_audio'),
            command=lambda: self.on_download("audio")
        )
        self.audio_btn.pack(side="left", padx=5)

        # Checkbox consola
        self.console_var = tk.BooleanVar(value=False)
        self.console_check = ttk.Checkbutton(
            master,
            text=self.translator.get('show_console'),
            variable=self.console_var,
            command=self.toggle_console
        )
        self.console_check.pack(pady=5)

        # Output consola
        self.console_frame = ttk.Frame(master)
        self.console = scrolledtext.ScrolledText(
            self.console_frame,
            height=8,
            width=50,
            wrap=tk.WORD
        )
        self.console.pack(pady=5, padx=10, fill="both", expand=True)
        self.console_frame.pack_forget() 

        # Progressbar
        self.progress_frame = ttk.Frame(master)
        self.progress_frame.pack(pady=10, padx=10, fill="x")
        self.progress = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=300
        )
        self.progress_label = ttk.Label(self.progress_frame, text="")
        self.progress_label.pack(pady=2)
        self.progress.pack()
        self.progress_frame.pack_forget()

        # GitHub button
        self.github_frame = ttk.Frame(master)
        self.github_frame.pack(side="bottom", pady=5, padx=10, fill="x")
        
        # Cargar y redimensionar el icono de GitHub
        github_img = Image.open("assets/github.png")
        github_img = github_img.resize((24, 24), Image.Resampling.LANCZOS)
        self.github_icon = ImageTk.PhotoImage(github_img)
        
        self.github_btn = ttk.Button(
            self.github_frame,
            image=self.github_icon,
            command=self.open_github,
            cursor="hand2"
        )
        self.github_btn.pack(side="right")

    def set_download_callback(self, callback):
        self.download_callback = callback

    def on_download(self, mode):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return
            
        self.disable_inputs()
        self.download_callback(url, mode)

    def disable_inputs(self):
        self.url_entry.config(state="disabled")
        self.video_btn.config(state="disabled")
        self.audio_btn.config(state="disabled")

    def enable_inputs(self):
        self.url_entry.config(state="normal")
        self.video_btn.config(state="normal")
        self.audio_btn.config(state="normal")

    def toggle_console(self):
        if self.console_var.get():
            self.console_frame.pack(before=self.btn_frame)
        else:
            self.console_frame.pack_forget()

    def update_progress(self, progress):
        if not self.progress_frame.winfo_ismapped():
            self.progress_frame.pack(before=self.btn_frame)
        self.progress['value'] = progress
        self.progress_label.config(text=f"{progress:.1f}%")

    def add_console_text(self, text):
        if self.console_var.get():
            self.console.insert(tk.END, text + "\n")
            self.console.see(tk.END)

    def reset_progress(self):
        self.progress['value'] = 0
        self.progress_label.config(text="")
        self.progress_frame.pack_forget()
        self.console.delete(1.0, tk.END)

    def on_language_change(self, event=None):
        lang = self.lang_var.get()
        self.translator.set_language(lang)
        self.update_texts()

    def update_texts(self):
        self.master.title(self.translator.get('window_title'))
        self.video_btn.config(text=self.translator.get('btn_video'))
        self.audio_btn.config(text=self.translator.get('btn_audio'))
        self.console_check.config(text=self.translator.get('show_console'))
        
        # Solo actualizar la plataforma si hay una URL
        if hasattr(self, 'current_platform') and self.url_entry.get().strip():
            self.update_platform(self.current_platform)

    def update_platform(self, platform):
        self.current_platform = platform
        url = self.url_entry.get().strip()
        
        if not url:
            self.platform_label.pack_forget()
            return
            
        if platform:
            self.platform_label.config(text=self.translator.get('platform_detected', platform))
        else:
            self.platform_label.config(text=self.translator.get('platform_unknown'))
        
        self.platform_label.pack(side="left", padx=5)

    def show_result(self, success, message):
        self.enable_inputs()
        self.reset_progress()
        if success:
            messagebox.showinfo("Success", self.translator.get('success_download', message))
        else:
            messagebox.showerror("Error", message)

    def open_github(self):
        webbrowser.open("https://github.com/Lostdou/EasyDownloader")
