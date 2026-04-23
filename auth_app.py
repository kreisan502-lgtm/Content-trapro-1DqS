import streamlit as st
import time
from security import verify_user, get_key_info

def show_login_screen():
    # Inisialisasi state untuk navigasi internal
    if 'auth_view' not in st.session_state: st.session_state.auth_view = "login_page"
    
    # --- LAYAR RESET PASSWORD ---
    if st.session_state.auth_view == "reset_page":
        st.markdown("### 🛠️ Pemulihan Akun")
        f_email = st.text_input("Email Pembelian", key="f_em")
        f_key = st.text_input("License Key", key="f_ky")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("VERIFIKASI DATA", use_container_width=True):
                info = get_key_info(f_key)
                if info and str(info['email']).strip() == str(f_email).strip():
                    st.session_state.can_reset = True
                    st.success("Data diverifikasi!")
                else: st.error("Data tidak cocok.")
        with c2:
            if st.button("BATAL", use_container_width=True):
                st.session_state.auth_view = "login_page"; st.rerun()

        if st.session_state.get('can_reset'):
            new_p = st.text_input("Password Baru", type="password")
            if st.button("UPDATE PASSWORD", use_container_width=True):
                if verify_user(f_email, new_p, key=f_key, mode="signup") == "SUCCESS_SIGNUP":
                    st.success("Sandi diperbarui!"); time.sleep(1)
                    st.session_state.auth_view = "login_page"; st.rerun()
        return

    # --- TAB NORMAL ---
    t1, t2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    with t1:
        e_log = st.text_input("Email Pembelian", key="le")
        p_log = st.text_input("Password", type="password", key="lp")
        
        # Link Biru Lupa Sandi
        st.markdown('<style>div.stButton > button#lupa { background:none; border:none; color:#60a5fa; padding:0; text-decoration:underline; font-size:0.8rem; }</style>', unsafe_allow_html=True)
        if st.button("Lupa kata sandi?", key="lupa"):
            st.session_state.auth_view = "reset_page"; st.rerun()

        if st.button("MASUK", use_container_width=True):
            # PROSES LOGIN & SIMPAN NAMA
            res = verify_user(e_log, p_log, mode="login")
            if isinstance(res, dict) and res["status"] == "SUCCESS":
                st.session_state.authenticated = True
                st.session_state.user_data = {
                    "nama": res["nama"],
                    "email": res["email"]
                }
                st.success(f"Selamat datang, {res['nama']}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Gagal Login. Periksa Email/Password.")

    with t2:
        st.markdown('<div style="background:#1e3a8a; padding:15px; border-radius:10px; border-left:5px solid #fbbf24; color:white; margin-bottom:20px;"><b>💡 Panduan Pendaftaran:</b><br>Belum punya Key? <a href="https://lynk.id/nore30" style="color:#fbbf24; text-decoration:none;">ORDER DI SINI</a>.</div>', unsafe_allow_html=True)
        
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
            st.text_input("Email", value=inf['email'], disabled=True)
            r_pass = st.text_input("Buat Password", type="password", key="new_reg_pass")
            if st.button("DAFTAR SEKARANG", use_container_width=True):
                if verify_user(inf['email'], r_pass, key=st.session_state.rk_ok, mode="signup") == "SUCCESS_SIGNUP":
                    st.success("Registrasi Berhasil!"); st.balloons()
                    
