import pandas as pd
import requests
import time
from config import CSV_URL, SCRIPT_URL

def get_key_info(key):
    """Mengambil informasi detail License Key dari Google Sheets"""
    try:
        # Cache busting menggunakan timestamp agar data tidak kadaluarsa
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        match = df[df['Key'].astype(str) == str(key)]
        
        if not match.empty:
            row = match.iloc[0]
            raw_pass = str(row.get('password', ''))
            # Cek apakah kolom password di sheet benar-benar kosong
            is_empty_pass = pd.isna(row.get('password')) or raw_pass.strip() == "" or raw_pass.lower() == "nan"
            
            return {
                "status": row['status'],
                "email": row['Email'],
                "nama": row['Nama'],
                "can_register": row['status'] == "AKTIF" and is_empty_pass,
                "is_registered": not is_empty_pass
            }
    except Exception as e:
        return None

def verify_user(email, password, key=None, mode="login", nama=None):
    """
    Fungsi Utama Autentikasi:
    - mode 'login': Verifikasi Email & Password
    - mode 'signup': Registrasi Baru atau Update Profil (Nama/Email/Pass)
    """
    try:
        # Load Data dari CSV Google Sheets
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        if mode == "login":
            # Mencari kecocokan Email dan Password secara case-sensitive
            match = df[(df['Email'].astype(str) == str(email)) & (df['password'].astype(str) == str(password))]
            if not match.empty:
                return {
                    "status": "SUCCESS", 
                    "nama": match.iloc[0]['Nama'], 
                    "email": str(match.iloc[0]['Email'])
                }
            return {"status": "FAILED"}
        
        elif mode == "signup":
            # Menyiapkan parameter untuk dikirim ke Google Apps Script
            # Parameter 'nama' ditambahkan agar Google Sheets bisa update Nama
            params = {
                "action": "signup", 
                "key": key, 
                "pass": password, # Berisi "" jika tidak ingin ubah sandi
                "email": email,   # Email baru/lama
                "nama": nama      # Nama baru/lama
            }
            
            # Melakukan request ke Web App Google Apps Script
            res = requests.get(SCRIPT_URL, params=params, timeout=15)
            
            # Jika respon dari Apps Script mengandung kata "SUCCESS"
            if "SUCCESS" in res.text.upper():
                return "SUCCESS_SIGNUP"
            else:
                return "FAILED"
                
    except Exception as e:
        return f"ERROR: {str(e)}"
        
