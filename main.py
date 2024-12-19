import tkinter as tk
from devices import load_device_data
from host import load_host_data
from ui import create_ui

# Dosya yolları
device_file_path = '/root/HW_PROBE/LATEST/hw.info/devices.json'
host_file_path = '/root/HW_PROBE/LATEST/hw.info/host'

# Verileri yükleme
device_data = load_device_data(device_file_path)
host_data = load_host_data(host_file_path)

# Tkinter uygulaması
root = tk.Tk()
root.title("Donanım Bilgileri")

# Arayüzü oluşturma
create_ui(root, device_data, host_data)

# Uygulamayı başlatma
root.mainloop()
