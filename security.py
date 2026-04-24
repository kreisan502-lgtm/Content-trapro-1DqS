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

def verify_user(email, password, key=None, mode="login", nama=None, ref=None):
    """
    Fungsi Autentikasi dengan dukungan Kode Ref (Kolom A)
    """
    try:
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        if mode == "login":
            # Mencari kecocokan Email & Password
            match = df[(df['Email'].astype(str) == str(email)) & (df['password'].astype(str) == str(password))]
            if not match.empty:
                return {
                    "status": "SUCCESS", 
                    "nama": match.iloc[0]['Nama'], 
                    "email": str(match.iloc[0]['Email']),
                    "ref": str(match.iloc[0].iloc[0]) # AMBIL KOLOM A (Ref) SEBAGAI KUNCI
                }
            return {"status": "FAILED"}
        
        elif mode == "signup":
            # Parameter dikirim ke Apps Script
            params = {
                "action": "signup", 
                "ref": ref,       # Kirim kunci baris
                "key": key, 
                "pass": password, 
                "email": email,   
                "nama": nama      
            }
            res = requests.get(SCRIPT_URL, params=params, timeout=15)
            return "SUCCESS_SIGNUP" if "SUCCESS" in res.text.upper() else "FAILED"
                
    except Exception as e:
        return f"ERROR: {str(e)}"
        
