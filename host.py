def load_host_data(file_path):
    """Host bilgilerini dosyadan yükler."""
    host_data = {}
    try:
        with open(file_path, 'r') as f:
            for line in f.readlines():
                key, value = line.strip().split(":", 1)
                host_data[key] = value.strip()
    except Exception as e:
        print(f"Host bilgileri yüklenirken hata oluştu: {e}")
    return host_data
