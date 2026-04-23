import streamlit as st
import time
from security import verify_user, get_key_info

def show_login_screen():
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    # --- TAB LOGIN ---
    with tab1:
        e_log = st.text_input("Email Pembelian", key="log_email")
        p_log = st.text_input("Password", type="password", key="log_pass")
        
        if st.button("MASUK", use_container_width=True):
            res = verify_user(e_log, p_log, mode="login")
            if res == "SUCCESS_LOGIN":
                st.session_state.authenticated = True
                st.session_state.user_email = e_log
                st.success("Berhasil! Membuka Dashboard...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Email atau Password salah.")

        # FITUR: LUPA KATA SANDI
        st.write("---")
        with st.expander("🔑 Lupa Kata Sandi? (Reset via Email & Key)"):
            f_email = st.text_input("Email Terdaftar", key="f_email")
            f_key = st.text_input("License Key", key="f_key")
            
            if st.button("VERIFIKASI DATA", use_container_width=True):
                info = get_key_info(f_key)
                if info and info['email'] == f_email:
                    st.session_state.reset_allowed = True
                    st.session_state.res_email = f_email
                    st.session_state.res_key = f_key
                    st.success("Data Cocok! Silakan masukkan password baru di bawah.")
                else:
                    st.error("Email atau Key tidak valid.")

            if st.session_state.reset_allowed:
                new_pass = st.text_input("Password Baru", type="password")
                if st.button("UPDATE PASSWORD", use_container_width=True):
                    # Menggunakan mode signup untuk overwrite password lama
                    res = verify_user(st.session_state.res_email, new_pass, key=st.session_state.res_key, mode="signup")
                    if res == "SUCCESS_SIGNUP":
                        st.success("Password diperbarui! Silakan Login.")
                        st.session_state.reset_allowed = False
                        time.sleep(1)
                        st.rerun()

    # --- TAB DAFTAR ---
    with tab2:
        r_key = st.text_input("License Key", key="reg_key", placeholder="BIZ-XXXXXXX")
        
        col1, col2 = st.columns(2)
        with col1:
            btn_val = st.button("VALIDASI KEY", use_container_width=True)
        with col2:
            st.link_button("BELI PRODUK", "https://lynk.id/nore30", use_container_width=True)

        if r_key or btn_val:
            info = get_key_info(r_key)
            if info and info['status'] == "AKTIF":
                # Disabled sesuai permintaan agar tidak bisa diedit
                st.text_input("Nama", value=info['nama'], disabled=True)
                st.text_input("Email", value=info['email'], disabled=True)
                
                r_pass = st.text_input("Buat Password", type="password", key="reg_pass")
                if st.button("AKTIFKAN AKUN", use_container_width=True):
                    if r_pass:
                        res = verify_user(info['email'], r_pass, key=r_key, mode="signup")
                        if res == "SUCCESS_SIGNUP":
                            st.success(f"Akun {info['nama']} Aktif! Silakan Login.")
                            st.balloons()
                    else:
                        st.warning("Password wajib diisi.")
            elif info:
                st.error(f"Key ini sudah {info['status']}")
            else:
                if len(r_key) > 5: st.warning("Key tidak ditemukan.")
                              
