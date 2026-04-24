import streamlit as st
import time
import datetime
from security import verify_user, get_key_info
from config import SCRIPT_URL, LINK_ORDER 

def show_login_screen(cookie_manager):
    # CSS kustom
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
            if st.button("KEMBALI", use_container_width=True):
                st.session_state.auth_view = "login_page"; st.rerun()

        if st.session_state.get('can_reset'):
            new_p = st.text_input("Password Baru", type="password", key="new_p_res")
            if st.button("UPDATE PASSWORD", use_container_width=True):
                if verify_user(f_email, new_p, key=f_key, mode="signup") == "SUCCESS_SIGNUP":
                    st.success("Sandi diperbarui!"); time.sleep(1)
                    st.session_state.can_reset = False
                    st.session_state.auth_view = "login_page"; st.rerun()
        return

    # --- TAB UTAMA ---
    t1, t2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    with t1:
        e_log = st.text_input("Email Pembelian", key="le")
        p_log = st.text_input("Password", type="password", key="lp")
        
        if st.button("Lupa kata sandi?", key="lupa_sandi"):
            st.session_state.auth_view = "reset_page"
            st.rerun()

        if st.button("MASUK", use_container_width=True):
            res = verify_user(e_log, p_log, mode="login")
            if isinstance(res, dict) and res["status"] == "SUCCESS":
                st.session_state.authenticated = True 
                
                # Masukkan data ke session state
                st.session_state.user_data = {
                    "nama": res["nama"], 
                    "email": res["email"],
                    "ref": res.get("ref") 
                }
                
                # --- BAGIAN PENYIMPANAN COOKIE (TAMBAHAN UTAMA) ---
                expiry = datetime.date.today() + datetime.timedelta(days=30)
                cookie_manager.set("vip_user_email", str(res["email"]), expires_at=expiry)
                cookie_manager.set("vip_user_nama", str(res["nama"]), expires_at=expiry)
                
                # TITIPKAN REF KE BROWSER AGAR TAHAN REFRESH
                cookie_manager.set("vip_user_ref", str(res.get("ref", "")), expires_at=expiry)
                
                st.success(f"Selamat datang, {res['nama']}!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Gagal Login. Periksa Email/Password.")

    with t2:
        st.markdown(f"""
            <div style="background-color: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 8px; border: 1px solid #bee5eb; margin-bottom: 20px;">
                <span style="font-size: 18px;">💡</span> <b>Panduan Pendaftaran:</b><br>
                1. Belum punya License Key? <a href="{LINK_ORDER}" style="color: #0c5460; font-weight: bold;" target="_blank">ORDER DI SINI</a>.<br>
                2. Sudah bayar tapi belum klaim? <a href="{SCRIPT_URL}" style="color: #0c5460; font-weight: bold;" target="_blank">KLAIM DI SINI</a>.
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
            st.text_input("Email Pembelian", value=inf['email'], disabled=True)
            r_pass = st.text_input("Buat Password", type="password", key="new_reg_pass")
            
            if st.button("DAFTAR SEKARANG", use_container_width=True):
                # Saat signup baru, kita gunakan r_key sebagai referensi pendaftaran
                if verify_user(inf['email'], r_pass, key=st.session_state.rk_ok, mode="signup") == "SUCCESS_SIGNUP":
                    st.success("Registrasi Berhasil! Silakan Login."); st.balloons()
