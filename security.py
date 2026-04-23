import streamlit as st
import pandas as pd
import requests

# URL Database dan Script kamu
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbwVq2GUVGrA3f9efmsUCeEsYNonQjdYAueHZNyt4bV__k99HSn5EG6YDPgOLhyAX3A7/exec"

def verify_user(email, password, key=None, mode="login"):
    try:
        # Membaca database secara real-time
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        
        if mode == "signup":
            # Cek apakah Kode Aktivasi ada dan belum punya pemilik (kolom Email kosong)
            if key in df['Key'].values:
                row = df[df['Key'] == key].iloc[0]
                # Anggap kolom B (index 1) adalah Email
                if pd.isna(row['Email']) or str(row['Email']).strip() == "":
                    # Kirim data pendaftaran ke Google Sheet
                    requests.get(f"{SCRIPT_URL}?key={key}&email={email}&pass={password}", timeout=10)
                    return "SUCCESS_SIGNUP"
                else:
                    return "KEY_ALREADY_USED"
            return "INVALID_KEY"
            
        elif mode == "login":
            # Mencari baris yang email dan password-nya cocok
            # Pastikan password di Sheet disimpan sebagai teks/string
            match = df[(df['Email'].astype(str) == str(email)) & (df['Password'].astype(str) == str(password))]
            if not match.empty:
                return "SUCCESS_LOGIN"
            return "WRONG_CREDENTIALS"
            
    except Exception as e:
        return f"ERROR: {str(e)}"
