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

# --- 2. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# --- 3. INISIALISASI COOKIE ---
cookie_manager = CookieManager()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Ambil data dari Cookie browser
saved_email = cookie_manager.get("vip_user_email")
saved_nama = cookie_manager.get("vip_user_nama")

# Logika Autologin: Jika ada cookie tapi session kosong, pulihkan session
if saved_email and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_data = {"nama": saved_nama, "email": saved_email}
    st.session_state.page = "dashboard"

# --- 4. ROUTING HALAMAN ---
if not st.session_state.authenticated:
    show_login_screen()
else:
    # --- SIDEBAR PRO ---
    with st.sidebar:
        user = st.session_state.user_data
        inisial = user['nama'][0].upper() if user['nama'] else "U"
        
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 12px; background-color: #1e293b; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px;">
                <div style="background-color: #fbbf24; color: #1e293b; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{inisial}</div>
                <div style="overflow: hidden;">
                    <p style="margin: 0; color: white; font-weight: bold; font-size: 14px;">{user['nama']}</p>
                    <p style="margin: 0; color: #94a3b8; font-size: 11px;">{user['email']}</p>
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

    # --- KONTEN DINAMIS ---
    if st.session_state.get('page') == "dashboard" or 'page' not in st.session_state:
        st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP DASHBOARD</h1>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 TERMINAL INVESTASI", use_container_width=True):
                st.session_state.page = "investasi"; st.rerun()
        with col2:
            if st.button("🧮 KALKULATOR BISNIS", use_container_width=True):
                st.session_state.page = "hpp"; st.rerun()

    elif st.session_state.page == "investasi":
        if st.button("⬅️ Kembali"): st.session_state.page = "dashboard"; st.rerun()
        show_investasi()
    elif st.session_state.page == "hpp":
        if st.button("⬅️ Kembali"): st.session_state.page = "dashboard"; st.rerun()
        show_hpp()
