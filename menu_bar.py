import tkinter as tk
from tkinter import messagebox
from pardus_packages import PardusPackagesWindow

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

def create_menu(root):
    menu_functions = MenuFunctions(root)
    
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # Sistem menüsü
    sistem_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Sistem", menu=sistem_menu)
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