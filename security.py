import streamlit as st
import pandas as pd

# Link database yang baru saja kamu buat
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTyzO1OA-Cq8Tabx9KODOX9VWNFTZ0Gluuja8qztT30GR7c2FbPoJLBs_F1h8KRtRYnW6SRbKM1jpu1/pub?gid=0&single=true&output=csv"

def get_device_id():
    # Mengambil identitas unik browser pembeli
    user_agent = st.context.headers.get("User-Agent", "unknown")
    # Mengubahnya menjadi angka unik agar tidak bisa dipalsukan
    return str(hash(user_agent))

def verify_activation(input_key):
    try:
        # Membaca data dari Google Sheets secara real-time
        df = pd.read_csv(SHEET_CSV_URL)
        current_device = get_device_id()
        
        # 1. Cek apakah Kode Aktivasi ada di kolom 'Key'
        if input_key in df['Key'].values:
            row = df[df['Key'] == input_key].iloc[0]
            
            # 2. Jika status masih 'Tersedia', berarti ini aktivasi pertama
            if str(row['Status']).strip().lower() == 'tersedia':
                return {"status": "REGISTER_NEW", "device_id": current_device}
            
            # 3. Jika status sudah 'Aktif', cek apakah perangkatnya sama
            elif str(row['Status']).strip().lower() == 'aktif':
                if str(row['Device_ID']).strip() == current_device:
                    return {"status": "VALID"}
                else:
                    return {"status": "LOCKED_OTHER_DEVICE"}
                    
        return {"status": "INVALID_KEY"}
    except Exception as e:
        return {"status": "ERROR", "msg": str(e)}
      
