import streamlit as st
import pandas as pd
import requests

# Link database dan Script terbaru
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbySfA_VE3XMlz3eyCA5NXnkAjVtIJeoX3qoF0dRw6TuNCrqR1KXwV7qTfSde-Y2I-Af/exec"

def verify_user(email, password, key=None, pin=None, mode="login"):
    try:
        # Load database secara real-time
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        
        if mode == "signup":
            if key in df['Key'].values:
                row = df[df['Key'] == key].iloc[0]
                if pd.isna(row['Email']) or str(row['Email']).strip() == "":
                    # Kirim data pendaftaran ke Script
                    url = f"{SCRIPT_URL}?action=signup&key={key}&email={email}&pass={password}&pin={pin}"
                    requests.get(url, timeout=10)
                    return "SUCCESS_SIGNUP"
                return "KEY_ALREADY_USED"
            return "INVALID_KEY"
            
        elif mode == "login":
            # Cek kecocokan Email dan Password di kolom B dan C
            match = df[(df['Email'].astype(str) == str(email)) & (df['Password'].astype(str) == str(password))]
            return "SUCCESS_LOGIN" if not match.empty else "WRONG_CREDENTIALS"
            
    except Exception as e:
        return f"ERROR: {str(e)}"

def reset_password(email, key, pin, new_password):
    try:
        url = f"{SCRIPT_URL}?action=update_pass&key={key}&email={email}&pin={pin}&pass={new_password}"
        res = requests.get(url, timeout=10)
        if res.text == "SUCCESS_UPDATE":
            return "SUCCESS"
        elif res.text == "WRONG_CONFIRMATION":
            return "WRONG_PIN"
        return "FAILED"
    except:
        return "ERROR"
        
