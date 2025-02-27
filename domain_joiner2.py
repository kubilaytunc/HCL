import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QVBoxLayout, QLabel, QLineEdit, QPushButton, QDialog

class DomainJoiner(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Debian AD Domain Join")
        self.setGeometry(100, 100, 350, 250)

        layout = QVBoxLayout()

        self.dc_ip_label = QLabel("DC IP Adresi:")
        self.dc_ip_input = QLineEdit()

        self.domain_label = QLabel("Domain Adı:")
        self.domain_input = QLineEdit()

        self.username_label = QLabel("Yetkili Kullanıcı:")
        self.username_input = QLineEdit()

        self.password_label = QLabel("Şifre:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.join_button = QPushButton("Domaine Katıl")
        self.join_button.clicked.connect(self.join_domain)

        layout.addWidget(self.dc_ip_label)
        layout.addWidget(self.dc_ip_input)
        layout.addWidget(self.domain_label)
        layout.addWidget(self.domain_input)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.join_button)

        self.setLayout(layout)

    def run_command(self, command):
        """Shell komutlarını çalıştırıp çıktı döndürür."""
        result = subprocess.run(command, shell=True, text=True, capture_output=True)
        return result.returncode, result.stdout, result.stderr

    def join_domain(self):
        dc_ip = self.dc_ip_input.text().strip()
        domain = self.domain_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not dc_ip or not domain or not username or not password:
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        try:
            QMessageBox.information(self, "Başlatılıyor", "Domain'e katılım işlemi başlatılıyor...")

            # 1️⃣ Gerekli Paketleri Yükle
            self.run_command("sudo apt update && sudo apt install -y sssd realmd adcli samba-common-bin oddjob oddjob-mkhomedir packagekit libnss-sss libpam-sss")

            # 2️⃣ Hostname ve DNS Ayarları
#            hostname_command = f"sudo hostnamectl set-hostname {domain}"
#            self.run_command(hostname_command)

            resolv_conf = f"nameserver {dc_ip}\nsearch {domain}"
            with open("/etc/resolv.conf", "w") as resolv_file:
                resolv_file.write(resolv_conf)

            # 3️⃣ Domaine Katılım
            join_command = f'echo {password} | sudo realm join --user={username} {domain}'
            returncode, stdout, stderr = self.run_command(join_command)

            if returncode == 0:
                QMessageBox.information(self, "Başarılı", "Makine başarıyla domaine katıldı!")
            else:
                QMessageBox.critical(self, "Hata", f"Domaine katılamadı!\n{stderr}")
                return

            # 4️⃣ SSSD Yapılandırması
            sssd_config = f"""
[sssd]
domains = {domain}
config_file_version = 2
services = nss, pam

[domain/{domain}]
id_provider = ad
access_provider = ad
auth_provider = ad
chpass_provider = ad
ldap_id_mapping = true
fallback_homedir = /home/%u
default_shell = /bin/bash
use_fully_qualified_names = False

[pam]
pam_cert_auth = False
"""
            with open("/etc/sssd/sssd.conf", "w") as sssd_file:
                sssd_file.write(sssd_config)

            self.run_command("sudo chmod 600 /etc/sssd/sssd.conf")

            # 5️⃣ Servisleri Başlat
            self.run_command("sudo systemctl enable --now sssd")
            self.run_command("sudo systemctl restart sssd")

            QMessageBox.information(self, "Tamamlandı", "Domaine katılım işlemi tamamlandı. Yeniden başlatmanız önerilir.")

        except Exception as e:
            QMessageBox.critical(self, "Hata", f"Bir hata oluştu: {str(e)}")


def sssd_join():
    app = QApplication(sys.argv)

    QMessageBox.information(None, "Bilgilendirme", "Bu işlem, bilgisayarı domaine eklemek için yapılacaktır.")

    dialog = DomainJoiner()
    dialog.exec_()  # PyQt5'te exec_() kullanılır

    sys.exit(app.exec_())  # PyQt5'te exec_() kullanılır

if __name__ == "__main__":
    sssd_join()
