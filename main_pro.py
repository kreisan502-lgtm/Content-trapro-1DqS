import streamlit as st
import time
from extra_streamlit_components import CookieManager

# 1. WAJIB DI BARIS PERTAMA
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# 2. Inisialisasi Cookie Manager
cookie_manager = CookieManager(key="main_auth_system")

# PENTING: Jeda agar Cookie Manager tidak blank
# Jika masih blank, naikkan ke 0.8 atau 1.0
time.sleep(0.6) 

# 3. Inisialisasi State Awal
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# --- 4. LOGIKA PEMULIHAN SESI (ANTI RESET) ---
saved_email = cookie_manager.get("vip_user_email")
saved_nama = cookie_manager.get("vip_user_nama")
saved_ref = cookie_manager.get("vip_user_ref")

if saved_email and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_data = {
        "nama": saved_nama,
        "email": saved_email,
        "ref": saved_ref if saved_ref else ""
    }
    # Pastikan default page adalah dashboard jika baru pulih
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"

# --- 5. IMPORT HALAMAN (Di bawah agar tidak bentrok) ---
from auth_app import show_login_screen
from sidebar_app import show_sidebar
from dashboard_app import show_main_dashboard
from settings_app import show_settings

# --- 6. NAVIGASI UTAMA ---
if not st.session_state.authenticated:
    show_login_screen(cookie_manager)
else:
    # Tampilkan Sidebar (Pastikan sidebar_app kamu menerima cookie_manager)
    show_sidebar(cookie_manager)
    
    # Ambil halaman aktif dari session
    page = st.session_state.get('page', 'dashboard')
    
    # Logika Percabangan Menu agar tidak Blank
    if page == "dashboard":
        show_main_dashboard()
    elif page == "settings":
        show_settings()
    elif page == "investasi":
        # Import lokal di dalam fungsi agar tidak berat di awal
        from investasi import show_investasi
        show_investasi()
    elif page == "hpp":
        # Import lokal untuk kalkulator HPP
        from kalkulator import show_hpp
        show_hpp()
        
