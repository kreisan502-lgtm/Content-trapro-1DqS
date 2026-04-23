import requests

def lock_device_to_sheet(key, device_id):
    # Ganti dengan URL Web App baru yang kamu dapatkan setelah Deploy
    SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx7l7Tn_ciHFOYUI17e7_kbGDUCXe5c4Uvmm4hEwBuWi9XQi4L8Q8yLaIJoUri6gOkL/exec"
    try:
        # Mengirim data secara diam-diam ke Google Sheet
        requests.get(f"{SCRIPT_URL}?key={key}&device_id={device_id}")
    except Exception as e:
        print(f"Gagal sinkronisasi: {e}")
