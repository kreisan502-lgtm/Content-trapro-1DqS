import streamlit as st
import time
import datetime
from security import verify_user, get_key_info

def show_login_screen():
    # Mengatur CSS untuk tombol biru kecil (Gambar 3)
    st.markdown("""
        <style>
            div.stButton > button#lupa_sandi {
                background: none;
                border: none;
                color: #60a5fa;
                padding: 0;
                text-decoration: underline;
                font-size: 0.8rem;
                cursor: pointer;
                box-shadow: none;
            }
            div.stButton > button#lupa_sandi:hover {
                color: #3b82f6;
            }
        </style>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    # --- TAB LOGIN (SESUAI GAMBAR 3) ---
    with t1:
        e_log = st.text_input("Email Pembelian", key="le")
        p_log = st.text_input("Password", type="password", key="lp")
        
        # Tombol Lupa Sandi Biru Kecil
        if st.button("Lupa kata sandi?", key="lupa_sandi"):
            st.info("Fitur Reset Otomatis sedang disiapkan. Silakan hubungi Admin atau coba gunakan Expander di bawah.")

        # Expander Reset (Opsional untuk keamanan)
        with st.expander("Klik di sini untuk Reset Password"):
            f_key = st.text_input("Masukkan License Key Anda", key="fky")
            new_p = st.text_input("Password Baru", type="password", key="np")
            if st.button("UPDATE PASSWORD", use_container_width=True):
                # Logika reset kamu
                st.success("Permintaan reset terkirim.")

        if st.button("MASUK", use_container_width=True):
            res = verify_user(e_log, p_log, mode="login")
            if isinstance(res, dict) and res["status"] == "SUCCESS":
                st.session_state.authenticated = True
                st.session_state.user_data = {"nama": res["nama"], "email": res["email"]}
                st.success("Login Berhasil!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Email atau Password salah.")

    # --- TAB DAFTAR (SESUAI GAMBAR 2 - WARNA BIRU MUDA) ---
    with t2:
        # Kotak Info Biru Muda (Alert Info Style)
        st.markdown("""
            <div style="background-color: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 8px; border: 1px solid #bee5eb; margin-bottom: 20px;">
                <span style="font-size: 20px;">💡</span> <b>Panduan Pendaftaran:</b><br>
                1. Belum punya License Key? <a href="https://lynk.id/nore30" style="color: #0c5460; font-weight: bold; text-decoration: underline;">ORDER DI SINI</a>.<br>
                2. Sudah bayar tapi belum klaim? <a href="https://script.google.com/macros/s/AKfycbxohqgxxasTpUpdgPPzu2TLrftc6JYdQ51u51CsMt6-TLAjXhIHTNKHB4RHHtW2_6fR/exec" style="color: #0c5460; font-weight: bold; text-decoration: underline;">KLAIM DI SINI</a>.
            </div>
        """, unsafe_allow_html=True)
        
        r_key = st.text_input("License Key", placeholder="BIZ-XXXXXXX", key="rk")
        if st.button("VALIDASI KEY", use_container_width=True):
            info = get_key_info(r_key)
            if info and info['can_register']:
                st.session_state.rk_ok = r_key
                st.session_state.reg_info = info
                st.success("Key Valid!")
            else:
                st.error("Key tidak ditemukan atau sudah aktif.")

        if st.session_state.get('rk_ok'):
            inf = st.session_state.reg_info
            st.text_input("Nama Terdaftar", value=inf['nama'], disabled=True)
            r_pass = st.text_input("Buat Password Baru", type="password", key="regp")
            if st.button("SELESAIKAN PENDAFTARAN", use_container_width=True):
                if verify_user(inf['email'], r_pass, key=st.session_state.rk_ok, mode="signup") == "SUCCESS_SIGNUP":
                    st.success("Registrasi Berhasil! Silakan Login."); st.balloons()
                    
