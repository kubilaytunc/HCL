from PyQt5.QtWidgets import (
    QApplication, QWidget, QMessageBox, QVBoxLayout, QPushButton, QDialog
)
from PyQt5.QtCore import Qt
import sys
from sssd_join import SSSDJoinUI  # Yeni pencere açmadan bu sınıfı kullanacağız

class DomainJoinerWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pardus Domaine Al")
        self.setFixedSize(400, 500)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)

        self.sssd_button = QPushButton("SSSD")
        self.sssd_button.clicked.connect(self.sssd_join)

        self.winbind_button = QPushButton("WINBIND")
        self.winbind_button.clicked.connect(self.winbind_join)

        self.exit_button = QPushButton("Çıkış")
        self.exit_button.clicked.connect(self.close)

        self.layout.addWidget(self.sssd_button)
        self.layout.addWidget(self.winbind_button)
        self.layout.addWidget(self.exit_button)

        # Varsayılan görünüm
        self.current_widget = None

    def sssd_join(self):
        """SSSDJoinUI'yi mevcut pencerenin içinde göster."""
        QMessageBox.information(self, "SSSD için gerekli bilgiler",
                                "AD veya Samba üzerinde yetkili bir kullanıcı\n"
                                "Yetkili kullanıcı parolası\n"
                                "AD veya Samba DC ip adresi.")

        if self.current_widget:
            self.layout.removeWidget(self.current_widget)
            self.current_widget.deleteLater()

        self.current_widget = SSSDJoinUI()  # Yeni pencere yerine burada göster
        self.layout.addWidget(self.current_widget)

    def winbind_join(self):
        """Winbind için bilgi mesajı gösterir."""
        QMessageBox.information(self, "Winbind için gerekli bilgiler",
                                "AD veya Samba üzerinde yetkili bir kullanıcı\n"
                                "Yetkili kullanıcı parolası\n"
                                "AD veya Samba DC ip adresi.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DomainJoinerWindow()
    window.show()
    sys.exit(app.exec_())
