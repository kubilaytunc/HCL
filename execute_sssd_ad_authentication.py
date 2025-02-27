import subprocess
import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QPushButton, QTextEdit

class AuthProgress(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Domaine Katılım Süreci")
        self.setGeometry(100, 100, 500, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("İşlem Durumu:")
        self.layout.addWidget(self.label)

        self.progress = QProgressBar(self)
        self.progress.setMaximum(7)  # 7 Adım var
        self.layout.addWidget(self.progress)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.layout.addWidget(self.log_output)

        self.close_button = QPushButton("Kapat")
        self.close_button.clicked.connect(self.close)
        self.close_button.setEnabled(False)
        self.layout.addWidget(self.close_button)

        self.setLayout(self.layout)

    def log(self, message):
        """Log mesajlarını arayüze ekler."""
        self.log_output.append(message)
        QApplication.processEvents()

    def authenticate(self, domain_name, host_name, ip_address, password, ad_username, dynamic_dns_update):
        try:
            self.log("📦 Paketler yükleniyor...")
            self.progress.setValue(1)
            self.install_packages()
            
            self.log("🔄 Mevcut domaine üyelik kontrol ediliyor...")
            self.progress.setValue(2)
            self.leave_realm()

            self.log("📝 DNS ayarları yapılandırılıyor...")
            self.progress.setValue(3)
            self.configure_dns(domain_name, ip_address)

            self.log("📌 Hosts dosyası güncelleniyor...")
            self.progress.setValue(4)
            self.configure_hosts(ip_address, host_name)

            self.log("🔧 PAM ayarları güncelleniyor...")
            self.progress.setValue(5)
            self.configure_pam()

            self.log("🔍 Domaine ait bilgiler alınıyor...")
            self.progress.setValue(6)
            self.realm_discover(domain_name)

            self.log("🔐 Domaine katılım işlemi başlatılıyor...")
            self.progress.setValue(7)
            self.realm_join(domain_name, password, ad_username)

            self.log("✅ Tüm işlemler başarıyla tamamlandı!")
            self.close_button.setEnabled(True)
        except Exception as e:
            self.log(f"❌ Hata oluştu: {str(e)}")

    def install_packages(self):
        """Gerekli paketleri non-interactive olarak yükler."""
        packages = [
            "realmd", "sssd", "sssd-tools", "adcli", "packagekit",
            "samba-common-bin", "samba-libs", "libsss-sudo"
        ]
        subprocess.run(["apt-get", "update"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["apt-get", "install", "-y", "--no-install-recommends"] + packages, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def leave_realm(self):
        """Mevcut domaine üyelik varsa kaldırır."""
        result = subprocess.run(["realm", "leave"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            self.log("✅ Mevcut domaine üyelik kaldırıldı.")

    def configure_dns(self, domain_name, ip_address):
        """resolv.conf dosyasına IP adresi ve domain ekler."""
        with open("/etc/resolv.conf", "a") as f:
            f.write(f"\nnameserver {ip_address}\nsearch {domain_name}\n")

    def configure_hosts(self, ip_address, host_name):
        """/etc/hosts dosyasına IP, tam domain adı ve kısa domain adı ekler."""
        host_parts = host_name.split('.', 1)  # İlk noktaya göre iki parçaya ayır
        if len(host_parts) > 1:
            domain_part = host_parts[1]  # İlk kelime hariç geri kalan
        else:
            domain_part = host_name  # Eğer nokta yoksa, orijinal değer

        with open("/etc/hosts", "a") as f:
            f.write(f"\n{ip_address} {host_name} {domain_part}\n")

    def configure_pam(self):
        """/etc/pam.d/common-session dosyasına home dizini açmayı ekler."""
        pam_line = "session optional        pam_mkhomedir.so skel=/etc/skel umask=077\n"
        with open("/etc/pam.d/common-session", "a") as f:
            f.write(pam_line)

    def realm_discover(self, domain_name):
        """Realm discover ile domain bilgilerini alır."""
        result = subprocess.run(["realm", "discover", domain_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            self.log("✅ Domain bilgileri:\n" + result.stdout)
        else:
            self.log("❌ Domain bilgileri alınamadı:\n" + result.stderr)

    def realm_join(self, domain_name, password, ad_username):
    
        command = f'echo {password} | realm join --user={ad_username} {domain_name}'
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            self.log("✅ Domaine başarıyla katılım sağlandı!")
        else:
            self.log("❌ Domaine katılım başarısız:\n" + result.stderr)


def authenticate(domain_name, host_name, ip_address, password, ad_username, dynamic_dns_update):
    """Qt arayüzü ile domaine katılım sürecini başlatır."""

    app = QApplication.instance()
    if app is None:  # Eğer zaten bir QApplication yoksa oluştur
        app = QApplication(sys.argv)

    window = AuthProgress()
    window.show()
    window.authenticate(domain_name, host_name, ip_address, password, ad_username, dynamic_dns_update)

    if app.applicationState() == 0:  # Eğer app kapalıysa çalıştır
        sys.exit(app.exec_())

