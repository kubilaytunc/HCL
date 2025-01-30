import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from devices import load_device_data
from host import load_host_data
import constants
import os
from landing import LandingPage  # landing.py'den LandingPage sınıfını içe aktar
from hw_probe import getProbe

# Probe kontrolü ve veri yükleme

# PyQt5 uygulaması
app = QApplication(sys.argv)
app.setWindowIcon(QIcon("assets/pardus.png"))  # Pencere ikonu

# LandingPage'i oluşturma
window = LandingPage()  # LandingPage sınıfını başlat
window.show()

# Uygulamayı başlatma
sys.exit(app.exec_())

"""
if os.path.exists(constants.DEVICE_FILE_PATH):
    print("Sistem verisi mevcut.")
else:
    if os.path.exists("/bin/hw-probe"):
        print("hw-probe var. Veriyi almak için çalıştırıyorum...")
        try:
            getProbe()  # Buradaki getProbe fonksiyonu bir hata oluşturabilir
        except Exception as e:
            print(f"Probe verisi alınırken hata oluştu: {e}")
    else:
        print("HW PROBE yüklü değil.")

# Verileri yükleme

#device_data = load_device_data(constants.DEVICE_FILE_PATH)
#host_data = load_host_data(constants.HOST_FILE_PATH)"""