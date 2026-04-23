import streamlit as st
import pandas as pd
import requests

# Link database CSV (Pastikan GID benar atau gunakan link pub terbaru)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTECVdfx3hAE8TrL_bUeSdtNx_LTe4o3UpTwOnRDarMkU9kgzOV_dSbZLPE2snpjGY4QQVjQgMCxHoJ/pub?output=csv"
# Link Script URL yang tadi (AKfycbyvbCjYd0LVMR3u1_...)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycby7lq0P6hhr6W1BcLhAxhvlr5P58WQF0eA1T8SypxespoTLT3WkZg_Z3uGIof5zZ4p1/exec"

def verify_user(email, password, key=None, pin=None, mode="login"):
    try:
        # Load database secara real-time
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip() # Bersihkan spasi di nama kolom
        
        # Penyesuaian Nama Kolom berdasarkan data LYNK + Tambahan kamu:
        # 'Buyer Email' (Kolom Q), 'Key' (Kolom AA), 'Password' (Kolom AB), 'PIN' (Kolom AC), 'Status Key' (Kolom AD)

        if mode == "signup":
            # 1. Cek apakah Key ada di database
            if key in df['Key'].values:
                row = df[df['Key'] == key].iloc[0]
                
                # 2. Cek apakah Statusnya masih AKTIF (belum terpakai)
                if str(row['Status Key']).upper() == "AKTIF":
                    # Kirim data pendaftaran ke Google Apps Script
                    params = {
                        "action": "signup",
                        "key": key,
                        "pass": password,
                        "pin": pin
                    }
                    res = requests.get(SCRIPT_URL, params=params, timeout=10)
                    
                    if res.text == "SUCCESS_REGISTER":
                        return "SUCCESS_SIGNUP"
                    else:
                        return f"FAILED_APPSCRIPT: {res.text}"
                
                return "KEY_ALREADY_USED" # Jika status bukan AKTIF
            return "INVALID_KEY"
            
        elif mode == "login":
            # Login mencocokkan Buyer Email (Kolom Q) dan Password (Kolom AB)
            # Sesuaikan nama kolom jika di CSV-mu berbeda
            match = df[(df['Buyer Email'].astype(str) == str(email)) & 
                       (df['Password'].astype(str) == str(password))]
            
            if not match.empty:
                # Tambahan: Cek status apakah diblokir atau tidak
                if match.iloc[0]['Status Key'] == "BLOKIR":
                    return "ACCOUNT_BLOCKED"
                return "SUCCESS_LOGIN"
            else:
                return "WRONG_CREDENTIALS"
            
    except Exception as e:
        return f"ERROR: {str(e)}"

def reset_password(email, key, pin, new_password):
    try:
        # Sesuai logika update pass (pastikan di AppScript sudah ada action ini)
        params = {
            "action": "update_pass",
            "key": key,
            "email": email,
            "pin": pin,
            "pass": new_password
        }
        res = requests.get(SCRIPT_URL, params=params, timeout=10)
        
        if "SUCCESS" in res.text:
            return "SUCCESS"
        return "FAILED"
    except:
        return "ERROR"
