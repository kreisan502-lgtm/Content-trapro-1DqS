import streamlit as st
import time
from security import verify_user, get_key_info

def show_login_screen():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    # --- TAB LOGIN ---
    with tab1:
        e_log = st.text_input("Email Pembelian", key="log_email")
        p_log = st.text_input("Password", type="password", key="log_pass")
        
        if st.button("MASUK SEKARANG", use_container_width=True):
            if e_log and p_log:
                res = verify_user(e_log, p_log, mode="login")
                if res == "SUCCESS_LOGIN":
                    st.session_state.authenticated = True
                    st.session_state.user_email = e_log
                    st.success("Login Berhasil! Memuat Dashboard...")
                    time.sleep(1)
                    st.rerun()
                elif res == "ACCOUNT_BLOCKED":
                    st.error("Akun Anda diblokir. Hubungi Admin.")
                else:
                    st.error("Email atau Password salah.")
            else:
                st.warning("Lengkapi Email dan Password.")

    # --- TAB DAFTAR (OTOMATIS) ---
    with tab2:
        st.info("Masukkan License Key untuk memvalidasi data Anda.")
        r_key = st.text_input("License Key", key="reg_key", placeholder="BIZ-XXXXXXXX")
        
        if r_key:
            info = get_key_info(r_key)
            
            if info:
                # Jika status masih AKTIF, tampilkan data Nama & Email
                if str(info['status']).upper() == "AKTIF":
                    st.success("Data Ditemukan!")
                    
                    # Field Nama & Email (Read-Only)
                    st.text_input("Nama Lengkap", value=info['nama'], disabled=True)
                    st.text_input("Email (LYNK)", value=info['email'], disabled=True)
                    
                    # Field Input Password Baru
                    r_pass = st.text_input("Buat Password Login", type="password", key="reg_pass")
                    
                    if st.button("AKTIFKAN AKUN", use_container_width=True):
                        if r_pass:
                            with st.spinner("Sedang memproses pendaftaran..."):
                                res = verify_user(info['email'], r_pass, key=r_key, mode="signup")
                                if res == "SUCCESS_SIGNUP":
                                    st.success("Akun Berhasil Aktif! Silakan Login.")
                                    st.balloons()
                                else:
                                    st.error(f"Gagal: {res}")
                        else:
                            st.warning("Buat password terlebih dahulu.")
                else:
                    st.error(f"Key ini sudah digunakan atau statusnya: {info['status']}")
            else:
                if len(r_key) > 5:
                    st.warning("Key tidak ditemukan. Pastikan sudah klaim di generator.")

# Pastikan panggil fungsi di file utama Anda
if __name__ == "__main__":
    show_login_screen()
    
