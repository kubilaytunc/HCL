import tkinter as tk
from tkinter import messagebox
from pardus_packages import PardusPackagesWindow
from tkinter import ttk
import hw_probe

class MenuFunctions:
    def __init__(self, root):
        self.root = root

    def pardus_paketler(self):
        # Pardus paketler penceresini aç
        PardusPackagesWindow(self.root)

    def firmware_bilgisi(self):
        # Firmware bilgilerini gösteren pencere veya işlevsellik
        messagebox.showinfo("Firmware", "Firmware bilgileri burada gösterilecek")

    def sistem_ayrintilari(self):
        # Sistem ayrıntılarını gösteren pencere veya işlevsellik
        messagebox.showinfo("Sistem Ayrıntıları", "Sistem ayrıntıları burada gösterilecek")

    def hakkinda(self):
        # Hakkında bilgilerini gösteren pencere
        about_window = tk.Toplevel(self.root)
        about_window.title("Hakkında")
        about_window.geometry("300x200")
        
        label = tk.Label(about_window, text="Donanım Bilgileri Uygulaması\nSürüm 1.0\n\nGeliştiriciler:\nKubilay TUNÇ\nAli Rıza GİRİŞEN\n\n© 2024")
        label.pack(pady=20)

    def icindekiler(self):
        # İçindekiler/Yardım bilgilerini gösteren pencere
        help_window = tk.Toplevel(self.root)
        help_window.title("İçindekiler")
        help_window.geometry("400x300")
        
        label = tk.Label(help_window, text="Uygulama Kullanım Kılavuzu\n\n" +
                        "1. Sistem Menüsü\n" +
                        "   - Pardus Paketler\n" +
                        "   - Firmware\n" +
                        "   - Ayrıntılar\n\n" +
                        "2. Yardım Menüsü\n" +
                        "   - Hakkında\n" +
                        "   - İçindekiler")
        label.pack(pady=20)
    
    def hardware_update(self):
        # Soruyu açıkça belirtmek için title ve message ekle
        response = messagebox.askquestion(
            title="Donanım Güncellemesi", 
            message="Donanım listeniz mevcut. Listeyi güncellemek ister misiniz?"
        )

        if response == 'yes':
            self.perform_update()


    def perform_update(self):
        # Yükleme penceresi oluştur
        loading_window = tk.Toplevel(self.root)
        loading_window.title("Yükleniyor")
        loading_window.geometry("300x100")
        loading_window.resizable(False, False)

        # Etiket
        label = tk.Label(loading_window, text="Güncelleme yapılıyor, lütfen bekleyin...", font=("Arial", 10))
        label.pack(pady=10)

        # İlerleme çubuğu
        progress = ttk.Progressbar(loading_window, mode="indeterminate")
        progress.pack(pady=10, padx=20, fill=tk.X)
        progress.start(1)  # Animasyonu başlat

        # Modal yap
        loading_window.transient(self.root)
        loading_window.grab_set()

        self.root.update_idletasks()

        try:
            hw_probe.getProbe()
            loading_window.destroy()
            messagebox.showinfo("Güncelleme", "Güncelleme tamamlandı.")
        except Exception as e:
            loading_window.destroy()
            messagebox.showerror("Hata", f"Güncelleme sırasında bir hata oluştu: {e}")




#    def perform_update(self):
#        
#        messagebox.showinfo("Güncelleme", "Donanım güncelleniyor...")
#
#        # Call the getProbe() function from hq_probe.py
#        try:
#            hw_probe.getProbe()
#        except Exception as e:
#            messagebox.showerror("Hata", f"Donanım güncelleme işlemi sırasında hata oluştu: {e}")

def create_menu(root):
    menu_functions = MenuFunctions(root)
    
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Sistem menüsü
    sistem_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Sistem", menu=sistem_menu)
    sistem_menu.add_command(label="Donanım Listesi Kontrol", command=menu_functions.hardware_update)
    sistem_menu.add_command(label="Pardus Paketler", command=menu_functions.pardus_paketler)
    sistem_menu.add_command(label="Firmware", command=menu_functions.firmware_bilgisi)
    sistem_menu.add_command(label="Ayrıntılar", command=menu_functions.sistem_ayrintilari)
    sistem_menu.add_command(label="Çıkış", command=root.quit)

    # Yardım menüsü
    yardim_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Yardım", menu=yardim_menu)
    yardim_menu.add_command(label="Hakkında", command=menu_functions.hakkinda)
    yardim_menu.add_command(label="İçindekiler", command=menu_functions.icindekiler)

    return menubar 