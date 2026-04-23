import streamlit as st
import time
from security import verify_user, reset_password
from investasi import show_investasi
from kalkulator import show_hpp

st.set_page_config(page_title="BizInvest VIP Suite", layout="centered")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def show_auth_page():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🔐 LOGIN", "📝 DAFTAR", "🔑 LUPA PASSWORD"])
    
    with tab1:
        e_log = st.text_input("Email", key="l_email")
        p_log = st.text_input("Password", type="password", key="l_pass")
        if st.button("MASUK", use_container_width=True):
            if verify_user(e_log, p_log) == "SUCCESS_LOGIN":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("Email atau Password salah.")

    with tab2:
        st.info("Gunakan License Key dari LYNK untuk mendaftar.")
        r_key = st.text_input("License Key")
        r_email = st.text_input("Email Baru")
        r_pass = st.text_input("Buat Password", type="password")
        r_pin = st.text_input("Buat PIN Keamanan (6 Digit)", type="password", help="PENTING: Simpan PIN ini untuk reset password.")
        
        if st.button("DAFTAR AKUN", use_container_width=True):
            if r_key and r_email and r_pass and r_pin:
                res = verify_user(r_email, r_pass, key=r_key, pin=r_pin, mode="signup")
                if res == "SUCCESS_SIGNUP": st.success("Berhasil! Silakan Login.")
                else: st.error(f"Gagal: {res}")
            else: st.warning("Isi semua kolom.")

    with tab3:
        st.subheader("Reset Password")
        f_email = st.text_input("Email Terdaftar")
        f_key = st.text_input("License Key")
        f_pin = st.text_input("PIN Keamanan Anda", type="password")
        f_new_p = st.text_input("Password Baru", type="password")
        
        if st.button("SETEL ULANG PASSWORD", use_container_width=True):
            res = reset_password(f_email, f_key, f_pin, f_new_p)
            if res == "SUCCESS": st.success("Password diperbarui!")
            elif res == "WRONG_PIN": st.error("PIN Salah!")
            else: st.error("Data tidak cocok.")

# Logika Navigasi
if not st.session_state.authenticated:
    show_auth_page()
else:
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False}))
    # Tampilkan modul investasi atau hpp di sini
    show_investasi()
    
