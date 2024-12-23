import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk


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
    root.title("Donanım Bilgisi Görüntüleme")
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    # Ana container frame oluştur
    main_frame = ttk.Frame(root)
    main_frame.grid(row=0, column=0, sticky="nsew")

    # Pencere yeniden boyutlandığında esneklik sağlama
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)

    # Sol ve sağ alanlar için iki alt frame
    left_frame = ttk.Frame(main_frame, padding=10)
    left_frame.grid(row=0, column=0, sticky="nsew")
    right_frame = ttk.Frame(main_frame, padding=10)
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Sol ve sağ frame'lerin genişlik ve yükseklik oranlarını ayarla
    main_frame.columnconfigure(0, weight=1)  # Sol alan genişliği
    main_frame.columnconfigure(1, weight=2)  # Sağ alan genişliği
    main_frame.rowconfigure(0, weight=1)

    # Sol kısımda bilgi alanı
    ttk.Label(left_frame, text=f"{host_data.get('vendor', 'N/A')} {host_data.get('model', 'N/A')}", font=("Arial", 14, "bold")).pack(anchor="w", pady=5)
    ttk.Label(left_frame, text=f"Test Edilen Sürüm: {host_data.get('system', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    ttk.Label(left_frame, text=f"Mimari: {host_data.get('arch', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    ttk.Label(left_frame, text=f"Kernel: {host_data.get('kernel', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    ttk.Label(left_frame, text=f"Marka: {host_data.get('vendor', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    ttk.Label(left_frame, text=f"Model: {host_data.get('model', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    ttk.Label(left_frame, text=f"Yıl: {host_data.get('year', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    ttk.Label(left_frame, text=f"Tür: {host_data.get('type', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    ttk.Label(left_frame, text=f"Dil: {host_data.get('lang', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)
    ttk.Label(left_frame, text=f"Dosya Sistemi: {host_data.get('filesystem', 'N/A')}", font=("Arial", 10)).pack(anchor="w", pady=2)

    # Pardus/Linux uyumluluğunu kontrol et ve göster
    system = host_data.get('system', '').lower()
    if "pardus" in system or "linux" in system:
        try:
            pardus_image = Image.open("assets/pardus.png")
            pardus_image = pardus_image.resize((100, 100), Image.Resampling.LANCZOS)
            pardus_photo = ImageTk.PhotoImage(pardus_image)
            img_label = ttk.Label(left_frame, image=pardus_photo)
            img_label.image = pardus_photo
            img_label.pack(side=tk.BOTTOM, pady=10)
            ttk.Label(left_frame, text="Bu cihaz Pardus/Linux Uyumludur", font=("Arial", 10, "bold")).pack(side=tk.BOTTOM, pady=5)
        except Exception as e:
            print(f"Pardus resmi yüklenirken hata: {e}")

    # Sağ kısımda Treeview (tablo) alanı
    tree = ttk.Treeview(right_frame, columns=("ID/Sınıf", "Üretici", "Cihaz", "Tür", "Sürücü", "Durum"), show="headings")

    # Sütun başlıklarını ayarla
    for col in ("ID/Sınıf", "Üretici", "Cihaz", "Tür", "Sürücü", "Durum"):
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=120)

    # Veriyi tabloya ekle
    for key, value in device_data.items():
        id_class = f"{value['Bus']} / {value.get('Class', 'N/A')}"
        vendor = value.get("Vendor", "N/A")
        device = value.get("Device", "N/A")
        type_ = value.get("Type", "N/A")
        driver = value.get("Driver", "N/A")
        status = value.get("Status", "N/A")
        
        display_status = "Çalışıyor" if status == "works" else "Tespit Edildi" if status == "detected" else status
        row_color = set_row_color(status)
        tree.insert("", "end", values=(id_class, vendor, device, type_, driver, display_status), tags=(row_color,))

    # Satır rengini ayarla
    tree.tag_configure("#A8E6A1", background="#A8E6A1")  # Yeşil
    tree.tag_configure("#A1D6E6", background="#A1D6E6")  # Mavi
    tree.tag_configure("#F2A1A1", background="#F2A1A1")  # Kırmızı

    # Treeview yerleştir ve scroll ekle
    tree.grid(row=0, column=0, sticky="nsew")
    right_frame.rowconfigure(0, weight=1)
    right_frame.columnconfigure(0, weight=1)

    scroll_y = ttk.Scrollbar(right_frame, orient="vertical", command=tree.yview)
    scroll_x = ttk.Scrollbar(right_frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

    scroll_y.grid(row=0, column=1, sticky="ns")
    scroll_x.grid(row=1, column=0, sticky="ew")
