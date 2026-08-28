import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os
import shutil
import subprocess

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class InstallerWizard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cài đặt Youtube Downloader")
        self.geometry("500x350")
        self.resizable(False, False)
        
        # Icon
        icon_path = resource_path(os.path.join("devscripts", "logo.ico"))
        if not os.path.exists(icon_path):
            icon_path = resource_path("logo.ico") # Fallback to root for pyinstaller
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)
            
        self.create_widgets()
        
    def create_widgets(self):
        # Header
        header = ttk.Label(self, text="Chào mừng đến với trình cài đặt\nYoutube Downloader", font=("Segoe UI", 16, "bold"), justify="center")
        header.pack(pady=30)
        
        # Dest folder
        ttk.Label(self, text="Thư mục cài đặt:").pack(anchor="w", padx=40)
        
        frame_dest = ttk.Frame(self)
        frame_dest.pack(fill="x", padx=40, pady=5)
        
        default_path = os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Youtube Downloader")
        self.dest_var = tk.StringVar(value=default_path)
        ttk.Entry(frame_dest, textvariable=self.dest_var).pack(side="left", fill="x", expand=True, padx=(0, 10))
        ttk.Button(frame_dest, text="Duyệt...", command=self.browse).pack(side="right")
        
        # Options
        self.shortcut_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(self, text="Tạo biểu tượng ngoài Desktop", variable=self.shortcut_var).pack(anchor="w", padx=40, pady=15)
        
        # Install Button
        self.btn_install = ttk.Button(self, text="CÀI ĐẶT NGAY", command=self.install)
        self.btn_install.pack(pady=30)
        
    def browse(self):
        folder = filedialog.askdirectory(initialdir=self.dest_var.get())
        if folder:
            self.dest_var.set(os.path.join(folder, "Youtube Downloader"))
            
    def install(self):
        dest = self.dest_var.get()
        app_exe_path = resource_path("youtube-downloader.exe")
        
        if not os.path.exists(app_exe_path):
            # For testing outside PyInstaller
            app_exe_path = os.path.join("dist", "youtube-downloader.exe")
            
        if not os.path.exists(app_exe_path):
            messagebox.showerror("Lỗi", "Không tìm thấy file nguồn cài đặt (youtube-downloader.exe)")
            return
            
        self.btn_install.config(text="Đang cài đặt...", state="disabled")
        self.update()
        
        try:
            os.makedirs(dest, exist_ok=True)
            target_exe = os.path.join(dest, "youtube-downloader.exe")
            shutil.copy2(app_exe_path, target_exe)
            
            # Copy icon for shortcut
            icon_path = resource_path("logo.ico")
            if not os.path.exists(icon_path):
                icon_path = resource_path(os.path.join("devscripts", "logo.ico"))
                
            target_icon = os.path.join(dest, "logo.ico")
            if os.path.exists(icon_path):
                shutil.copy2(icon_path, target_icon)
            
            if self.shortcut_var.get():
                self.create_desktop_shortcut(target_exe, target_icon)
                
            messagebox.showinfo("Thành công", "Đã cài đặt Youtube Downloader thành công!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể cài đặt: {str(e)}\n\nVui lòng thử chạy file cài đặt với quyền Administrator (Run as administrator).")
            self.btn_install.config(text="CÀI ĐẶT NGAY", state="normal")
            
    def create_desktop_shortcut(self, target, icon):
        desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
        shortcut_path = os.path.join(desktop, "Youtube Downloader.lnk")
        
        vbs_script = f'''
        Set oWS = WScript.CreateObject("WScript.Shell")
        sLinkFile = "{shortcut_path}"
        Set oLink = oWS.CreateShortcut(sLinkFile)
        oLink.TargetPath = "{target}"
        oLink.WorkingDirectory = "{os.path.dirname(target)}"
        oLink.IconLocation = "{icon}"
        oLink.Save
        '''
        
        vbs_path = os.path.join(os.environ["TEMP"], "create_shortcut.vbs")
        with open(vbs_path, "w", encoding="utf-8") as f:
            f.write(vbs_script)
            
        subprocess.run(["cscript.exe", "//Nologo", vbs_path], creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            os.remove(vbs_path)
        except:
            pass

if __name__ == "__main__":
    app = InstallerWizard()
    app.mainloop()
