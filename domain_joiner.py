from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QPushButton, QMessageBox, QApplication
)
from PyQt5.QtCore import Qt

class DomainJoinerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pardus Domaine Al")
        self.setFixedSize(400, 500)  # Pencere boyutunu sabitle

        # Ana layout
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)  # Butonları ortala

        # Butonlar
        buttons = [
            ("SSSD", self.sssd_join),
            ("WINBIND", self.winbind_join),
            ("Çıkış", self.close)
        ]

        for text, slot in buttons:
            button = QPushButton(text)
            button.clicked.connect(slot)
            layout.addWidget(button)

    def sssd_join(self):
        # SSSD ile yapılacak işlemler
        QMessageBox.information(self, "SSSD için gerekli bilgiler",
                              "AD veya Samba üzerinde yetkili bir kullanıcı\n"
                                "Yetkili kullanıcı parolası\n"
                              "AD veya Samba DC ip adresi.")

    def winbind_join(self):
        # Winbind ile yapılacak işlemler
        QMessageBox.information(self, "Winbind için gerekli bilgiler",
                              "AD veya Samba üzerinde yetkili bir kullanıcı\n"
                                 "Yetkili kullanıcı parolası\n"
                              "AD veya Samba DC ip adresi.")


# Örnek kullanım
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = DomainJoinerWindow()
    window.show()
    sys.exit(app.exec_())
