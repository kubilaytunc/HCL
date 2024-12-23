import tkinter as tk
from PIL import Image, ImageTk  # Pillow kütüphanesi için
from devices import load_device_data
from host import load_host_data
from ui import create_ui
from menu_bar import create_menu
from hw_probe import getProbe

import constants
import os

#device_file_path = '/root/HW_PROBE/LATEST/hw.info/devices.json'
#host_file_path = '/root/HW_PROBE/LATEST/hw.info/host'

try:
    if os.path.exists(constants.DEVICE_FILE_PATH):
        print("Sistem verisi mevcut. Devam edin yada güncellemek için tıklayın (ui'da düzenlenecek)")
    else:
        if os.path.exists("/bin/hw-probe"):
            getProbe()
        else:
            print("HW PROBE yüklü değil. (ui'da gerek yok ?)")
except Exception as e:
    print(f"Probe yüklenirken hata oluştu: {e}")


# Verileri yükleme
device_data = load_device_data(constants.DEVICE_FILE_PATH)
host_data = load_host_data(constants.HOST_FILE_PATH)

# Tkinter uygulaması
root = tk.Tk()
root.title("Donanım Bilgileri")
root.minsize(800, 600)

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

