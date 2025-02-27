import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QCheckBox, QMessageBox
)
from execute_sssd_ad_authentication import authenticate  # authenticate fonksiyonunu içe aktar

class SSSDJoinUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SSSD Join")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

        self.domain_label = QLabel("Domain Adı:")
        self.domain_input = QLineEdit()

        self.host_label = QLabel("Sunucu Host Adı:")
        self.host_input = QLineEdit()

        self.ip_label = QLabel("Sunucu IP Adresi:")
        self.ip_input = QLineEdit()

        self.user_label = QLabel("AD Yetkili Kullanıcı:")
        self.user_input = QLineEdit()

        self.password_label = QLabel("Yetkili Kullanıcı Parola:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.dns_label = QLabel("Dynamic DNS Update:")
        self.dns_checkbox = QCheckBox("Enable Dynamic DNS Update")

        self.join_button = QPushButton("Domaine Katıl")
        self.join_button.clicked.connect(self.execute_join)

        layout.addWidget(self.domain_label)
        layout.addWidget(self.domain_input)
        layout.addWidget(self.host_label)
        layout.addWidget(self.host_input)
        layout.addWidget(self.ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(self.user_label)
        layout.addWidget(self.user_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.dns_label)
        layout.addWidget(self.dns_checkbox)
        layout.addWidget(self.join_button)

        self.setLayout(layout)

    def execute_join(self):
        """Kullanıcıdan alınan bilgileri kullanarak authenticate fonksiyonunu çağırır."""
        domain_name = self.domain_input.text().strip()
        host_name = self.host_input.text().strip()
        ip_address = self.ip_input.text().strip()
        password = self.password_input.text().strip()
        ad_username = self.user_input.text().strip()
        dynamic_dns_update = self.dns_checkbox.isChecked()  # True veya False dönecek

        if not (domain_name and host_name and ip_address and password and ad_username):
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")
            return

        # execute_sssd_ad_authentication.py'deki authenticate fonksiyonunu çağır
        try:
            authenticate(domain_name, host_name, ip_address, password, ad_username, dynamic_dns_update)
            
            # İşlem başarılı olduğunda pop-up göster
            QMessageBox.information(self, "Başarılı", "Domaine katılım başarılı!")
            
            # Pencereyi kapat
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")

def sssd_join():
    """Arayüzü açan fonksiyon. Eğer mevcut bir QApplication varsa tekrar oluşturmaz."""
    app = QApplication.instance()  # Zaten bir instance var mı kontrol et
    if app is None:  
        app = QApplication(sys.argv)  # Yoksa yeni bir tane oluştur

    window = SSSDJoinUI()
    window.show()
