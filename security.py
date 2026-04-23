import streamlit as st
import pandas as pd
import requests
import time

# URL Database Aktivasi (CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"

# URL Google Apps Script yang baru Anda berikan
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby0CzpBx5JCnUZNApcOqWCkZ0adGJkhPsbowmQX1fylV9fxQP2ETtWb-vZ6F3bnFpvF/exec"

def get_key_info(key):
    """Mengambil info Nama & Email berdasarkan Key untuk pendaftaran"""
    try:
        # Menambahkan timestamp agar data selalu fresh (anti-cache)
        df = pd.read_csv(f"{SHEET_CSV_URL}&t={int(time.time())}")
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
    except:
        return None

def verify_user(email, password, key=None, mode="login"):
    """Fungsi Login dan Signup"""
    try:
        # Tarik data terbaru
        df = pd.read_csv(f"{SHEET_CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        
        if mode == "login":
            # Login mencocokkan Email & password (E)
            match = df[(df['Email'].astype(str) == str(email)) & 
                       (df['password'].astype(str) == str(password))]
            
            if not match.empty:
                if str(match.iloc[0]['status']).upper() == "BLOKIR":
                    return "ACCOUNT_BLOCKED"
                return "SUCCESS_LOGIN"
            return "WRONG_CREDENTIALS"
            
        elif mode == "signup":
            # Kirim data ke Apps Script untuk aktivasi
            params = {"action": "signup", "key": key, "pass": password}
            res = requests.get(SCRIPT_URL, params=params, timeout=15)
            if res.text == "SUCCESS_REGISTER":
                return "SUCCESS_SIGNUP"
            return res.text
    except Exception as e:
        return f"ERROR: {str(e)}"
        
