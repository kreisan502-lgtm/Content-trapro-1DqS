import streamlit as st
import time
from security import verify_user, get_key_info

def show_login_screen():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    # --- TAB LOGIN ---
    with tab1:
        e_log = st.text_input("Email Pembelian", key="log_email_field")
        p_log = st.text_input("Password", type="password", key="log_pass_field")
        
        if st.button("MASUK SEKARANG", use_container_width=True, key="btn_login"):
            if e_log and p_log:
                res = verify_user(e_log, p_log, mode="login")
                if res == "SUCCESS_LOGIN":
                    st.session_state.authenticated = True
                    st.session_state.user_email = e_log
                    st.success("Login Berhasil! Memuat Dashboard...")
                    time.sleep(1)
                    st.rerun()
                elif res == "ACCOUNT_BLOCKED":
                    st.error("Akun Anda ditangguhkan. Hubungi Admin.")
                else:
                    st.error("Email atau Password salah.")
            else:
                st.warning("Mohon isi Email dan Password.")

    # --- TAB DAFTAR (OTOMATIS) ---
    with tab2:
        st.info("Masukkan License Key Anda untuk memvalidasi data.")
        r_key = st.text_input("License Key", key="reg_key_field", placeholder="BIZ-XXXXXXXX")
        
        if r_key:
            info = get_key_info(r_key)
            
            if info:
                if str(info['status']).upper() == "AKTIF":
                    st.success("Key Valid! Data ditemukan.")
                    
                    # Field Nama & Email (Read-Only)
                    st.text_input("Nama Lengkap", value=info['nama'], disabled=True)
                    st.text_input("Email (LYNK)", value=info['email'], disabled=True)
                    
                    # Input Password Baru
                    r_pass = st.text_input("Buat Password Login", type="password", key="reg_pass_new")
                    
                    if st.button("AKTIFKAN AKUN", use_container_width=True, key="btn_reg_confirm"):
                        if r_pass:
                            with st.spinner("Mendaftarkan akun..."):
                                res = verify_user(info['email'], r_pass, key=r_key, mode="signup")
                                if res == "SUCCESS_SIGNUP":
                                    # Custom Message Berhasil
                                    st.balloons()
                                    st.markdown(f"""
                                        <div style="background-color: #dcfce7; padding: 20px; border-radius: 15px; border-left: 6px solid #22c55e; margin-top: 15px;">
                                            <h3 style="color: #166534; margin: 0;">✅ Berhasil!</h3>
                                            <p style="color: #166534; font-size: 14px;">Akun atas nama <b>{info['nama']}</b> telah aktif.</p>
                                            <p style="color: #166534; font-size: 13px; font-weight: bold;">Silakan pindah ke Tab LOGIN untuk masuk.</p>
                                        </div>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.error(f"Gagal: {res}")
                        else:
                            st.warning("Harap buat password terlebih dahulu.")
                else:
                    st.error(f"Key ini sudah digunakan atau statusnya: {info['status']}")
            else:
                if len(r_key) > 5:
                    st.warning("Key tidak ditemukan. Pastikan sudah klaim kode di generator.")

# Pastikan fungsi ini dipanggil di file utama Anda (main_pro.py)
