import pandas as pd
import requests
import time
from config import CSV_URL, SCRIPT_URL  # Memanggil URL dari file config

def get_key_info(key):
    try:
        # Mengambil data terbaru dari Google Sheets (CSV)
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        match = df[df['Key'].astype(str) == str(key)]
        
        if not match.empty:
            row = match.iloc[0]
            raw_pass = str(row.get('password', ''))
            # Cek apakah user sudah punya password atau belum
            is_empty_pass = pd.isna(row.get('password')) or raw_pass.strip() == "" or raw_pass.lower() == "nan"
            
            return {
                "status": row['status'],
                "email": row['Email'],
                "nama": row['Nama'],
                "can_register": row['status'] == "AKTIF" and is_empty_pass,
                "is_registered": not is_empty_pass
            }
    except:
        return None

def verify_user(email, password, key=None, mode="login"):
    try:
        # Load Data CSV untuk pengecekan login
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        if mode == "login":
            match = df[(df['Email'].astype(str) == str(email)) & (df['password'].astype(str) == str(password))]
            if not match.empty:
                return {
                    "status": "SUCCESS", 
                    "nama": match.iloc[0]['Nama'], 
                    "email": str(match.iloc[0]['Email'])
                }
            return {"status": "FAILED"}
        
        elif mode == "signup":
            # Kirim data ke Apps Script untuk Registrasi atau Update Profil
            # 'pass' akan berisi "" jika user tidak merubah password di Settings
            params = {
                "action": "signup", 
                "key": key, 
                "pass": password,
                "email": email  # Menambahkan email jika Apps Script perlu update email
            }
            
            res = requests.get(SCRIPT_URL, params=params, timeout=15)
            
            # Jika Apps Script berhasil melakukan update/register
            if "SUCCESS" in res.text:
                return "SUCCESS_SIGNUP"
            else:
                return "FAILED"
                
    except Exception as e:
        return f"ERROR: {str(e)}"
        
