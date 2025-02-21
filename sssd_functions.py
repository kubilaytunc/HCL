import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog

class DomainJoinDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Domaine Al")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.dc_ip_label = QLabel("DC IP Adresi:")
        self.dc_ip_input = QLineEdit()

        self.username_label = QLabel("Yetkili Kullanıcı:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)  # PyQt5'te kullanım böyle

        self.join_button = QPushButton("Domaine Katıl")
        self.join_button.clicked.connect(self.join_domain)

        layout.addWidget(self.dc_ip_label)
        layout.addWidget(self.dc_ip_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.join_button)

        self.setLayout(layout)

    def join_domain(self):
        dc_ip = self.dc_ip_input.text()
        username = self.username_input.text()
        password = self.password_input.text()

        if not dc_ip or not username or not password:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return
        
        try:
            # realm join ile domaine katılma komutu
            command = f'echo {password} | realm join --user={username} {dc_ip}'
            result = subprocess.run(command, shell=True, text=True, capture_output=True)

            if result.returncode == 0:
                QMessageBox.information(self, "Başarılı", "Domaine başarıyla katıldınız.")
            else:
                QMessageBox.critical(self, "Hata", f"Domaine katılamadı!\nHata: {result.stderr}")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")


def sssd_join():
    app = QApplication(sys.argv)

    QMessageBox.information(None, "Bilgilendirme", "Bu işlem, bilgisayarı domaine eklemek için yapılacaktır.")

    dialog = DomainJoinDialog()
    dialog.exec_()  # PyQt5'te exec_() kullanılır

    sys.exit(app.exec_())  # PyQt5'te exec_() kullanılır

if __name__ == "__main__":
    sssd_join()
