import streamlit as st
import time
from security import verify_user, get_key_info

def show_login_screen():
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    # --- TAB LOGIN ---
    with tab1:
        e_log = st.text_input("Email Pembelian", key="log_email")
        p_log = st.text_input("Password", type="password", key="log_pass")
        
        # Link Biru "Lupa kata sandi?" sesuai permintaan
        st.markdown("""
            <div style="text-align: right; margin-top: -15px; margin-bottom: 10px;">
                <a href="https://wa.me/6285797416836?text=Halo%20Admin,%20saya%20lupa%20password" 
                style="color: #60a5fa; text-decoration: none; font-size: 0.8rem;">Lupa kata sandi?</a>
            </div>
        """, unsafe_allow_html=True)

        if st.button("MASUK", use_container_width=True):
            res = verify_user(e_log, p_log, mode="login")
            if res == "SUCCESS_LOGIN":
                st.session_state.authenticated = True
                st.session_state.user_email = e_log
                st.rerun()
            else:
                st.error("Email atau Password salah.")

    # --- TAB DAFTAR ---
    with tab2:
        # Kotak Panduan Pendaftaran Biru
        st.markdown("""
            <div style="background-color: #1e3a8a; padding: 15px; border-radius: 10px; border-left: 5px solid #fbbf24; margin-bottom: 20px;">
                <p style="color: white; margin: 0; font-weight: bold;">💡 Panduan Pendaftaran:</p>
                <p style="color: white; margin: 5px 0; font-size: 0.9rem;">1. Jika belum memiliki License Key, silakan <a href="https://lynk.id/nore30" style="color: #fbbf24; font-weight: bold; text-decoration: none;">ORDER KEY DI SINI</a>.</p>
                <p style="color: white; margin: 5px 0; font-size: 0.9rem;">2. Jika sudah bayar tapi belum klaim kode, silakan <a href="#" style="color: #fbbf24; font-weight: bold; text-decoration: none;">KLAIM KODE DI SINI</a>.</p>
            </div>
        """, unsafe_allow_html=True)

        r_key = st.text_input("License Key", key="reg_key", placeholder="BIZ-XXXXXXX")
        
        # Tombol Validasi Manual
        if st.button("VALIDASI KEY", use_container_width=True):
            info = get_key_info(r_key)
            if info and info['status'] == "AKTIF":
                st.session_state.temp_nama = info['nama']
                st.session_state.temp_email = info['email']
                st.session_state.key_valid = True
            else:
                st.error("Key tidak valid atau sudah digunakan.")

        # Jika key valid, tampilkan input password saja
        if st.session_state.get('key_valid'):
            st.text_input("Nama Terdaftar", value=st.session_state.temp_nama, disabled=True)
            st.text_input("Email Terdaftar", value=st.session_state.temp_email, disabled=True)
            r_pass = st.text_input("Buat Password Baru", type="password", key="reg_pass")
            
            if st.button("AKTIFKAN AKUN", use_container_width=True):
                if r_pass:
                    res = verify_user(st.session_state.temp_email, r_pass, key=r_key, mode="signup")
                    if res == "SUCCESS_SIGNUP":
                        st.success("Akun Berhasil Aktif! Silakan pindah ke tab LOGIN.")
                        st.balloons()
