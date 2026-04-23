import pandas as pd
import requests
import time

# URL Database Anda (JANGAN DIUBAH)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby0CzpBx5JCnUZNApcOqWCkZ0adGJkhPsbowmQX1fylV9fxQP2ETtWb-vZ6F3bnFpvF/exec"

def get_key_info(key):
    try:
        df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
        df.columns = df.columns.str.strip()
        match = df[df['Key'].astype(str) == str(key)]
        if not match.empty:
            return {
                "status": match.iloc[0]['status'], 
                "email": match.iloc[0]['Email'], 
                "nama": match.iloc[0]['Nama']
            }
    except: return None

def verify_user(email, password, key=None, mode="login"):
    try:
        if mode == "login":
            df = pd.read_csv(f"{CSV_URL}&t={int(time.time())}")
            df.columns = df.columns.str.strip()
            # Cek Email dan Password di database
            match = df[(df['Email'].astype(str) == str(email)) & (df['Password'].astype(str) == str(password))]
            return "SUCCESS_LOGIN" if not match.empty else "FAILED"
        
        elif mode == "signup":
            # Kirim data ke Google Apps Script untuk update password
            payload = {"email": email, "password": password, "key": key}
            resp = requests.post(SCRIPT_URL, json=payload)
            return "SUCCESS_SIGNUP" if resp.status_code == 200 else "FAILED"
    except:
        return "ERROR"
        
