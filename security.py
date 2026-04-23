import streamlit as st
import pandas as pd
import requests

# URL Database 2 (Aktivasi) yang sudah di-publish ke Web (Format CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"

# URL Google Apps Script terbaru Anda
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby0CzpBx5JCnUZNApcOqWCkZ0adGJkhPsbowmQX1fylV9fxQP2ETtWb-vZ6F3bnFpvF/exec"

def get_key_info(key):
    """Mencari data Nama & Email di Database Aktivasi berdasarkan Key"""
    try:
        # Menambahkan parameter waktu agar pandas tidak mengambil data cache (selalu terbaru)
        df = pd.read_csv(f"{SHEET_CSV_URL}&cache={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        match = df[df['Key'].astype(str) == str(key)]
        if not match.empty:
            row = match.iloc[0]
            return {
                "status": row['status'],
                "email": row['Email'],
                "nama": row['Nama']
            }
        return None
    except Exception as e:
        return None

def verify_user(email, password, key=None, mode="login"):
    """Fungsi utama untuk Login dan Registrasi"""
    try:
        # Muat ulang data terbaru
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        
        if mode == "login":
            # Login: Mencocokkan Email (Kolom C) & password (Kolom E)
            match = df[(df['Email'].astype(str) == str(email)) & 
                       (df['password'].astype(str) == str(password))]
            
            if not match.empty:
                status_user = str(match.iloc[0]['status']).upper()
                if status_user == "BLOKIR":
                    return "ACCOUNT_BLOCKED"
                return "SUCCESS_LOGIN"
            return "WRONG_CREDENTIALS"
            
        elif mode == "signup":
            # Signup: Kirim perintah ke Apps Script untuk update Password di Sheets
            params = {
                "action": "signup",
                "key": key,
                "pass": password
            }
            res = requests.get(SCRIPT_URL, params=params, timeout=15)
            if res.text == "SUCCESS_REGISTER":
                return "SUCCESS_SIGNUP"
            return res.text
            
    except Exception as e:
        return f"ERROR_SYSTEM: {str(e)}"
