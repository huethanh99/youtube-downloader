import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
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
        self.app_version = "v1.1.0"
        self.core_version = yt_dlp.version.__version__
        self.title(f"Youtube Downloader {self.app_version} (Lõi / Core yt-dlp {self.core_version})")
        self.geometry("680x520")
        self.minsize(620, 480)
        self.resizable(True, True)
        
        # Set icon
        icon_path = resource_path(os.path.join("devscripts", "logo.ico"))
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
            
        self.batch_current = 1
        self.batch_total = 1
        self.cancel_flag = False
        
        self.create_widgets()
        
    def _select_all_urls(self, event):
        self.url_text.tag_add("sel", "1.0", "end")
        return "break"
        
    def clear_urls(self):
        self.url_text.delete("1.0", "end")
        self.status_var.set("Sẵn sàng (Ready)")
        
    def create_widgets(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # URL Input Header (Label + Clear Button)
        frame_url_header = ttk.Frame(main_frame)
        frame_url_header.pack(pady=(15, 5), padx=20, fill="x")
        
        ttk.Label(
            frame_url_header, 
            text="Đường dẫn Video / Video URLs (dán 1 hoặc nhiều link, mỗi link 1 dòng):"
        ).pack(side="left")
        
        ttk.Button(
            frame_url_header, 
            text="Xóa sạch (Clear)", 
            width=14, 
            command=self.clear_urls
        ).pack(side="right")
        
        # Multi-line URL input with scrollbar
        self.url_text = scrolledtext.ScrolledText(main_frame, height=5, font=("Segoe UI", 9), wrap="char")
        self.url_text.pack(pady=(0, 5), padx=20, fill="x")
        self.url_text.bind("<Control-a>", self._select_all_urls)
        self.url_text.bind("<Control-A>", self._select_all_urls)
        
        # Format Selection
        ttk.Label(main_frame, text="Định dạng và Chất lượng / Format & Quality:").pack(pady=(10, 5), padx=20, anchor="w")
        self.format_var = tk.StringVar(value="video")
        
        frame_formats = ttk.Frame(main_frame)
        frame_formats.pack(pady=5, padx=20, fill="x")
        
        ttk.Radiobutton(frame_formats, text="Video (MP4)", variable=self.format_var, value="video").pack(side="left", padx=5)
        
        self.quality_var = tk.StringVar(value="1080p")
        self.quality_combo = ttk.Combobox(frame_formats, textvariable=self.quality_var, values=["2160p", "1440p", "1080p", "720p", "480p", "360p"], state="readonly", width=8)
        self.quality_combo.pack(side="left", padx=(0, 15))
        
        ttk.Radiobutton(frame_formats, text="Chỉ Âm thanh / Audio only (MP3)", variable=self.format_var, value="audio").pack(side="left", padx=5)
        
        # Destination Folder
        ttk.Label(main_frame, text="Thư mục lưu / Destination:").pack(pady=(10, 5), padx=20, anchor="w")
        
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
            
            # Thông tin thứ tự link nếu tải nhiều link
            batch_prefix = ""
            if self.batch_total > 1:
                batch_prefix = f"[{self.batch_current}/{self.batch_total}] "
                
            # Nếu đang tải playlist, hiển thị thêm thông tin video thứ mấy trong playlist
            playlist_idx = d.get('info_dict', {}).get('playlist_index')
            playlist_count = d.get('info_dict', {}).get('n_entries')
            
            prefix = ""
            if playlist_idx and playlist_count:
                prefix = f"(Video {playlist_idx}/{playlist_count}) "
                
            self.status_var.set(f"{batch_prefix}{prefix}Đang tải (Downloading)... {percent_str}")
            
        elif d['status'] == 'finished':
            batch_prefix = ""
            if self.batch_total > 1:
                batch_prefix = f"[{self.batch_current}/{self.batch_total}] "
            self.status_var.set(f"{batch_prefix}Hoàn tất tải tệp, đang xử lý... (Downloaded, processing...)")
        
    def start_download(self):
        raw_text = self.url_text.get("1.0", "end-1c").strip()
        if not raw_text:
            messagebox.showwarning("Lỗi (Error)", "Vui lòng nhập đường dẫn video! (Please enter video URL!)")
            return
            
        # Tách các đường dẫn (hỗ trợ phân tách bằng dòng mới, dấu cách hoặc phẩy)
        urls = []
        for line in raw_text.splitlines():
            parts = line.replace(",", " ").split()
            for p in parts:
                p = p.strip()
                if p:
                    urls.append(p)
                    
        # Loại bỏ các link trùng lặp mà vẫn giữ nguyên thứ tự
        seen = set()
        unique_urls = []
        for u in urls:
            if u not in seen:
                seen.add(u)
                unique_urls.append(u)
        urls = unique_urls
        
        if not urls:
            messagebox.showwarning("Lỗi (Error)", "Không tìm thấy đường dẫn hợp lệ! (No valid URL found!)")
            return
            
        self.download_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.cancel_flag = False
        self.status_var.set("Đang khởi tạo... (Initializing...)")
        
        # Run in separate thread to not block GUI
        thread = threading.Thread(target=self.download_worker, args=(urls,))
        thread.daemon = True
        thread.start()
        
    def download_worker(self, urls):
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
            
        total_urls = len(urls)
        success_count = 0
        failed_urls = []
        self.batch_total = total_urls
        
        try:
            for idx, url in enumerate(urls, start=1):
                if self.cancel_flag:
                    break
                self.batch_current = idx
                if total_urls > 1:
                    self.status_var.set(f"[{idx}/{total_urls}] Đang kết nối... (Connecting...)")
                else:
                    self.status_var.set("Đang kết nối... (Connecting...)")
                    
                try:
                    with YoutubeDL(ydl_opts) as ydl:
                        retcode = ydl.download([url])
                        if retcode == 0:
                            success_count += 1
                        else:
                            failed_urls.append((url, "Tải không thành công hoặc video không khả dụng"))
                except Exception as e:
                    if self.cancel_flag or "Đã hủy tải xuống" in str(e):
                        raise ValueError("Đã hủy tải xuống (Canceled)")
                    failed_urls.append((url, str(e)))
                    
            if not self.cancel_flag:
                if failed_urls:
                    if success_count > 0:
                        self.status_var.set(f"Hoàn tất {success_count}/{total_urls} link (có link lỗi)")
                        msg = f"Đã tải thành công {success_count}/{total_urls} link.\n\nCó {len(failed_urls)} link gặp lỗi:\n"
                        for u, err in failed_urls:
                            msg += f"• {u}\n"
                        messagebox.showwarning("Hoàn tất có cảnh báo", msg)
                    else:
                        self.status_var.set("Tất cả link đều gặp lỗi! (All failed!)")
                        msg = "Không thể tải các link sau:\n" + "\n".join([f"• {u}" for u, _ in failed_urls])
                        messagebox.showerror("Lỗi tải xuống (Download Error)", msg)
                else:
                    if total_urls > 1:
                        self.status_var.set(f"Tải xuống hoàn tất {success_count}/{total_urls} link!")
                        messagebox.showinfo("Thành công (Success)", f"Đã tải thành công toàn bộ {success_count} link!")
                    else:
                        self.status_var.set("Tải xuống thành công! (Successful!)")
                        messagebox.showinfo("Thành công (Success)", "Đã tải video thành công! (Video downloaded successfully!)")
        except Exception as e:
            if "Đã hủy tải xuống" in str(e) or self.cancel_flag:
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
