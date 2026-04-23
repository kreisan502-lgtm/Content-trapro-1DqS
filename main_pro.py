import streamlit as st
from extra_streamlit_components import CookieManager
from auth_app import show_login_screen
from sidebar_app import show_sidebar
from dashboard_app import show_main_dashboard

# --- CONFIG (WAJIB PALING ATAS) ---
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# --- INISIALISASI SISTEM ---
cookie_manager = CookieManager(key="main_auth_system")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Cek Cookie Otomatis
saved_email = cookie_manager.get("vip_user_email")
saved_nama = cookie_manager.get("vip_user_nama")

if saved_email and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_data = {"nama": saved_nama, "email": saved_email}
    st.session_state.page = "dashboard"

# --- LOGIKA PEMANGGILAN ---
if not st.session_state.authenticated:
    show_login_screen(cookie_manager)
else:
    # Panggil Sidebar dari file terpisah
    show_sidebar(cookie_manager)
    
    # Panggil Dashboard atau Halaman Modul
    if st.session_state.get('page') == "dashboard" or 'page' not in st.session_state:
        show_main_dashboard()
    elif st.session_state.page == "investasi":
        from investasi import show_investasi
        if st.button("⬅️ Kembali"): st.session_state.page = "dashboard"; st.rerun()
        show_investasi()
    elif st.session_state.page == "hpp":
        from kalkulator import show_hpp
        if st.button("⬅️ Kembali"): st.session_state.page = "dashboard"; st.rerun()
        show_hpp()
        
