import pandas as pd
import requests
import time
from config import CSV_URL, SCRIPT_URL

def get_key_info(key):
    """Mengambil informasi detail License Key dari Google Sheets"""
    try:
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        match = df[df['Key'].astype(str) == str(key)]
        
        if not match.empty:
            row = match.iloc[0]
            raw_pass = str(row.get('password', ''))
            is_empty_pass = pd.isna(row.get('password')) or raw_pass.strip() == "" or raw_pass.lower() == "nan"
            
            return {
                "status": row['status'],
                "email": row['Email'],
                "nama": row['Nama'],
                "can_register": row['status'] == "AKTIF" and is_empty_pass,
                "is_registered": not is_empty_pass
            }
    except Exception:
        return None

# PERBAIKAN: Menambahkan parameter ref=None
def verify_user(email, password, key=None, mode="login", nama=None, ref=None):
    """
    Fungsi Utama Autentikasi dengan Dukungan Kunci Reff (Kolom A)
    """
    try:
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        if mode == "login":
            match = df[(df['Email'].astype(str) == str(email)) & (df['password'].astype(str) == str(password))]
            if not match.empty:
                return {
                    "status": "SUCCESS", 
                    "nama": match.iloc[0]['Nama'], 
                    "email": str(match.iloc[0]['Email']),
                    "ref": str(match.iloc[0].iloc[0]) # Mengambil Kolom A (Reff)
                }
            return {"status": "FAILED"}
        
        elif mode == "signup":
            # Menyiapkan parameter untuk dikirim ke Google Apps Script
            params = {
                "action": "signup", 
                "ref": ref,       # KUNCI UTAMA: Mengirim Ref agar tidak salah baris
                "key": key, 
                "pass": password, # Kosong jika tidak ganti sandi
                "email": email,   
                "nama": nama      
            }
            
            res = requests.get(SCRIPT_URL, params=params, timeout=15)
            
            if "SUCCESS" in res.text.upper():
                return "SUCCESS_SIGNUP"
            else:
                return "FAILED"
                
    except Exception as e:
        return f"ERROR: {str(e)}"
                    
