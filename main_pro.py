import streamlit as st
from extra_streamlit_components import CookieManager
from auth_app import show_login_screen
import datetime

# --- 1. IMPORT MODUL ANALISIS ---
try:
    from investasi import show_investasi 
    from kalkulator import show_hpp
except ImportError:
    def show_investasi(): st.error("File investasi.py tidak ditemukan.")
    def show_hpp(): st.error("File kalkulator.py tidak ditemukan.")

# --- 2. CONFIG (WAJIB PALING ATAS) ---
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# --- 3. INISIALISASI COOKIE MANAGER (PEMBERIAN KEY UNIK) ---
# Tambahkan key='main' agar tidak bentrok
cookie_manager = CookieManager(key="main_cookie_manager")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Ambil data dari Cookie browser
saved_email = cookie_manager.get("vip_user_email")
saved_nama = cookie_manager.get("vip_user_nama")

# Logika Autologin
if saved_email and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_data = {"nama": saved_nama, "email": saved_email}
    st.session_state.page = "dashboard"

# --- 4. ROUTING HALAMAN ---
if not st.session_state.authenticated:
    # KIRIM cookie_manager ke fungsi login
    show_login_screen(cookie_manager)
else:
    # --- SIDEBAR PRO ---
    with st.sidebar:
        user = st.session_state.user_data
        nama_u = user.get('nama', 'User')
        email_u = user.get('email', '')
        inisial = nama_u[0].upper() if nama_u else "U"
        
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 12px; background-color: #1e293b; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px;">
                <div style="background-color: #fbbf24; color: #1e293b; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{inisial}</div>
                <div style="overflow: hidden;">
                    <p style="margin: 0; color: white; font-weight: bold; font-size: 14px;">{nama_u}</p>
                    <p style="margin: 0; color: #94a3b8; font-size: 11px;">{email_u}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.button("🏠 Dashboard Utama", use_container_width=True):
            st.session_state.page = "dashboard"; st.rerun()

        st.write("---")
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            cookie_manager.delete("vip_user_email")
            cookie_manager.delete("vip_user_nama")
            st.session_state.authenticated = False
            st.rerun()

    # --- KONTEN HALAMAN ---
    curr_page = st.session_state.get('page', 'dashboard')
    if curr_page == "dashboard":
        st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP DASHBOARD</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 TERMINAL INVESTASI", use_container_width=True):
                st.session_state.page = "investasi"; st.rerun()
        with col2:
            if st.button("🧮 KALKULATOR BISNIS", use_container_width=True):
                st.session_state.page = "hpp"; st.rerun()
    elif curr_page == "investasi":
        if st.button("⬅️ Kembali"): st.session_state.page = "dashboard"; st.rerun()
        show_investasi()
    elif curr_page == "hpp":
        if st.button("⬅️ Kembali"): st.session_state.page = "dashboard"; st.rerun()
        show_hpp()
