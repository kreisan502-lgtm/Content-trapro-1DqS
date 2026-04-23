import streamlit as st
from auth_app import show_login_screen
from investasi import show_investasi
from kalkulator import show_hpp

# 1. PENGATURAN HALAMAN (Paling Atas)
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. INISIALISASI SESSION STATE (Anti-Refresh)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""

# 3. LOGIKA TAMPILAN
if not st.session_state.authenticated:
    show_login_screen()
else:
    # --- SIDEBAR DASHBOARD ---
    with st.sidebar:
        st.markdown("### ⚙️ PENGATURAN")
        st.caption(f"👤 Akun: {st.session_state.user_email}")
        st.write("---")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
            
        if st.button("📈 Terminal Analisis", use_container_width=True):
            st.session_state.current_page = "investasi"
            st.rerun()
            
        if st.button("🧮 Kalkulator Bisnis", use_container_width=True):
            st.session_state.current_page = "hpp"
            st.rerun()

        st.write("---")
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- KONTEN UTAMA ---
    st.markdown("""
        <div style="text-align: center; padding: 10px;">
            <h1 style="color: #fbbf24; margin-bottom: 0;">👑 VIP TERMINAL</h1>
            <p style="color: #94a3b8; font-size: 14px;">BizInvest VIP Terminal v2.0</p>
        </div>
    """, unsafe_allow_html=True)

    if st.session_state.current_page == "home":
        st.subheader("Selamat Datang!")
        col1, col2 = st.columns(2)
        with col1:
            st.info("Gunakan Terminal Analisis untuk memantau aset.")
        with col2:
            st.success("Gunakan Kalkulator untuk hitung profit bisnis.")

    elif st.session_state.current_page == "investasi":
        show_investasi()

    elif st.session_state.current_page == "hpp":
        show_hpp()
        
