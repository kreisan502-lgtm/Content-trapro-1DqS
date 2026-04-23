import streamlit as st
import pandas as pd
import requests

# Database 2 (Aktivasi)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pubhtml"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby0CzpBx5JCnUZNApcOqWCkZ0adGJkhPsbowmQX1fylV9fxQP2ETtWb-vZ6F3bnFpvF/exec"

def get_key_info(key):
    """Fungsi untuk mengambil Nama & Email berdasarkan Key sebelum daftar"""
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        match = df[df['Key'] == key]
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
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        
        if mode == "login":
            match = df[(df['Email'].astype(str) == str(email)) & 
                       (df['password'].astype(str) == str(password))]
            if not match.empty:
                if match.iloc[0]['status'] == "BLOKIR": return "ACCOUNT_BLOCKED"
                return "SUCCESS_LOGIN"
            return "WRONG_CREDENTIALS"
            
        elif mode == "signup":
            params = {"action": "signup", "key": key, "pass": password}
            res = requests.get(SCRIPT_URL, params=params, timeout=10)
            return "SUCCESS_SIGNUP" if res.text == "SUCCESS_REGISTER" else res.text
    except Exception as e:
        return f"ERROR: {str(e)}"
        
