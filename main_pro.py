import streamlit as st
from extra_streamlit_components import CookieManager
import time

# 1. WAJIB DI BARIS PERTAMA
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# 2. Inisialisasi Cookie Manager
# Tambahkan 'key' yang unik agar tidak bentrok
cookie_manager = CookieManager(key="vip_suite_auth")

# 3. PROTEKSI ANTI-BLANK (Kuncinya di sini)
# Berikan waktu jeda agar browser siap. Jika blank, Streamlit akan menunggu.
if not cookie_manager:
    st.info("Sedang menyiapkan sistem keamanan...")
    st.stop()

# Tambahkan sedikit delay agar cookie terbaca sempurna
time.sleep(0.4) 

# 4. Inisialisasi Session State
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None

# --- 5. LOGIKA AUTO-LOGIN ---
# Kita ambil data dari cookie browser
saved_email = cookie_manager.get("vip_user_email")
saved_nama = cookie_manager.get("vip_user_nama")
saved_ref = cookie_manager.get("vip_user_ref")

# Jika di session kosong (habis refresh) tapi di browser ada datanya
if saved_email and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_data = {
        "nama": saved_nama,
        "email": saved_email,
        "ref": saved_ref if saved_ref else ""
    }
    if 'page' not in st.session_state:
        st.session_state.page = "dashboard"

# --- 6. NAVIGASI UTAMA ---
from auth_app import show_login_screen
from sidebar_app import show_sidebar
from dashboard_app import show_main_dashboard
from settings_app import show_settings

if not st.session_state.authenticated:
    # Kirim cookie_manager ke halaman login
    show_login_screen(cookie_manager)
else:
    # Tampilkan Sidebar
    show_sidebar(cookie_manager)
    
    # Cek halaman mana yang aktif
    current_page = st.session_state.get('page', 'dashboard')
    
    if current_page == "dashboard":
        show_main_dashboard()
    elif current_page == "settings":
        show_settings()
    # Tambahkan halaman lain jika ada...
    
