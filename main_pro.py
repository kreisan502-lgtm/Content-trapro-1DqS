import streamlit as st
import datetime
from auth_app import show_login_screen

# --- PERBAIKAN 1: Buka Import Modul ---
from investasi import show_investasi 
from kalkulator import show_hpp

# --- 1. CONFIG (HARUS PALING ATAS) ---
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. ANTI-REFRESH SYSTEM ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {"nama": "", "email": ""}
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

# --- 3. LOGIKA ROUTING ---
if not st.session_state.authenticated:
    show_login_screen()
else:
    # --- SIDEBAR PRO ---
    with st.sidebar:
        # Mengambil data dari session_state agar tidak hilang saat ganti halaman
        user = st.session_state.user_data
        nama_user = user.get('nama', 'User')
        email_user = user.get('email', '')
        inisial = nama_user[0].upper() if nama_user else "U"

        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 10px; background-color: #1e293b; border-radius: 12px; margin-bottom: 20px; border: 1px solid #334155;">
                <div style="background-color: #fbbf24; color: #1e293b; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{inisial}</div>
                <div style="overflow: hidden;">
                    <p style="margin: 0; color: white; font-weight: bold; font-size: 14px;">{nama_user}</p>
                    <p style="margin: 0; color: #94a3b8; font-size: 12px;">{email_user}</p>
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
            st.rerun()

    # --- 4. NAVIGASI HALAMAN (PERBAIKAN 2: Panggil Fungsi Modul) ---
    if st.session_state.page == "dashboard":
        st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
        st.write("---")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("📈 Terminal Analisis")
                if st.button("BUKA TERMINAL", key="go_inv", use_container_width=True):
                    st.session_state.page = "investasi"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.subheader("🧮 Kalkulator Bisnis")
                if st.button("BUKA KALKULATOR", key="go_hpp", use_container_width=True):
                    st.session_state.page = "hpp"
                    st.rerun()

    elif st.session_state.page == "investasi":
        if st.button("⬅️ Kembali ke Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        show_investasi() # Memanggil fungsi dari investasi.py

    elif st.session_state.page == "hpp":
        if st.button("⬅️ Kembali ke Dashboard"):
            st.session_state.page = "dashboard"
            st.rerun()
        show_hpp() # Memanggil fungsi dari kalkulator.py
