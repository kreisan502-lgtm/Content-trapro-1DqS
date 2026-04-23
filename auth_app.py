import streamlit as st
import time
from security import verify_user, get_key_info

def show_login_screen():
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    with tab1:
        e_log = st.text_input("Email Pembelian", key="log_email")
        p_log = st.text_input("Password", type="password", key="log_pass")
        if st.button("MASUK", use_container_width=True):
            res = verify_user(e_log, p_log, mode="login")
            if res == "SUCCESS_LOGIN":
                st.session_state.authenticated = True
                st.session_state.user_email = e_log
                st.success("Berhasil! Membuka Dashboard...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Email atau Password salah.")

    with tab2:
        r_key = st.text_input("License Key", key="reg_key", placeholder="BIZ-XXXXXXX")
        if r_key:
            info = get_key_info(r_key)
            if info and info['status'] == "AKTIF":
                st.text_input("Nama", value=info['nama'], disabled=True)
                st.text_input("Email", value=info['email'], disabled=True)
                r_pass = st.text_input("Buat Password", type="password", key="reg_pass")
                if st.button("AKTIFKAN AKUN", use_container_width=True):
                    if r_pass:
                        res = verify_user(info['email'], r_pass, key=r_key, mode="signup")
                        if res == "SUCCESS_SIGNUP":
                            st.success(f"Akun {info['nama']} Aktif! Silakan Login.")
                            st.balloons()
                    else:
                        st.warning("Password wajib diisi.")
            elif info:
                st.error(f"Key ini sudah {info['status']}")
            else:
                if len(r_key) > 5: st.warning("Key tidak ditemukan.")
                    
