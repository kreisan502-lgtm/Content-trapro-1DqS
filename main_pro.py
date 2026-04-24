import streamlit as st
from extra_streamlit_components import CookieManager
import time

# 1. Konfigurasi Awal
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# 2. Inisialisasi Cookie
cookie_manager = CookieManager(key="main_auth_system")
time.sleep(0.6) # Jeda wajib agar cookie terbaca

# 3. State Management
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 4. PEMULIHAN SESI DARI COOKIE ---
if not st.session_state.authenticated:
    saved_email = cookie_manager.get("vip_user_email")
    saved_nama = cookie_manager.get("vip_user_nama")
    saved_ref = cookie_manager.get("vip_user_ref")
    
    if saved_email:
        st.session_state.authenticated = True
        st.session_state.user_data = {
            "nama": saved_nama,
            "email": saved_email,
            "ref": saved_ref if saved_ref else ""
        }

# --- 5. LOGIKA NAVIGASI (HANYA BOLEH ADA SATU) ---
from auth_app import show_login_screen
from sidebar_app import show_sidebar
from dashboard_app import show_main_dashboard
from settings_app import show_settings

if not st.session_state.authenticated:
    # PASTIKAN BARIS INI HANYA ADA SATU DI SELURUH MAIN.PY
    show_login_screen(cookie_manager)
else:
    # Tampilkan Sidebar
    show_sidebar(cookie_manager)
    
    # Navigasi Halaman
    page = st.session_state.get('page', 'dashboard')
    
    if page == "dashboard":
        show_main_dashboard()
    elif page == "settings":
        show_settings()
    elif page == "investasi":
        from investasi import show_investasi
        show_investasi()
    elif page == "hpp":
        from kalkulator import show_hpp
        show_hpp()
