from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt
import sys, os
from ui import create_ui  # ui.py'den create_ui fonksiyonunu içe aktar
from devices import load_device_data
from host import load_host_data
import constants
from hw_probe import getProbe
from pardus_packages import PardusPackagesWindow
from pardus_kernel import KernelApp


class LandingPage(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pardus Donanım Kontrol")
        self.setGeometry(100, 100, 800, 600)  # Pencere boyutunu artırdık
        
        # Ana widget ve layout
        central_widget = QWidget()
        central_widget.setStyleSheet("background-color: #F5F5F5;")  # Ana pencerenin arka plan rengi
        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)  # Butonlar arasındaki boşluğu artır

        # Butonlar
        buttons = [
            ("Donanım Listesi Kontrol", self.open_device_check),
            ("Pardus Paketler", self.open_pardus_packages),
            ("Çekirdek ve Backports Depolar", self.open_backports),
            ("Ayrıntılar", self.show_details),
            ("Çıkış", self.close)
        ]
        
        for text, function in buttons:
            button = QPushButton(text)
            button.setFixedSize(300, 60)  # Buton boyutlarını artırdık
            button.setStyleSheet("""
                QPushButton {
                    background-color: #FFFFFF;  /* Beyaz arka plan */
                    color: #333;               /* Koyu gri yazı rengi */
                    font-size: 16px;
                    border-radius: 10px;
                    padding: 10px;
                    border: 1px solid #CCCCCC; /* Kenarlık ekledik */
                }
                QPushButton:hover {
                    background-color: #E0E0E0; /* Hover rengi */
                }
            """)
            button.clicked.connect(function)
            layout.addWidget(button, alignment=Qt.AlignCenter)
        
        # Pardus logosu
        try:
            pardus_logo = QLabel()
            pixmap = QPixmap("assets/pardus.png")
            pardus_logo.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
            pardus_logo.setAlignment(Qt.AlignCenter)
            layout.addWidget(pardus_logo)
        except Exception as e:
            print(f"Pardus logosu yüklenemedi: {e}")
        
        # Başlık etiketi
        title_label = QLabel("Pardus Donanım Kontrol")
        title_label.setFont(QFont("Arial", 24, QFont.Bold))
        title_label.setStyleSheet("color: #333;")
        layout.insertWidget(0, title_label, alignment=Qt.AlignCenter)
        
        # Footer
        footer_widget = QWidget()
        footer_widget.setStyleSheet("""
            QWidget {
                border-top: 1px solid #CCCCCC;  /* İnce ve kesintisiz gri çizgi */
                margin: 17px;  /* Margin'i sıfırla */
            }
            QLabel {
                color: #666;  /* Gri yazı rengi */
                font-size: 14px;
            }
        """)
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(footer_widget)
        footer_label = QLabel("TÜBİTAK BİLGEM-YTE 2024")
        layout.insertWidget(149, footer_label, alignment=Qt.AlignCenter)
        
        self.setCentralWidget(central_widget)

    def open_device_check(self):
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
        device_data = load_device_data(constants.DEVICE_FILE_PATH)
        host_data = load_host_data(constants.HOST_FILE_PATH)
        
        # UI'yi oluştur ve göster
        self.device_check_window = create_ui(device_data, host_data)  # create_ui fonksiyonunu çağır
        self.device_check_window.show()
        #self.close()  # LandingPage'i kapat
        
    def open_pardus_packages(self):
        print("Pardus Paketler açılıyor...")
        self.packages_window = PardusPackagesWindow()  # Yeni pencere aç
        self.packages_window.show()
    
    def open_backports(self):
        self.kernel_test_window = KernelApp()  # Yeni pencere aç
        self.kernel_test_window.show()
        print("Kernel backports açılıyor...")

    
    def show_details(self):
        QMessageBox.information(self, "Ayrıntılar", "\nSürüm 1.0\n\nGeliştiriciler:\nKubilay TUNÇ\nAli Rıza GİRİŞEN\n\n© 2024")


# PyQt5 uygulaması
app = QApplication(sys.argv)
app.setWindowIcon(QIcon("assets/pardus.png"))  # Pencere ikonu

# Uygulamayı başlatma
window = LandingPage()
window.show()

sys.exit(app.exec_())