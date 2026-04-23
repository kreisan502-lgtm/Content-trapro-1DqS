import streamlit as st
import time
import datetime
from security import verify_user, get_key_info

# Tambahkan 'cookie_manager' di dalam kurung agar tidak error TypeError
def show_login_screen(cookie_manager):
    # CSS kustom untuk tombol Lupa Sandi kecil warna biru (Gambar 3)
    st.markdown("""
        <style>
            div.stButton > button#lupa_sandi {
                background: none; border: none; color: #60a5fa; padding: 0;
                text-decoration: underline; font-size: 0.8rem; cursor: pointer; box-shadow: none;
            }
            div.stButton > button#lupa_sandi:hover { color: #3b82f6; }
        </style>
    """, unsafe_allow_html=True)

    if 'auth_view' not in st.session_state: st.session_state.auth_view = "login_page"
    
    t1, t2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    # --- TAB LOGIN (SESUAI GAMBAR 3) ---
    with t1:
        e_log = st.text_input("Email Pembelian", key="le")
        p_log = st.text_input("Password", type="password", key="lp")
        
        # Tombol biru kecil (Gambar 3)
        if st.button("Lupa kata sandi?", key="lupa_sandi"):
            st.session_state.auth_view = "reset_page"
            st.rerun()

        if st.button("MASUK", use_container_width=True):
            res = verify_user(e_log, p_log, mode="login")
            if isinstance(res, dict) and res["status"] == "SUCCESS":
                st.session_state.authenticated = True 
                st.session_state.user_data = {"nama": res["nama"], "email": res["email"]}
                
                # Simpan ke Cookie
                expiry = datetime.date.today() + datetime.timedelta(days=30)
                cookie_manager.set("vip_user_email", res["email"], expires_at=expiry)
                cookie_manager.set("vip_user_nama", res["nama"], expires_at=expiry)
                
                st.success(f"Selamat datang, {res['nama']}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Gagal Login. Periksa Email/Password.")

    # --- TAB DAFTAR (SESUAI GAMBAR 2) ---
    with t2:
        # Kotak Notifikasi Biru Muda (Gambar 2)
        st.markdown("""
            <div style="background-color: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 8px; border: 1px solid #bee5eb; margin-bottom: 20px;">
                <span style="font-size: 18px;">💡</span> <b>Panduan Pendaftaran:</b><br>
                1. Belum punya License Key? <a href="https://lynk.id/nore30" style="color: #0c5460; font-weight: bold;">ORDER DI SINI</a>.<br>
                2. Sudah bayar tapi belum klaim? <a href="#" style="color: #0c5460; font-weight: bold;">KLAIM DI SINI</a>.
            </div>
        """, unsafe_allow_html=True)
        
        r_key = st.text_input("License Key", placeholder="BIZ-XXXXXXX", key="rk")
        if st.button("VALIDASI KEY", use_container_width=True):
            info = get_key_info(r_key)
            if info and info['can_register']:
                st.session_state.reg_info = info
                st.session_state.rk_ok = r_key
                st.success("Key Valid!")
            else: st.error("Key sudah terdaftar atau tidak aktif.")

        if st.session_state.get('rk_ok'):
            inf = st.session_state.reg_info
            st.text_input("Nama", value=inf['nama'], disabled=True)
            r_pass = st.text_input("Buat Password", type="password", key="new_reg_pass")
            if st.button("DAFTAR SEKARANG", use_container_width=True):
                if verify_user(inf['email'], r_pass, key=st.session_state.rk_ok, mode="signup") == "SUCCESS_SIGNUP":
                    st.success("Registrasi Berhasil!"); st.balloons()
                    
