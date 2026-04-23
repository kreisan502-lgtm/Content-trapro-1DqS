import streamlit as st
import time
from security import verify_user, reset_password
from extra_streamlit_components import CookieManager

cookie_manager = CookieManager()

def show_login_screen():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🔐 LOGIN", "📝 DAFTAR", "🔑 LUPA PASSWORD"])
    
    with tab1:
        e_log = st.text_input("Email", key="l_email")
        p_log = st.text_input("Password", type="password", key="l_pass")
        if st.button("MASUK", use_container_width=True):
            res = verify_user(e_log, p_log)
            if res == "SUCCESS_LOGIN":
                cookie_manager.set("bizinvest_user", e_log)
                st.session_state.authenticated = True
                st.session_state.user_email = e_log
                st.success("Akses Diterima!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Email atau Password salah.")

    with tab2:
        st.info("Gunakan License Key dari LYNK untuk mendaftar.")
        r_key = st.text_input("License Key")
        r_email = st.text_input("Email Baru")
        r_pass = st.text_input("Buat Password", type="password")
        r_pin = st.text_input("Buat PIN (6 Digit)", type="password")
        if st.button("DAFTAR AKUN", use_container_width=True):
            res = verify_user(r_email, r_pass, key=r_key, pin=r_pin, mode="signup")
            if res == "SUCCESS_SIGNUP": st.success("Berhasil! Silakan Login.")
            else: st.error(f"Gagal: {res}")

    with tab3:
        st.subheader("Reset Password")
        f_email = st.text_input("Email Terdaftar")
        f_key = st.text_input("License Key")
        f_pin = st.text_input("PIN Keamanan", type="password")
        f_new_p = st.text_input("Password Baru", type="password")
        if st.button("SETEL ULANG", use_container_width=True):
            res = reset_password(f_email, f_key, f_pin, f_new_p)
            if res == "SUCCESS": st.success("Password diperbarui!")
            else: st.error("Data tidak cocok.")
