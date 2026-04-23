import streamlit as st
from auth_app import show_login_screen
# Import modul lain milik Anda
# from investasi import show_investasi 
# from kalkulator import show_hpp

# 1. Konfigurasi Halaman (WAJIB PALING ATAS)
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# 2. Inisialisasi Session State (Anti-Refresh)
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'reset_mode' not in st.session_state:
    st.session_state.reset_mode = False

# 3. Logika Tampilan
if not st.session_state.authenticated:
    show_login_screen()
else:
    with st.sidebar:
        st.markdown("### ⚙️ PENGATURAN")
        st.caption(f"👤 Akun: {st.session_state.user_email}")
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # Header Dashboard
    st.markdown('<h1 style="text-align: center; color: #fbbf24;">👑 VIP TERMINAL</h1>', unsafe_allow_html=True)
    
    if st.session_state.current_page == "home":
        st.write("Selamat datang di panel kontrol utama.")
        
