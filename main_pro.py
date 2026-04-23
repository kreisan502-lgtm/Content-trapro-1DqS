import streamlit as st
import datetime
from auth_app import show_login_screen

# --- 1. IMPORT MODUL (PASTIKAN TIDAK ADA # LAGI) ---
try:
    from investasi import show_investasi 
    from kalkulator import show_hpp
except ImportError:
    st.error("Error: File investasi.py atau kalkulator.py tidak ditemukan!")

# --- 2. CONFIG (WAJIB PALING ATAS) ---
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 3. ANTI-REFRESH SYSTEM ---
# Variabel ini menjaga agar saat refresh, data user tetap ada di memori server
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {"nama": "", "email": ""}
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

# --- 4. LOGIKA ROUTING UTAMA ---
if not st.session_state.authenticated:
    show_login_screen()
else:
    # --- SIDEBAR PRO ---
    with st.sidebar:
        nama_user = st.session_state.user_data.get('nama', 'User')
        email_user = st.session_state.user_data.get('email', '')
        inisial = nama_user[0].upper() if nama_user else "U"

        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 10px; background-color: #1e293b; border-radius: 12px; margin-bottom: 20px; border: 1px solid #334155;">
                <div style="background-color: #fbbf24; color: #1e293b; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{inisial}</div>
                <div>
                    <p style="margin: 0; color: white; font-weight: bold; font-size: 14px;">{nama_user}</p>
                    <p style="margin: 0; color: #94a3b8; font-size: 11px;">{email_user}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.sidebar.button("🏠 Dashboard Utama", use_container_width=True):
            st.session_state.page = "dashboard"
            st.rerun()

        st.write("---")
        if st.sidebar.button("🚪 Keluar Aplikasi", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_data = {"nama": "", "email": ""}
            st.session_state.page = "dashboard"
            st.rerun()

    # --- 5. NAVIGASI HALAMAN ---
    if st.session_state.page == "dashboard":
        st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
        st.write("---")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("📈 Terminal Analisis")
                st.write("Analisis pergerakan aset & teknikal secara real-time.")
                if st.button("BUKA TERMINAL 🚀", key="go_inv", use_container_width=True):
                    st.session_state.page = "investasi"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.subheader("🧮 Kalkulator Bisnis")
                st.write("Hitung HPP, Margin Profit, dan Analisis Keuangan.")
                if st.button("BUKA KALKULATOR 🛠️", key="go_hpp", use_container_width=True):
                    st.session_state.page = "hpp"
                    st.rerun()

    elif st.session_state.page == "investasi":
        if st.button("⬅️ Kembali ke Menu Utama", key="back_inv"):
            st.session_state.page = "dashboard"
            st.rerun()
        show_investasi() # AKTIF MEMANGGIL FILE INVESTASI.PY

    elif st.session_state.page == "hpp":
        if st.button("⬅️ Kembali ke Menu Utama", key="back_hpp"):
            st.session_state.page = "dashboard"
            st.rerun()
        show_hpp() # AKTIF MEMANGGIL FILE KALKULATOR.PY
