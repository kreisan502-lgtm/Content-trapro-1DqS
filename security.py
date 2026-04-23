import streamlit as st
import pandas as pd
import requests
import uuid

# URL tetap sama
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbx7l7Tn_ciHFOYUI17e7_kbGDUCXe5c4Uvmm4hEwBuWi9XQi4L8Q8yLaIJoUri6gOkL/exec"

def get_device_id():
    """Membuat ID unik permanen yang disimpan di session browser"""
    if 'unique_browser_id' not in st.session_state:
        # Membuat ID acak yang sangat panjang sehingga tidak mungkin sama
        st.session_state.unique_browser_id = str(uuid.uuid4())
    return st.session_state.unique_browser_id

def lock_device_to_sheet(key, device_id):
    try:
        requests.get(f"{SCRIPT_URL}?key={key}&device_id={device_id}", timeout=10)
    except:
        pass

def verify_activation(input_key):
    try:
        df = pd.read_csv(SHEET_CSV_URL)
        df.columns = df.columns.str.strip()
        
        # Ambil ID unik yang dibuat khusus untuk browser ini
        current_device = get_device_id()
        
        if input_key in df['Key'].values:
            row = df[df['Key'] == input_key].iloc[0]
            device_terdaftar = str(row['Device_ID']).strip()

            # JIKA KOSONG (User Pertama)
            if pd.isna(row['Device_ID']) or device_terdaftar in ["nan", "", "None"]:
                lock_device_to_sheet(input_key, current_device)
                return {"status": "FIRST_TIME_LOCK", "device_id": current_device}
            
            # JIKA SUDAH ADA, CEK COCOK ATAU TIDAK
            if device_terdaftar == current_device:
                return {"status": "VALID"}
            else:
                return {"status": "LOCKED_OTHER_DEVICE"}
        
        return {"status": "INVALID_KEY"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)}
