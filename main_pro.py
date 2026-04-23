import streamlit as st
import time
from security import verify_user, reset_password
from extra_streamlit_components import CookieManager # Library kunci

# Inisialisasi Cookie Manager
cookie_manager = CookieManager()

st.set_page_config(page_title="BizInvest VIP Suite", layout="centered")

# --- FUNGSI AUTO-LOGIN ---
def check_auto_login():
    # Cek apakah ada cookie bernama 'bizinvest_user'
    saved_user = cookie_manager.get("bizinvest_user")
    if saved_user and 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
        st.session_state.user_email = saved_user
        return True
    return False

# Jalankan cek auto-login di awal
check_auto_login()

def show_auth_page():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🔐 LOGIN", "📝 DAFTAR", "🔑 LUPA PASSWORD"])
    
    with tab1:
        e_log = st.text_input("Email", key="l_email")
        p_log = st.text_input("Password", type="password", key="l_pass")
        
        if st.button("MASUK", use_container_width=True):
            if verify_user(e_log, p_log) == "SUCCESS_LOGIN":
                # SIMPAN COOKIE: Agar saat refresh tidak hilang
                # Expired dalam 7 hari (60 detik * 60 menit * 24 jam * 7 hari)
                cookie_manager.set("bizinvest_user", e_log, expires_at=None)
                
                st.session_state.authenticated = True
                st.session_state.user_email = e_log
                st.success("Berhasil Masuk!")
                time.sleep(1)
                st.rerun()
            else: 
                st.error("Email atau Password salah.")

    # ... (Tab Daftar & Lupa Password tetap sama)

# --- LOGIKA NAVIGASI ---
if not st.session_state.get('authenticated'):
    show_auth_page()
else:
    # Sidebar untuk Logout
    st.sidebar.write(f"Logged in as: {st.session_state.get('user_email')}")
    if st.sidebar.button("LOGOUT"):
        # HAPUS COOKIE: Agar saat refresh setelah logout, dia minta login lagi
        cookie_manager.delete("bizinvest_user")
        st.session_state.authenticated = False
        st.rerun()
        
    # Jalankan Aplikasi Utama (Investasi / HPP)
    st.title("Main Dashboard")
    st.write("Selamat datang kembali!")
