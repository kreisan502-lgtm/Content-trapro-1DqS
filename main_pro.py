import streamlit as st
from auth_app import show_login_screen
from investasi import show_investasi
from kalkulator import show_hpp

# Pengaturan dasar halaman (WAJIB PALING ATAS)
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 1. INISIALISASI SESSION STATE ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'setting_currency' not in st.session_state:
    st.session_state.setting_currency = "IDR"
if 'setting_lang' not in st.session_state:
    st.session_state.setting_lang = "Indonesia"

# --- 2. LOGIKA TAMPILAN (LOGIN VS DASHBOARD) ---
if not st.session_state.authenticated:
    show_login_screen()
else:
    # --- 3. SIDEBAR ---
    with st.sidebar:
        st.markdown("### ⚙️ PENGATURAN")
        st.session_state.setting_currency = st.radio("Mata Uang:", ["IDR", "USD"])
        st.session_state.setting_lang = st.selectbox("Bahasa:", ["Indonesia", "English"])
        
        st.write("---")
        st.caption(f"👤 Akun: {st.session_state.user_email}")
        
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- 4. HEADER ---
    st.markdown(f"""
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #fbbf24; margin-bottom: 0;">👑 VIP TERMINAL</h1>
            <p style="color: #94a3b8; font-size: 14px;">BizInvest VIP Terminal v2.0</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 5. NAVIGASI ---
    if st.session_state.current_page == "home":
        col1, col2 = st.columns(2)
        with col1:
            st.info("### 📈 Investasi\nAnalisis Saham & Crypto.")
            if st.button("Buka Terminal Analisis 🚀", use_container_width=True):
                st.session_state.current_page = "investasi"
                st.rerun()
        with col2:
            st.success("### 🧮 Kalkulator\nHitung HPP & Margin.")
            if st.button("Buka Kalkulator Bisnis 🛠️", use_container_width=True):
                st.session_state.current_page = "hpp"
                st.rerun()

    elif st.session_state.current_page == "investasi":
        if st.button("⬅️ Kembali"):
            st.session_state.current_page = "home"
            st.rerun()
        show_investasi()

    elif st.session_state.current_page == "hpp":
        if st.button("⬅️ Kembali"):
            st.session_state.current_page = "home"
            st.rerun()
        show_hpp()
        
