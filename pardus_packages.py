import tkinter as tk
from tkinter import ttk, messagebox

class PardusPackagesWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Pardus Paketler")
        
        # Pencereyi ortalama
        window_width = 400
        window_height = 500
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.window.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        
        # Ana container frame
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Butonlar
        ttk.Button(main_frame, text="Güncellenebilirlik", command=self.check_updates).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="Backports Depolar", command=self.backports_repos).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="Debian Firmware Paketleri", command=self.debian_firmware).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="Kernel Seçenekleri", command=self.kernel_options).pack(fill=tk.X, pady=5)
        ttk.Button(main_frame, text="Çıkış", command=self.window.destroy).pack(fill=tk.X, pady=20)

    def check_updates(self):
        # Güncellenebilir paketleri kontrol et
        messagebox.showinfo("Güncellemeler", 
                          "Sistem güncellemeleri kontrol ediliyor...\n"
                          "Bu özellik henüz geliştirme aşamasındadır.")

    def backports_repos(self):
        # Backports depolarını göster/yönet
        messagebox.showinfo("Backports Depolar", 
                          "Backports depo yönetimi...\n"
                          "Bu özellik henüz geliştirme aşamasındadır.")

    def debian_firmware(self):
        # Debian firmware paketlerini listele
        messagebox.showinfo("Debian Firmware", 
                          "Debian firmware paketleri listeleniyor...\n"
                          "Bu özellik henüz geliştirme aşamasındadır.")

    def kernel_options(self):
        # Kernel seçeneklerini göster
        messagebox.showinfo("Kernel Seçenekleri", 
                          "Kernel seçenekleri görüntüleniyor...\n"
                          "Bu özellik henüz geliştirme aşamasındadır.") 