import streamlit as st
import pandas as pd
import requests

# Link CSV dari Google Sheet kamu
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"

def get_device_id():
    # Mengambil ID unik perangkat/browser
    ua = st.context.headers.get("User-Agent", "unknown")
    return str(hash(ua))

def verify_activation(input_key):
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        current_device = get_device_id()
        
        # Bersihkan data
        df.columns = df.columns.str.strip()
        
        if input_key in df['Key'].values:
            row = df[df['Key'] == input_key].iloc[0]
            device_terdaftar = str(row['Device_ID']).strip()

            # JIKA DEVICE ID MASIH KOSONG (User Pertama)
            if pd.isna(row['Device_ID']) or device_terdaftar == "nan" or device_terdaftar == "":
                return {"status": "FIRST_TIME_LOCK", "device_id": current_device}
            
            # JIKA DEVICE ID SUDAH ADA, CEK COCOK ATAU TIDAK
            if device_terdaftar == current_device:
                return {"status": "VALID"}
            else:
                return {"status": "LOCKED_OTHER_DEVICE"}
        
        return {"status": "INVALID_KEY"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)}
