import pandas as pd
import requests
import time

# URL Database & Apps Script Anda
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxohqgxxasTpUpdgPPzu2TLrftc6JYdQ51u51CsMt6-TLAjXhIHTNKHB4RHHtW2_6fR/exec"

def get_key_info(key):
    try:
        # Cache busting agar data selalu paling baru dari server Google
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        # Pencarian key secara akurat
        match = df[df['Key'].astype(str) == str(key)]
        
        if not match.empty:
            row = match.iloc[0]
            # Cek apakah kolom password kosong
            raw_pass = str(row.get('password', ''))
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
        # Load Data
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        if mode == "login":
            # Cari baris yang Email & Password-nya cocok
            match = df[(df['Email'].astype(str) == str(email)) & (df['password'].astype(str) == str(password))]
            if not match.empty:
                # Mengembalikan data lengkap untuk Sidebar Pro
                return {
                    "status": "SUCCESS", 
                    "nama": match.iloc[0]['Nama'], 
                    "email": str(match.iloc[0]['Email'])
                }
            return {"status": "FAILED"}
        
        elif mode == "signup":
            # Kirim data ke Apps Script (Daftar Baru / Reset Sandi)
            params = {"action": "signup", "key": key, "pass": password}
            res = requests.get(SCRIPT_URL, params=params, timeout=15)
            # Pastikan Apps Script mengembalikan teks "SUCCESS_REGISTER"
            if res.text == "SUCCESS_REGISTER":
                return "SUCCESS_SIGNUP"
            else:
                return "FAILED"
                
    except Exception as e:
        return f"ERROR: {str(e)}"
