import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import sys
import os

# Ensure the yt_dlp package can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from yt_dlp import YoutubeDL
import yt_dlp.version

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class YoutubeDownloaderApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.app_version = "v1.0.1"
        self.core_version = yt_dlp.version.__version__
        self.title(f"Youtube Downloader {self.app_version} (Lõi / Core yt-dlp {self.core_version})")
        self.geometry("650x450")
        self.minsize(600, 400)
        self.resizable(True, True)
        
        # Set icon
        icon_path = resource_path(os.path.join("devscripts", "logo.ico"))
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
            
        self.create_widgets()
        
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # URL Input
        ttk.Label(main_frame, text="Đường dẫn Video / Video URL:").pack(pady=(20, 5), padx=20, anchor="w")
        self.url_var = tk.StringVar()
        self.url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        self.url_entry.pack(pady=5, padx=20, fill="x")
        
        # Format Selection
        ttk.Label(main_frame, text="Định dạng và Chất lượng / Format & Quality:").pack(pady=(15, 5), padx=20, anchor="w")
        self.format_var = tk.StringVar(value="video")
        
        frame_formats = ttk.Frame(main_frame)
        frame_formats.pack(pady=5, padx=20, fill="x")
        
        ttk.Radiobutton(frame_formats, text="Video (MP4)", variable=self.format_var, value="video").pack(side="left", padx=5)
        
        self.quality_var = tk.StringVar(value="1080p")
        self.quality_combo = ttk.Combobox(frame_formats, textvariable=self.quality_var, values=["2160p", "1440p", "1080p", "720p", "480p", "360p"], state="readonly", width=8)
        self.quality_combo.pack(side="left", padx=(0, 15))
        
        ttk.Radiobutton(frame_formats, text="Chỉ Âm thanh / Audio only (MP3)", variable=self.format_var, value="audio").pack(side="left", padx=5)
        
        # Destination Folder
        ttk.Label(main_frame, text="Thư mục lưu / Destination:").pack(pady=(15, 5), padx=20, anchor="w")
        
        frame_dest = ttk.Frame(main_frame)
        frame_dest.pack(pady=5, padx=20, fill="x")
        
        self.dest_var = tk.StringVar(value=os.path.expanduser("~\\Downloads"))
        self.dest_entry = ttk.Entry(frame_dest, textvariable=self.dest_var)
        self.dest_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        ttk.Button(frame_dest, text="Chọn (Browse)", command=self.browse_folder).pack(side="right")
        
        # Playlist Option
        self.playlist_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Tải toàn bộ danh sách / Download Playlist nếu có", variable=self.playlist_var).pack(anchor="w", padx=40, pady=(0, 5))
        
        # Subtitle Option
        self.subtitle_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Tải Phụ đề / Download Subtitles (VI/EN) nếu có", variable=self.subtitle_var).pack(anchor="w", padx=40, pady=(0, 10))
        
        # Status Label
        self.status_var = tk.StringVar(value="Sẵn sàng (Ready)")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="gray")
        self.status_label.pack(pady=(5, 5), padx=20, anchor="w")
        
        # Buttons frame
        frame_buttons = ttk.Frame(main_frame)
        frame_buttons.pack(pady=10)
        
        self.download_btn = ttk.Button(frame_buttons, text="TẢI XUỐNG (DOWNLOAD)", command=self.start_download)
        self.download_btn.pack(side="left", padx=5)
        
        self.cancel_btn = ttk.Button(frame_buttons, text="HỦY (CANCEL)", command=self.cancel_download, state="disabled")
        self.cancel_btn.pack(side="left", padx=5)
        
        self.cancel_flag = False
        
    def cancel_download(self):
        self.cancel_flag = True
        self.cancel_btn.config(state="disabled")
        self.status_var.set("Đang hủy tải xuống... (Canceling...)")
        
    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.dest_var.get())
        if folder:
            self.dest_var.set(folder)
            
    def my_hook(self, d):
        if self.cancel_flag:
            raise ValueError("Đã hủy tải xuống (Canceled)")
            
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0.0%').strip()
            
            # Nếu đang tải playlist, hiển thị thêm thông tin video thứ mấy
            playlist_idx = d.get('info_dict', {}).get('playlist_index')
            playlist_count = d.get('info_dict', {}).get('n_entries')
            
            prefix = ""
            if playlist_idx and playlist_count:
                prefix = f"[{playlist_idx}/{playlist_count}] "
                
            self.status_var.set(f"{prefix}Đang tải (Downloading)... {percent_str}")
            
        elif d['status'] == 'finished':
            self.status_var.set("Hoàn tất tải tệp, đang xử lý... (Downloaded, processing...)")
        
    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Lỗi (Error)", "Vui lòng nhập đường dẫn video! (Please enter video URL!)")
            return
            
        self.download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.cancel_flag = False
        self.status_var.set("Đang khởi tạo... (Initializing...)")
        
        # Run in separate thread to not block GUI
        thread = threading.Thread(target=self.download_worker, args=(url,))
        thread.daemon = True
        thread.start()
        
    def download_worker(self, url):
        fmt = self.format_var.get()
        dest = self.dest_var.get()
        download_playlist = self.playlist_var.get()
        download_subtitle = self.subtitle_var.get()
        quality_str = self.quality_var.get().replace('p', '')
        
        if download_playlist:
            outtmpl_str = '%(playlist_title|.)s/%(playlist_index|)s%(playlist_index&. |)s%(title)s.%(ext)s'
        else:
            outtmpl_str = '%(title)s.%(ext)s'
            
        ydl_opts = {
            'paths': {'home': dest},
            'outtmpl': {'default': outtmpl_str},
            'progress_hooks': [self.my_hook],
            'quiet': True,
            'no_warnings': True,
            'noplaylist': not download_playlist,
            'ignoreerrors': download_playlist,
            'socket_timeout': 30,
            'retries': 10,
            'fragment_retries': 10
        }
        
        import platform
        ffmpeg_dir = resource_path("bin")
        ffmpeg_name = "ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg"
        ffmpeg_exe = os.path.join(ffmpeg_dir, ffmpeg_name)
        if os.path.exists(ffmpeg_exe):
            ydl_opts['ffmpeg_location'] = ffmpeg_exe
        else:
            print(f"DEBUG: FFmpeg không tồn tại tại {ffmpeg_exe}")
        
        if fmt == "audio":
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        else:
            ydl_opts['format'] = f'bestvideo[height<={quality_str}][ext=mp4]+bestaudio[ext=m4a]/best[height<={quality_str}][ext=mp4]/best'
            if download_subtitle:
                ydl_opts['writesubtitles'] = True
                ydl_opts['subtitleslangs'] = ['vi', 'en', 'en-US', 'vi-VN']
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegEmbedSubtitle'
                }]
            
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if not self.cancel_flag:
                self.status_var.set("Tải xuống thành công! (Successful!)")
                messagebox.showinfo("Thành công (Success)", "Đã tải video thành công! (Video downloaded successfully!)")
        except Exception as e:
            if "Đã hủy tải xuống" in str(e):
                self.status_var.set("Đã hủy tải xuống! (Canceled!)")
                messagebox.showinfo("Đã hủy (Canceled)", "Quá trình tải xuống đã bị hủy. (Download canceled.)")
            else:
                self.status_var.set("Đã xảy ra lỗi! (Error!)")
                messagebox.showerror("Lỗi tải xuống (Download Error)", f"Lỗi (Error): {str(e)}")
        finally:
            self.download_btn.config(state="normal")
            self.cancel_btn.config(state="disabled")

if __name__ == "__main__":
    app = YoutubeDownloaderApp()
    app.mainloop()
