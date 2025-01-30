from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt

class PardusPackagesWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pardus Paketler")
        self.setFixedSize(400, 500)  # Pencere boyutunu sabitle

        # Ana layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)  # Butonları ortala

        # Butonlar
        buttons = [
            ("Güncellenebilirlik", self.check_updates),
            ("Backports Depolar", self.backports_repos),
            ("Debian Firmware Paketleri", self.debian_firmware),
            ("Kernel Seçenekleri", self.kernel_options),
            ("Çıkış", self.close)
        ]

        for text, slot in buttons:
            button = QPushButton(text)
            button.clicked.connect(slot)
            layout.addWidget(button)

    def check_updates(self):
        # Güncellenebilir paketleri kontrol et
        QMessageBox.information(self, "Güncellemeler",
                              "Sistem güncellemeleri kontrol ediliyor...\n"
                              "Bu özellik henüz geliştirme aşamasındadır.")

    def backports_repos(self):
        # Backports depolarını göster/yönet
        QMessageBox.information(self, "Backports Depolar",
                              "Backports depo yönetimi...\n"
                              "Bu özellik henüz geliştirme aşamasındadır.")

    def debian_firmware(self):
        # Debian firmware paketlerini listele
        QMessageBox.information(self, "Debian Firmware",
                              "Debian firmware paketleri listeleniyor...\n"
                              "Bu özellik henüz geliştirme aşamasındadır.")

    def kernel_options(self):
        # Kernel seçeneklerini göster
        QMessageBox.information(self, "Kernel Seçenekleri",
                              "Kernel seçenekleri görüntüleniyor...\n"
                              "Bu özellik henüz geliştirme aşamasındadır.")


# Örnek kullanım
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = PardusPackagesWindow()
    window.show()
    sys.exit(app.exec_())