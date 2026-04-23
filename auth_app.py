import streamlit as st
import time
import datetime
from extra_streamlit_components import CookieManager
from security import verify_user, get_key_info

def show_login_screen():
    cm = CookieManager()
    if 'auth_view' not in st.session_state: st.session_state.auth_view = "login_page"
    
    t1, t2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    with t1:
        e_log = st.text_input("Email Pembelian", key="le")
        p_log = st.text_input("Password", type="password", key="lp")
        
        if st.button("MASUK KE SISTEM", use_container_width=True):
            res = verify_user(e_log, p_log, mode="login")
            if isinstance(res, dict) and res["status"] == "SUCCESS":
                # 1. Simpan ke Session
                st.session_state.authenticated = True 
                st.session_state.user_data = {"nama": res["nama"], "email": res["email"]}
                
                # 2. Tanam Cookie (Berlaku 30 Hari)
                expiry = datetime.date.today() + datetime.timedelta(days=30)
                cm.set("vip_user_email", res["email"], expires_at=expiry)
                cm.set("vip_user_nama", res["nama"], expires_at=expiry)
                
                st.success("Login Berhasil! Memuat Dashboard...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Email atau Password salah.")

    with t2:
        st.info("Gunakan License Key dari email konfirmasi LYNK.id Anda.")
        r_key = st.text_input("License Key", placeholder="BIZ-XXXXXXX", key="rk")
        
        if st.button("VALIDASI KEY", use_container_width=True):
            info = get_key_info(r_key)
            if info and info['can_register']:
                st.session_state.reg_info = info
                st.session_state.rk_ok = r_key
                st.success("Key Valid! Silakan buat password.")
            else:
                st.error("Key tidak ditemukan atau sudah terdaftar.")

        if st.session_state.get('rk_ok'):
            inf = st.session_state.reg_info
            st.text_input("Nama Terdaftar", value=inf['nama'], disabled=True)
            r_pass = st.text_input("Buat Password Baru", type="password", key="new_reg_pass")
            
            if st.button("SELESAIKAN PENDAFTARAN", use_container_width=True):
                if r_pass:
                    status = verify_user(inf['email'], r_pass, key=st.session_state.rk_ok, mode="signup")
                    if status == "SUCCESS_SIGNUP":
                        st.success("Pendaftaran Berhasil! Silakan Login di tab sebelah.")
                        st.balloons()
                else:
                    st.warning("Password tidak boleh kosong.")
