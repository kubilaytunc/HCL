import sys
import subprocess
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QDialog, QLabel, QComboBox, QVBoxLayout, QPushButton
from PyQt5.QtGui import QIcon
from devices import load_device_data
from host import load_host_data
import constants
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtCore import Qt

class KernelApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

        # DOSYA YOLU PARDUS SÜRÜMÜNE GÖRE DİNAMİK AYARLANACAK
        
        with open("/etc/os-release", "r") as f:
            for line in f:
                if line.startswith("VERSION_CODENAME="):
                    self.pardus_version = line.strip().split("=", 1)[1].strip('"')

        self.backports_file = f"/etc/apt/sources.list.d/{self.pardus_version}-backports.list"

        # Eğer backports dosyası varsa, butonu disable et
        self.update_backports_button_state()

    def initUI(self):
        self.setWindowTitle('Kernel Uygulaması')
        self.setGeometry(100, 100, 400, 300)
    
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
    
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # Butonları merkeze hizala
    
        self.btn_view_current_kernel = QPushButton('Mevcut Kernel Sürümünü Görüntüle', self)
        self.btn_view_current_kernel.clicked.connect(self.on_btn_view_current_kernel_clicked)
        layout.addWidget(self.btn_view_current_kernel)
    
        self.btn_update_kernel = QPushButton('Kernel Güncelle', self)
        self.btn_update_kernel.clicked.connect(self.on_btn_update_kernel_clicked)
        layout.addWidget(self.btn_update_kernel)
    
        self.btn_view_backports = QPushButton('Backports Kernelleri Ekle', self)
        self.btn_view_backports.clicked.connect(self.on_btn_view_backports_clicked)
        layout.addWidget(self.btn_view_backports)
    
        self.btn_exit = QPushButton('Çıkış', self)
        self.btn_exit.clicked.connect(self.on_btn_exit_clicked)
        layout.addWidget(self.btn_exit)
    
        central_widget.setLayout(layout)

    def update_backports_button_state(self):
        # Backports dosyasının mevcut olup olmadığını kontrol et
        if os.path.exists(self.backports_file):
            self.btn_view_backports.setText("Backports Kernelleri Kaldır")  # Etiketi değiştir
        else:
            self.btn_view_backports.setText("Backports Kernelleri Ekle")  # Varsayılan etiket

    def on_btn_view_current_kernel_clicked(self):
        try:
            result = subprocess.check_output(["uname", "-r"], text=True).strip()
            self.show_message(f"Mevcut Kernel Sürümü: {result}")
        except subprocess.CalledProcessError:
            self.show_message("Kernel sürümü alınamadı.", QMessageBox.Critical)

    def extract_version(self, package_name):
        """
        Paket adından versiyon numarasını ayıklar.
        Örneğin: 'linux-image-5.15.0-58-generic' -> '5.15.0-58'
        """
        prefix = "linux-image-"
        if package_name.startswith(prefix):
            version = package_name[len(prefix):]
            return version
        return None

    def on_btn_update_kernel_clicked(self):
        try:
            # 1. Mevcut kernel sürümünü al
            current_kernel = subprocess.check_output(["uname", "-r"], text=True).strip()
            current_version = current_kernel.split("-")[0]  # Versiyon kısmını al

            # 2. Depolardaki kernel paketlerini al ve versiyonları ayıkla
            kernel_packages = subprocess.check_output(
                ["apt-cache", "search", "linux-image-"],
                text=True
            ).splitlines()

            # 3. Yalnızca 'amd64' ile biten ve 'linux-image' ile başlayan paketleri filtrele
            available_kernels = []
            for line in kernel_packages:
                parts = line.split()
                if len(parts) > 0:
                    package_name = parts[0]
                    if package_name.startswith("linux-image-") and package_name.endswith("-amd64"):
                        version = self.extract_version(package_name)
                        if version and version > current_version:
                            available_kernels.append(package_name)

            if not available_kernels:
                self.show_message("Yükseltme için uygun kernel bulunamadı.")
                return

            # 4. Kullanıcıya seçim sun
            selected_kernel = self.select_kernel_dialog(available_kernels)
            if selected_kernel:
                # 5. Seçilen versiyona ait tüm paketleri kur
                self.install_kernel(selected_kernel)

        except subprocess.CalledProcessError as e:
            self.show_message(f"Hata oluştu: {str(e)}", QMessageBox.Critical)

    def install_kernel(self, selected_kernel):
        try:
            # Seçilen kernel'in version kısmını al
            selected_kernel_version = self.extract_version(selected_kernel)

            # Seçilen kernel'i kur
            subprocess.run(
                ["sudo", "apt", "install", "-y", selected_kernel],
                check=True
            )

            # Seçilen kernel için linux-headers paketini kur
            headers_package = f"linux-headers-{selected_kernel_version}-amd64"
            subprocess.run(
                ["sudo", "apt", "install", "-y", headers_package],
                check=True
            )

            self.show_message(
                f"{selected_kernel} kernel ve {headers_package} başarıyla kuruldu. Sistemi yeniden başlatın.")
        except subprocess.CalledProcessError as e:
            self.show_message(f"Kernel kurulumu başarısız: {str(e)}", QMessageBox.Critical)

    def select_kernel_dialog(self, kernels):
        dialog = QDialog(self)
        dialog.setWindowTitle("Kernel Seçimi")
        layout = QVBoxLayout()

        label = QLabel("Yükseltmek istediğiniz kernel sürümünü seçin:")
        layout.addWidget(label)

        combo = QComboBox()
        for kernel in kernels:
            combo.addItem(kernel)
        layout.addWidget(combo)

        btn_ok = QPushButton("Tamam")
        btn_ok.clicked.connect(dialog.accept)
        layout.addWidget(btn_ok)

        btn_cancel = QPushButton("İptal")
        btn_cancel.clicked.connect(dialog.reject)
        layout.addWidget(btn_cancel)

        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            return combo.currentText()
        else:
            return None

    def show_message(self, message, message_type=QMessageBox.Information):
        msg_box = QMessageBox(self)
        msg_box.setIcon(message_type)
        msg_box.setText(message)
        msg_box.setWindowTitle("Bilgi")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def on_btn_view_backports_clicked(self):
        if os.path.exists(self.backports_file):
            # Backports dosyasını sil
            try:
                subprocess.run(["sudo", "rm", "-rf", self.backports_file], check=True)
                if self.pardus_version != "ondokuz":
                    subprocess.run(["sudo", "rm", "-rf", f"/etc/apt/sources.list.d/experimental-{self.pardus_version}-firmware.list"], check=True)
                    subprocess.run(["sudo", "apt", "update"], check=True)
                self.show_message("Backports kernel kaynakları kaldırıldı ve apt update yapıldı.")
                # Buton etiketini tekrar değiştirme
                self.btn_view_backports.setText("Backports Kernelleri Ekle")
            except subprocess.CalledProcessError as e:
                self.show_message(f"Hata oluştu: {str(e)}", QMessageBox.Critical)
        else:
            # Backports dosyasını ekle
            self.on_btn_add_backports_clicked()

    def on_btn_add_backports_clicked(self):
        print("Backports kernelleri ekleniyor ve görüntüleniyor...")
        try:
            # 1. Backports deposunu ekle

            if self.pardus_version == "yirmiuc" or self.pardus_version == "yirmibes":
                subprocess.run(
                ["sudo", "sh", "-c",
                 f'echo "deb http://depo.pardus.org.tr/backports {self.pardus_version}-backports main contrib non-free non-free-firmware" > /etc/apt/sources.list.d/{self.pardus_version}-backports.list'],
                check=True
                )
                subprocess.run(
                ["sudo", "sh", "-c",
                 f'echo "deb http://depo.pardus.org.tr/experimental {self.pardus_version}-firmware non-free" > /etc/apt/sources.list.d/experimental-{self.pardus_version}-firmware.list'],
                check=True
                )

            elif self.pardus_version == "yirmibir" or self.pardus_version == "ondokuz":
                subprocess.run(
                ["sudo", "sh", "-c",
                 f'echo "deb http://depo.pardus.org.tr/backports {self.pardus_version}-backports main contrib non-free" > /etc/apt/sources.list.d/{self.pardus_version}-backports.list'],
                check=True
                )
                if self.pardus_version == "yirmibir":
                    subprocess.run(
                    ["sudo", "sh", "-c",
                     'echo "deb http://depo.pardus.org.tr/experimental yirmibir-firmware non-free" > /etc/apt/sources.list.d/experimental-yirmibir-firmware.list'],
                    check=True
                    )

            # 2. Paket listelerini güncelle
            subprocess.run(["sudo", "apt", "update"], check=True)

            self.show_message("Backports kernel kaynakları eklendi ve apt update yapıldı.")
            # Buton etiketini değiştir
            self.btn_view_backports.setText("Backports Kernelleri Kaldır")

            # 1. Mevcut kernel sürümünü al
            current_kernel = subprocess.check_output(["uname", "-r"], text=True).strip()
            current_version = current_kernel.split("-")[0]  # Versiyon kısmını al

            # 2. Depolardaki kernel paketlerini al ve versiyonları ayıkla
            kernel_packages = subprocess.check_output(
                ["apt-cache", "search", "linux-image"],
                text=True
            ).splitlines()

            # 3. Yalnızca 'amd64' ile biten ve 'linux-image' ile başlayan paketleri filtrele
            available_kernels = []
            for line in kernel_packages:
                parts = line.split()
                if len(parts) > 0:
                    package_name = parts[0]
                    if package_name.startswith("linux-image-") and package_name.endswith("amd64"):
                        version = self.extract_version(package_name)
                        if version and version > current_version:
                            available_kernels.append(package_name)

            if not available_kernels:
                self.show_message("Yükseltme için uygun kernel bulunamadı.")
                return

            # 4. Kullanıcıya seçim sun
            selected_kernel = self.select_kernel_dialog(available_kernels)
            if selected_kernel:
                # 5. Seçilen versiyona ait tüm paketleri kur
                self.install_kernel(selected_kernel)

        except subprocess.CalledProcessError as e:
            self.show_message(f"Hata oluştu: {str(e)}", QMessageBox.Critical)

    def on_btn_install_backports_clicked(self):
        print("Backports kernel kurulumu yapılıyor...")

    def on_btn_extra_packages_clicked(self):
        print("Ek paketler yönetiliyor...")

    def on_btn_exit_clicked(self):
        print("Kernel backports kapatılıyor...")
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = KernelApp()
    window.show()
    sys.exit(app.exec_())