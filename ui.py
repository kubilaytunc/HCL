from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem,
    QHeaderView, QScrollArea, QSplitter, QMenuBar, QMenu, QAction, QMessageBox, QProgressDialog
)
from PyQt5.QtGui import QPixmap, QColor, QFont 
from PyQt5.QtCore import Qt, QTimer
import os 
from hw_probe import getProbe
import constants
from devices import load_device_data
from host import load_host_data

def set_row_color(status):
    """Satır rengi belirleme."""
    if status == "works":
        return QColor("#A8E6A1")  # Yeşil
    elif status == "detected":
        return QColor("#A1D6E6")  # Mavi
    else:
        return QColor("#F2A1A1")  # Kırmızı

def open_device_check():
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
    return device_data, host_data

def create_ui(device_data, host_data):
    """PyQt5 arayüzünü oluşturur."""
    window = QMainWindow()
    window.setWindowTitle("Donanım Bilgisi Görüntüleme")
    window.setGeometry(100, 100, 1200, 800)

    # Üst menü çubuğu oluştur
    menubar = window.menuBar()

    # Dosya menüsü
    file_menu = menubar.addMenu('Sistem')

    def confirm_update():
        """Onay kutusunu aç ve kullanıcının seçimine göre pencereyi güncelle"""
        msg_box = QMessageBox(window)
        msg_box.setWindowTitle("Güncelleme")
        msg_box.setText("Donanım listesini güncellemek istiyor musunuz?")

        evet_button = msg_box.addButton("Evet", QMessageBox.YesRole)
        hayir_button = msg_box.addButton("Hayır", QMessageBox.NoRole)

        msg_box.exec_()

        if msg_box.clickedButton() == evet_button:
            # Güncelleme işlemi sırasında loading göstergesi göster
            progress = QProgressDialog("Güncelleme yapılıyor...", "İptal", 0, 0, window)
            progress.setWindowTitle("Güncelleme")
            progress.setWindowModality(Qt.WindowModal)
            progress.show()

            # Güncelleme işlemini başlat
            QTimer.singleShot(2000, lambda: perform_update(progress))  # 2 saniye sonra güncelleme işlemini başlat
        else:
            print("Güncelleme iptal edildi.")

    def perform_update(progress):
        """Güncelleme işlemini gerçekleştir ve pencereyi yenile."""
        device_data, host_data = open_device_check()
        progress.close()

        # Güncelleme tamamlandı mesajı göster
        QMessageBox.information(window, "Güncelleme Tamamlandı", "Donanım listesi başarıyla güncellendi.")

        # Pencereyi yenile
        window.close()
        new_window = create_ui(device_data, host_data)
        new_window.show()

    update_action = QAction('Donanım Listesi Güncelle', window)
    update_action.triggered.connect(confirm_update)
    file_menu.addAction(update_action)

    # Çıkış eylemi
    exit_action = QAction('Çıkış', window)
    exit_action.triggered.connect(window.close)
    file_menu.addAction(exit_action)

    # Ana container widget
    main_widget = QWidget()
    main_layout = QHBoxLayout(main_widget)

    # Sol ve sağ alanlar için splitter
    splitter = QSplitter(Qt.Horizontal)

    # Sol kısım: Bilgi alanı
    left_widget = QWidget()
    left_layout = QVBoxLayout(left_widget)

    # Sol kısımda bilgi alanı
    left_layout.addWidget(QLabel(f"{host_data.get('vendor', 'N/A')} {host_data.get('model', 'N/A')}", font=QFont("Arial", 14, QFont.Bold)))
    left_layout.addWidget(QLabel(f"Test Edilen Sürüm: {host_data.get('system', 'N/A')}"))
    left_layout.addWidget(QLabel(f"Mimari: {host_data.get('arch', 'N/A')}"))
    left_layout.addWidget(QLabel(f"Kernel: {host_data.get('kernel', 'N/A')}"))
    left_layout.addWidget(QLabel(f"Marka: {host_data.get('vendor', 'N/A')}"))
    left_layout.addWidget(QLabel(f"Model: {host_data.get('model', 'N/A')}"))
    left_layout.addWidget(QLabel(f"Yıl: {host_data.get('year', 'N/A')}"))
    left_layout.addWidget(QLabel(f"Tür: {host_data.get('type', 'N/A')}"))
    left_layout.addWidget(QLabel(f"Dil: {host_data.get('lang', 'N/A')}"))
    left_layout.addWidget(QLabel(f"Dosya Sistemi: {host_data.get('filesystem', 'N/A')}"))

    # Pardus/Linux uyumluluğunu kontrol et ve göster
    system = host_data.get('system', '').lower()
    if "pardus" in system or "linux" in system:
        try:
            pardus_image = QPixmap("assets/pardus.png")
            pardus_label = QLabel()
            pardus_label.setPixmap(pardus_image.scaled(100, 100, Qt.KeepAspectRatio))
            left_layout.addWidget(pardus_label)
            left_layout.addWidget(QLabel("Bu cihaz Pardus/Linux Uyumludur", font=("Arial", 10, QFont.Bold)))
        except Exception as e:
            print(f"Pardus resmi yüklenirken hata: {e}")

    # Sol kısımın sağ altına PNG ekle
    try:
        bottom_image = QPixmap("assets/pardus.png")  # PNG dosyasının yolunu belirtin
        bottom_label = QLabel()
        bottom_label.setPixmap(bottom_image.scaled(100, 100, Qt.KeepAspectRatio))
        left_layout.addStretch()  # İçeriği yukarı itmek için boşluk ekle
        left_layout.addWidget(bottom_label, alignment=Qt.AlignRight | Qt.AlignBottom)
    except Exception as e:
        print(f"Sağ alt resim yüklenirken hata: {e}")

    # Sol widget'ı bir QScrollArea içine al
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setWidget(left_widget)

    # Sol widget'ın genişliğini esnek yap
    left_widget.setMinimumWidth(200)  # Sol panelin minimum genişliğini ayarla

    # Sağ kısım: Tablo alanı
    right_widget = QWidget()
    right_layout = QVBoxLayout(right_widget)

    # Tablo oluştur
    table = QTableWidget()
    table.setColumnCount(6)
    table.setHorizontalHeaderLabels(["ID/Sınıf", "Üretici", "Cihaz", "Tür", "Sürücü", "Durum"])
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # Tablodaki hücrelerin değiştirilememesi için
    table.setEditTriggers(QTableWidget.NoEditTriggers)

    # Başlıklara çift tıklayarak sıralama yapmak için
    table.setSortingEnabled(True)

    # Veriyi tabloya ekle
    table.setRowCount(len(device_data))
    for row, (key, value) in enumerate(device_data.items()):
        id_class = f"{value['Bus']} / {value.get('Class', 'N/A')}"
        vendor = value.get("Vendor", "N/A")
        device = value.get("Device", "N/A")
        type_ = value.get("Type", "N/A")
        driver = value.get("Driver", "N/A")
        status = value.get("Status", "N/A")

        display_status = "Çalışıyor" if status == "works" else "Tespit Edildi" if status == "detected" else "Çalışmıyor" if status == "failed" else status
        row_color = set_row_color(status)

        # Tablo hücrelerini oluştur ve düzenlenemez yap
        item_id_class = QTableWidgetItem(id_class)
        item_vendor = QTableWidgetItem(vendor)
        item_device = QTableWidgetItem(device)
        item_type = QTableWidgetItem(type_)
        item_driver = QTableWidgetItem(driver)
        item_status = QTableWidgetItem(display_status)

        # Hücrelerin arka plan rengini ayarla
        for item in [item_id_class, item_vendor, item_device, item_type, item_driver, item_status]:
            item.setBackground(row_color)

        # Hücreleri tabloya ekle
        table.setItem(row, 0, item_id_class)
        table.setItem(row, 1, item_vendor)
        table.setItem(row, 2, item_device)
        table.setItem(row, 3, item_type)
        table.setItem(row, 4, item_driver)
        table.setItem(row, 5, item_status)

    right_layout.addWidget(table)

    # Splitter'a sol ve sağ widget'ları ekle
    splitter.addWidget(scroll_area)  # Sol kısmı QScrollArea içine al
    splitter.addWidget(right_widget)
    main_layout.addWidget(splitter)

    # Splitter için esnek genişlik ayarları yap
    splitter.setSizes([250, 800])  # Sol panel için 250px, sağ panel için 800px başlangıç genişliği

    # Ana pencereye widget'ı ekle
    window.setCentralWidget(main_widget)
    return window