import json

def load_device_data(file_path):
    """Donanım bilgilerini JSON dosyasından yükler."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Donanım bilgileri yüklenirken hata oluştu: {e}")
        return {}
