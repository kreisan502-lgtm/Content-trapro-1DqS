import pandas as pd
import requests
import time
from config import CSV_URL, SCRIPT_URL

def get_key_info(key):
    """Mengambil informasi detail License Key dari Google Sheets"""
    try:
        # Cache busting menggunakan timestamp agar data selalu fresh
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

# Ganti fungsi verify_user di security.py kamu menjadi ini:
def verify_user(email, password, key=None, mode="login", nama=None, ref=None):
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
                    "ref": str(match.iloc[0].iloc[0]) # Mengambil Kolom A (Ref) saat login
                }
            return {"status": "FAILED"}
        
        elif mode == "signup":
            params = {
                "action": "signup", 
                "ref": ref,       # INI KUNCINYA: Mengirimkan Ref ke Apps Script
                "key": key, 
                "pass": password, 
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
