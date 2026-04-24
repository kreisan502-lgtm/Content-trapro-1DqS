import streamlit as st
from extra_streamlit_components import CookieManager
from auth_app import show_login_screen
from sidebar_app import show_sidebar
from dashboard_app import show_main_dashboard
from settings_app import show_settings
import time

st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# 1. Inisialisasi Cookie Manager
cookie_manager = CookieManager(key="main_auth_system")

# Berikan waktu sedikit agar cookie manager siap
time.sleep(0.1) 

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# --- 2. LOGIKA AUTO-LOGIN (DIPERBAIKI) ---
saved_email = cookie_manager.get("vip_user_email")
saved_nama = cookie_manager.get("vip_user_nama")
saved_ref = cookie_manager.get("vip_user_ref") # AMBIL JUGA REF-NYA

if saved_email and not st.session_state.authenticated:
    st.session_state.authenticated = True
    # Pastikan 'ref' masuk ke session agar profil tidak Error saat refresh
    st.session_state.user_data = {
        "nama": saved_nama, 
        "email": saved_email,
        "ref": saved_ref if saved_ref else "" 
    }
    st.session_state.page = "dashboard"

# --- 3. NAVIGASI ---
if not st.session_state.authenticated:
    show_login_screen(cookie_manager)
else:
    show_sidebar(cookie_manager)
    
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
