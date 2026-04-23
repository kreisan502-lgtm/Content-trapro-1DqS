import pandas as pd
import requests
import time

# URL Anda tetap sama
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbxohqgxxasTpUpdgPPzu2TLrftc6JYdQ51u51CsMt6-TLAjXhIHTNKHB4RHHtW2_6fR/exec"

def get_key_info(key):
    try:
        # Cache busting agar data selalu paling baru dari server Google
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        # Pencarian key secara akurat (case-sensitive)
        match = df[df['Key'].astype(str) == str(key)]
        
        if not match.empty:
            row = match.iloc[0]
            # Logika Utama: Cek apakah kolom password benar-benar kosong
            # Kita anggap kosong jika nilainya NaN, string kosong, atau spasi
            raw_pass = str(row.get('password', ''))
            is_empty_pass = pd.isna(row.get('password')) or raw_pass.strip() == "" or raw_pass == "nan"
            
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
        if mode == "login":
            df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
            df.columns = df.columns.str.strip()
            # Validasi Login: Email dan Password harus cocok presisi
            match = df[(df['Email'].astype(str) == str(email)) & (df['password'].astype(str) == str(password))]
            return "SUCCESS_LOGIN" if not match.empty else "FAILED"
        
        elif mode == "signup":
            # Mode ini juga digunakan untuk EDIT/RESET SANDI karena sistem menimpa data berdasarkan Key
            params = {"action": "signup", "key": key, "pass": password}
            res = requests.get(SCRIPT_URL, params=params, timeout=15)
            return "SUCCESS_SIGNUP" if res.text == "SUCCESS_REGISTER" else "FAILED"
    except:
        return "ERROR"
        
