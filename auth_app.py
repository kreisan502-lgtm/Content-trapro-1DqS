import streamlit as st
import time
from security import verify_user, get_key_info

def show_login_screen():
    # State untuk mengatur perpindahan layar ke Reset Password
    if 'reset_view' not in st.session_state:
        st.session_state.reset_view = False
    if 'reset_step_2' not in st.session_state:
        st.session_state.reset_step_2 = False

    # --- TAMPILAN RESET PASSWORD (Gaya Windows/Web Modern) ---
    if st.session_state.reset_view:
        st.markdown("### 🛠️ Pemulihan Akun")
        st.write("Verifikasi identitas untuk mengubah kata sandi.")
        
        f_email = st.text_input("Email Pembelian", key="f_email_reset")
        f_key = st.text_input("License Key", key="f_key_reset")
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            if st.button("VERIFIKASI DATA", use_container_width=True):
                info = get_key_info(f_key)
                if info and info['email'] == f_email:
                    st.session_state.reset_step_2 = True
                    st.session_state.res_email = f_email
                    st.session_state.res_key = f_key
                    st.success("Data diverifikasi!")
                else:
                    st.error("Data tidak ditemukan.")
        with col_res2:
            if st.button("BATAL", use_container_width=True):
                st.session_state.reset_view = False
                st.session_state.reset_step_2 = False
                st.rerun()

        # Step 2: Input Password Baru jika verifikasi lolos
        if st.session_state.reset_step_2:
            new_p = st.text_input("Kata Sandi Baru", type="password")
            if st.button("SIMPAN PERUBAHAN", use_container_width=True):
                res = verify_user(st.session_state.res_email, new_p, key=st.session_state.res_key, mode="signup")
                if res == "SUCCESS_SIGNUP":
                    st.success("Sandi berhasil diubah! Memuat ulang...")
                    time.sleep(1.5)
                    st.session_state.reset_view = False
                    st.session_state.reset_step_2 = False
                    st.rerun()
        return # Menghentikan render agar tab login di bawah tidak muncul

    # --- TAMPILAN LOGIN & DAFTAR NORMAL ---
    tab1, tab2 = st.tabs(["🔐 LOGIN", "📝 DAFTAR"])

    with tab1:
        e_log = st.text_input("Email Pembelian", key="log_email")
        p_log = st.text_input("Password", type="password", key="log_pass")
        
        # Link Biru Lupa Sandi
        # Gunakan button transparan/kecil agar bisa memicu perubahan state
        st.markdown("""<style>div.stButton > button#btn_lupa { background: none; border: none; color: #60a5fa; padding: 0; font-size: 0.8rem; text-decoration: underline; }</style>""", unsafe_allow_html=True)
        if st.button("Lupa kata sandi?", key="btn_lupa"):
            st.session_state.reset_view = True
            st.rerun()

        if st.button("MASUK", use_container_width=True):
            res = verify_user(e_log, p_log, mode="login")
            if res == "SUCCESS_LOGIN":
                st.session_state.authenticated = True
                st.session_state.user_email = e_log
                st.rerun()
            else:
                st.error("Gagal Login.")

    with tab2:
        # PANDUAN BIRU (Sesuai Screenshot Anda)
        st.markdown("""
            <div style="background-color: #1e3a8a; padding: 15px; border-radius: 10px; border-left: 5px solid #fbbf24; margin-bottom: 20px;">
                <p style="color: white; margin: 0; font-weight: bold;">💡 Panduan Pendaftaran:</p>
                <p style="color: white; margin: 5px 0; font-size: 0.8rem;">1. Belum punya License Key? <a href="https://lynk.id/nore30" style="color: #fbbf24; text-decoration: none;">ORDER DI SINI</a>.</p>
                <p style="color: white; margin: 5px 0; font-size: 0.8rem;">2. Sudah bayar tapi belum klaim? <a href="https://script.google.com/macros/s/AKfycby0CzpBx5JCnUZNApcOqWCkZ0adGJkhPsbowmQX1fylV9fxQP2ETtWb-vZ6F3bnFpvF/exec" style="color: #fbbf24; text-decoration: none;">KLAIM DI SINI</a>.</p>
            </div>
        """, unsafe_allow_html=True)

        r_key = st.text_input("License Key", placeholder="BIZ-XXXXXXX", key="reg_key")
        
        if st.button("VALIDASI KEY", use_container_width=True):
            info = get_key_info(r_key)
            if info and info['status'] == "AKTIF":
                st.session_state.key_valid = True
                st.session_state.temp_nama = info['nama']
                st.session_state.temp_email = info['email']
            else:
                st.error("Key sudah digunakan atau tidak ditemukan.")

        if st.session_state.get('key_valid'):
            st.text_input("Nama", value=st.session_state.temp_nama, disabled=True)
            st.text_input("Email", value=st.session_state.temp_email, disabled=True)
            r_pass = st.text_input("Buat Password Baru", type="password")
            if st.button("AKTIFKAN AKUN SEKARANG", use_container_width=True):
                res = verify_user(st.session_state.temp_email, r_pass, key=r_key, mode="signup")
                if res == "SUCCESS_SIGNUP":
                    st.success("Akun Berhasil Aktif!")
                    st.balloons()
                    
