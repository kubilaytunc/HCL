from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QMessageBox, QProgressDialog, QLabel, QVBoxLayout, QWidget
)
from PyQt5.QtCore import Qt, QTimer
from pardus_packages import PardusPackagesWindow  # Bu modülü PyQt5'e uyarlamanız gerekecek
import hw_probe
import sys

class MenuFunctions:
    def __init__(self, main_window):
        self.main_window = main_window

    def pardus_paketler(self):
        # Pardus paketler penceresini aç
        self.pardus_packages_window = PardusPackagesWindow(self.main_window)
        self.pardus_packages_window.show()

    def firmware_bilgisi(self):
        # Firmware bilgilerini göster
        QMessageBox.information(self.main_window, "Firmware", "Firmware bilgileri burada gösterilecek")

    def sistem_ayrintilari(self):
        # Sistem ayrıntılarını göster
        QMessageBox.information(self.main_window, "Sistem Ayrıntıları", "Sistem ayrıntıları burada gösterilecek")

    def hakkinda(self):
        # Hakkında penceresi
        about_window = QWidget()
        about_window.setWindowTitle("Hakkında")
        about_window.setGeometry(100, 100, 300, 200)
        
        layout = QVBoxLayout()
        label = QLabel("Donanım Bilgileri Uygulaması\nSürüm 1.0\n\nGeliştiriciler:\nKubilay TUNÇ\nAli Rıza GİRİŞEN\n\n© 2024")
        layout.addWidget(label)
        about_window.setLayout(layout)
        about_window.show()

    def icindekiler(self):
        # İçindekiler/Yardım penceresi
        help_window = QWidget()
        help_window.setWindowTitle("İçindekiler")
        help_window.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        label = QLabel(
            "Uygulama Kullanım Kılavuzu\n\n"
            "1. Sistem Menüsü\n"
            "   - Pardus Paketler\n"
            "   - Firmware\n"
            "   - Ayrıntılar\n\n"
            "2. Yardım Menüsü\n"
            "   - Hakkında\n"
            "   - İçindekiler"
        )
        layout.addWidget(label)
        help_window.setLayout(layout)
        help_window.show()

    def hardware_update(self):
        # Donanım güncelleme sorusu
        response = QMessageBox.question(
            self.main_window,
            "Donanım Güncellemesi",
            "Donanım listeniz mevcut. Listeyi güncellemek ister misiniz?",
            QMessageBox.Yes | QMessageBox.No
        )

        if response == QMessageBox.Yes:
            self.perform_update()

    def perform_update(self):
        # Yükleme penceresi
        self.progress_dialog = QProgressDialog("Güncelleme yapılıyor, lütfen bekleyin...", None, 0, 0, self.main_window)
        self.progress_dialog.setWindowTitle("Yükleniyor")
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setCancelButton(None)  # İptal butonunu devre dışı bırak
        self.progress_dialog.show()

        # İşlemi başlat
        QTimer.singleShot(100, self.run_update)  # İşlemi biraz geciktir

    def run_update(self):
        try:
            hw_probe.getProbe()
            self.progress_dialog.close()
            QMessageBox.information(self.main_window, "Güncelleme", "Güncelleme tamamlandı.")
        except Exception as e:
            self.progress_dialog.close()
            QMessageBox.critical(self.main_window, "Hata", f"Güncelleme sırasında bir hata oluştu: {e}")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pardus Donanım Kontrol")
        self.setGeometry(100, 100, 800, 600)

        # Menü fonksiyonlarını başlat
        self.menu_functions = MenuFunctions(self)

        # Menü çubuğunu oluştur
        self.create_menu()

    def create_menu(self):
        menubar = self.menuBar()

        # Sistem menüsü
        sistem_menu = menubar.addMenu("Sistem")
        sistem_menu.addAction("Donanım Listesi Kontrol", self.menu_functions.hardware_update)
        sistem_menu.addAction("Pardus Paketler", self.menu_functions.pardus_paketler)
        sistem_menu.addAction("Firmware", self.menu_functions.firmware_bilgisi)
        sistem_menu.addAction("Ayrıntılar", self.menu_functions.sistem_ayrintilari)
        sistem_menu.addAction("Çıkış", self.close)

        # Yardım menüsü
        yardim_menu = menubar.addMenu("Yardım")
        yardim_menu.addAction("Hakkında", self.menu_functions.hakkinda)
        yardim_menu.addAction("İçindekiler", self.menu_functions.icindekiler)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())