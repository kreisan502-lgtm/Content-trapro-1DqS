import streamlit as st
import time
from security import verify_user, reset_password
from extra_streamlit_components import CookieManager

# Inisialisasi di level global
cookie_manager = CookieManager()

def show_login_screen():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["🔐 LOGIN", "📝 DAFTAR", "🔑 LUPA PASSWORD"])
    
    with tab1:
        e_log = st.text_input("Email", key="login_email_input")
        p_log = st.text_input("Password", type="password", key="login_pass_input")
        
        if st.button("MASUK", use_container_width=True, key="btn_login_submit"):
            if e_log and p_log:
                res = verify_user(e_log, p_log)
                if res == "SUCCESS_LOGIN":
                    cookie_manager.set("bizinvest_user", e_log)
                    st.session_state.authenticated = True
                    st.session_state.user_email = e_log
                    st.success("Akses Diterima! Membuka Dashboard...")
                    time.sleep(1)
                    st.rerun()
                elif res == "ACCOUNT_BLOCKED":
                    st.error("Akun Anda ditangguhkan (BLOKIR). Hubungi Admin.")
                else:
                    st.error("Email atau Password salah.")
            else:
                st.warning("Mohon isi Email dan Password.")

     with tab2:
        # Teks info box yang baru dengan link aktif
        st.markdown(
            """
            <div style="background-color: #1e3a8a; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 20px;">
                <p style="color: white; margin: 0; font-size: 14px;">
                    💡 <b>Panduan Pendaftaran:</b><br>
                    1. Jika belum memiliki License Key, silakan <a href="http://lynk.id/nore30/pv6kkekzp1j0/checkout" style="color: #fbbf24; font-weight: bold; text-decoration: none;">ORDER KEY DI SINI</a>.<br>
                    2. Jika sudah bayar tapi belum klaim kode, silakan <a href="https://script.google.com/macros/s/AKfycbztryd1YOJLuSiltboR5Lg7bwata41Gu7SrrIdnUMR-FdVlxlUMwVb4f5Udu7xzLUX-/exec" style="color: #fbbf24; font-weight: bold; text-decoration: none;">KLAIM KODE DI SINI</a>.
                </p>
            </div>
            """, 
            unsafe_allow_html=True
        )

        r_key = st.text_input("License Key", key="signup_key_input")
        r_email = st.text_input("Email Baru", key="signup_email_input")
        r_pass = st.text_input("Buat Password", type="password", key="signup_pass_input")
        r_pin = st.text_input("Buat PIN (6 Digit)", type="password", key="signup_pin_input")
        
        if st.button("DAFTAR AKUN", use_container_width=True, key="btn_signup_submit"):
            # ... (logika pendaftaran sama seperti sebelumnya)

    with tab3:
        st.subheader("Reset Password")
        f_email = st.text_input("Email Terdaftar", key="reset_email_input")
        f_key = st.text_input("License Key", key="reset_key_input")
        f_pin = st.text_input("PIN Keamanan", type="password", key="reset_pin_input")
        f_new_p = st.text_input("Password Baru", type="password", key="reset_new_pass_input")
        
        if st.button("SETEL ULANG PASSWORD", use_container_width=True, key="btn_reset_submit"):
            if f_email and f_key and f_pin and f_new_p:
                res = reset_password(f_email, f_key, f_pin, f_new_p)
                if res == "SUCCESS":
                    st.success("Password diperbarui! Silakan Login kembali.")
                else:
                    st.error("Data tidak cocok atau PIN salah.")
            else:
                st.warning("Mohon lengkapi semua syarat reset.")
