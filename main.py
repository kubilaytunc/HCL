import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from devices import load_device_data
from host import load_host_data
from ui import create_ui
from hw_probe import getProbe
import constants
import os

# Probe kontrolü ve veri yükleme
try:
    if os.path.exists(constants.DEVICE_FILE_PATH):
        print("Sistem verisi mevcut. Devam edin ya da güncellemek için tıklayın (ui'da düzenlenecek)")
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

# PyQt5 uygulaması
app = QApplication(sys.argv)
app.setWindowIcon(QIcon("assets/pardus.png"))  # Pencere ikonu

# Arayüzü oluşturma
window = create_ui(device_data, host_data)
window.show()

# Uygulamayı başlatma
sys.exit(app.exec_())