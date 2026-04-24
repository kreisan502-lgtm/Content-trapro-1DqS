import streamlit as st
from extra_streamlit_components import CookieManager
import time

# Pastikan ini di baris paling atas
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# 1. Inisialisasi Cookie Manager dengan key unik
cookie_manager = CookieManager(key="main_auth_system")

# PENTING: Kasih jeda sedikit lebih lama (0.5 detik) agar browser sempat kirim cookie
time.sleep(0.5) 

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 2. LOGIKA AUTO-LOGIN YANG LEBIH KUAT ---
# Ambil data dari cookie
saved_email = cookie_manager.get("vip_user_email")
saved_nama = cookie_manager.get("vip_user_nama")
saved_ref = cookie_manager.get("vip_user_ref")

# Cek apakah cookie ada DAN session sedang kosong (akibat refresh)
if saved_email and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_data = {
        "nama": saved_nama, 
        "email": saved_email,
        "ref": saved_ref if saved_ref else "" 
    }
    # Jangan paksa pindah ke dashboard jika user sedang di halaman lain
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"
