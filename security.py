import streamlit as st
import pandas as pd
import requests

# 1. Link CSV database kamu
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"

# 2. URL Web App Google Apps Script kamu
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx7l7Tn_ciHFOYUI17e7_kbGDUCXe5c4Uvmm4hEwBuWi9XQi4L8Q8yLaIJoUri6gOkL/exec"

def get_device_id():
    """Mengambil sidik jari unik browser user"""
    ua = st.context.headers.get("User-Agent", "unknown")
    return str(hash(ua))

def lock_device_to_sheet(key, device_id):
    """Mengirim perintah ke Google Script untuk mengisi kolom Device_ID"""
    try:
        # Mengirim data menggunakan metode GET ke Script Google
        requests.get(f"{SCRIPT_URL}?key={key}&device_id={device_id}", timeout=10)
    except Exception as e:
        st.error(f"Gagal Sinkronisasi Keamanan: {e}")

def verify_activation(input_key):
    """Logika utama pengecekan lisensi"""
    try:
        # Membaca database secara real-time
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        current_device = get_device_id()
        
        # Cari apakah kunci ada di database
        if input_key in df['Key'].values:
            row = df[df['Key'] == input_key].iloc[0]
            device_terdaftar = str(row['Device_ID']).strip()

            # JIKA DEVICE ID KOSONG (Belum pernah dipakai)
            if pd.isna(row['Device_ID']) or device_terdaftar == "nan" or device_terdaftar == "":
                # OTOMATIS: Isi kolom Device_ID di Google Sheet kamu
                lock_device_to_sheet(input_key, current_device)
                return {"status": "FIRST_TIME_LOCK", "device_id": current_device}
            
            # JIKA SUDAH ADA PEMILIKNYA, CEK APAKAH PERANGKATNYA SAMA
            if device_terdaftar == current_device:
                return {"status": "VALID"}
            else:
                return {"status": "LOCKED_OTHER_DEVICE"}
        
        return {"status": "INVALID_KEY"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)}
