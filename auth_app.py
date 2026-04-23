import streamlit as st
import time
from security import verify_user, get_key_info

def show_login_screen():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR AKUN"])
    
    # --- TAB LOGIN ---
    with tab1:
        e_log = st.text_input("Email", key="log_email", placeholder="Email terdaftar")
        p_log = st.text_input("Password", type="password", key="log_pass", placeholder="Password")
        
        if st.button("MASUK KE DASHBOARD", use_container_width=True):
            if e_log and p_log:
                res = verify_user(e_log, p_log, mode="login")
                if res == "SUCCESS_LOGIN":
                    st.session_state.authenticated = True
                    st.session_state.user_email = e_log
                    st.success("Login Berhasil!")
                    time.sleep(1)
                    st.rerun()
                elif res == "ACCOUNT_BLOCKED":
                    st.error("Akun Anda telah diblokir oleh Admin.")
                else:
                    st.error("Email atau Password salah.")
            else:
                st.warning("Isi semua data.")

    # --- TAB DAFTAR (OTOMATIS) ---
    with tab2:
        st.info("Masukkan License Key untuk memunculkan data Nama & Email Anda.")
        
        r_key = st.text_input("License Key", key="reg_key", placeholder="BIZ-XXXXXXX")
        
        if r_key:
            info = get_key_info(r_key)
            
            if info:
                if str(info['status']).upper() == "AKTIF":
                    st.success("Key Valid! Silakan lengkapi pendaftaran.")
                    
                    # Field Nama & Email (Read-Only / Disabled)
                    st.text_input("Nama Lengkap", value=info['nama'], disabled=True)
                    st.text_input("Email (LYNK)", value=info['email'], disabled=True)
                    
                    # Field Password Baru
                    r_pass = st.text_input("Buat Password Baru", type="password", key="reg_pass")
                    
                    if st.button("AKTIFKAN AKUN SEKARANG", use_container_width=True):
                        if r_pass:
                            with st.spinner("Mendaftarkan..."):
                                res = verify_user(info['email'], r_pass, key=r_key, mode="signup")
                                if res == "SUCCESS_SIGNUP":
                                    st.success("Akun berhasil aktif! Silakan login di tab sebelah.")
                                    st.balloons()
                                else:
                                    st.error(f"Gagal: {res}")
                        else:
                            st.warning("Password tidak boleh kosong.")
                else:
                    st.error(f"Maaf, Key ini sudah berstatus: {info['status']}")
            else:
                if len(r_key) >= 8:
                    st.warning("Key tidak ditemukan di database.")

# Integrasi ke App Utama
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    show_login_screen()
    st.stop()
