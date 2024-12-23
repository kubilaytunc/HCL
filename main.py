import tkinter as tk
from PIL import Image, ImageTk  # Pillow kütüphanesi için
from devices import load_device_data
from host import load_host_data
from ui import create_ui
from menu_bar import create_menu

# Dosya yolları
device_file_path = '/root/HW_PROBE/LATEST/hw.info/devices.json'
host_file_path = '/root/HW_PROBE/LATEST/hw.info/host'

# Verileri yükleme
device_data = load_device_data(device_file_path)
host_data = load_host_data(host_file_path)

# Tkinter uygulaması
root = tk.Tk()
root.title("Donanım Bilgileri")

# Pencere ikonunu ayarlama
try:
    icon = ImageTk.PhotoImage(file="assets/pardus.png")
    root.iconphoto(True, icon)
except Exception as e:
    print(f"İkon yüklenirken hata oluştu: {e}")

# Menü çubuğunu oluşturma
menubar = create_menu(root)

# Arayüzü oluşturma
create_ui(root, device_data, host_data)

# Uygulamayı başlatma
root.mainloop()

