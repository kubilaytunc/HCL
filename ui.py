import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Pardus resmi için

def set_row_color(status):
    """Satır rengi belirleme."""
    if status == "works":
        return "#A8E6A1"  # Yeşil
    elif status == "detected":
        return "#A1D6E6"  # Mavi
    else:
        return "#F2A1A1"  # Kırmızı


def create_ui(root, device_data, host_data):
    """Tkinter arayüzünü oluşturur."""

    # Ekran boyutlarını alma
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Pencereyi ekran boyutuna göre ayarlama
    root.geometry(f"{screen_width}x{screen_height}")

    # Sol kısım: Bilgi Alanı
    info_frame = tk.Frame(root, padx=10, pady=10)
    info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

    # Sağ kısım: Tablo Alanı
    table_frame = tk.Frame(root, padx=10, pady=10)
    table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Sol kısımdaki bilgileri yerleştirme
    tk.Label(info_frame, text=f"{host_data.get('vendor', 'N/A')} {host_data.get('model', 'N/A')}", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
    tk.Label(info_frame, text=f"Test Edilen Sürüm: {host_data.get('system', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Mimari: {host_data.get('arch', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Kernel: {host_data.get('kernel', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Marka: {host_data.get('vendor', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Model: {host_data.get('model', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Yıl: {host_data.get('year', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Tür: {host_data.get('type', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Dil: {host_data.get('lang', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    tk.Label(info_frame, text=f"Dosya Sistemi: {host_data.get('filesystem', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)

    # Pardus/Linux uyumluluğunu kontrol et ve göster
    system = host_data.get('system', '').lower()
    if "pardus" in system or "linux" in system:
        try:
            pardus_image = Image.open("assets/pardus.png")
            pardus_image = pardus_image.resize((100, 100), Image.ANTIALIAS)
            pardus_photo = ImageTk.PhotoImage(pardus_image)
            img_label = tk.Label(info_frame, image=pardus_photo)
            img_label.image = pardus_photo  # Referansı sakla
            img_label.pack(side=tk.BOTTOM, pady=10)
            tk.Label(info_frame, text="Bu cihaz Pardus/Linux Uyumludur", font=("Arial", 10, "bold"), fg="green").pack(side=tk.BOTTOM, pady=5)
        except Exception as e:
            print(f"Pardus resmi yüklenirken hata: {e}")

    # Sağ kısımda Treeview widget'ı oluşturma
    tree = ttk.Treeview(table_frame, columns=("ID/Sınıf", "Üretici", "Cihaz", "Tür", "Sürücü", "Durum"), show="headings")


    # Dinamik sütun genişlikleri hesaplama
    total_width = screen_width * 0.65  # Sağ kısma ayrılan alanın genişliği
    col_widths = {
        "ID/Sınıf": int(total_width * 0.2),
        "Üretici": int(total_width * 0.15),
        "Cihaz": int(total_width * 0.3),
        "Tür": int(total_width * 0.1),
        "Sürücü": int(total_width * 0.15),
        "Durum": int(total_width * 0.1),
    }

    # Sütun başlıklarını ayarlama ve genişliklerini atama
    for col, width in col_widths.items():
        tree.heading(col, text=col)
        tree.column(col, width=width)

    # Veriyi tabloya ekleme
    for key, value in device_data.items():
        id_class = f"{value['Bus']} / {value.get('Class', 'N/A')}"
        vendor = value.get("Vendor", "N/A")
        device = value.get("Device", "N/A")
        type_ = value.get("Type", "N/A")
        driver = value.get("Driver", "N/A")
        status = value.get("Status", "N/A")
        
        # "works" ve "detected" durumlarını Türkçeye çevirme
        if status == "works":
            display_status = "Çalışıyor"
        elif status == "detected":
            display_status = "Tespit Edildi"
        else:
            display_status = status

        # Satır eklerken renk belirleme
        row_color = set_row_color(status)
        tree.insert("", "end", values=(id_class, vendor, device, type_, driver, display_status), tags=(row_color,))

    # Satır rengini ayarlama
    tree.tag_configure("#A8E6A1", background="#A8E6A1")  # Yeşil
    tree.tag_configure("#A1D6E6", background="#A1D6E6")  # Mavi
    tree.tag_configure("#F2A1A1", background="#F2A1A1")  # Kırmızı

    # Treeview'i yerleştirme
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
