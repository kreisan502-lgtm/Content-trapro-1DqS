import streamlit as st
import time
from security import verify_user

def show_settings():
    st.markdown("<h2 style='color: #fbbf24;'>⚙️ Pengaturan Akun</h2>", unsafe_allow_html=True)
    st.write("Perbarui informasi profil dan keamanan Anda.")
    st.write("---")

    user = st.session_state.get('user_data', {"nama": "", "email": ""})

    with st.container(border=True):
        new_nama = st.text_input("Nama Lengkap", value=user.get('nama'))
        new_email = st.text_input("Email Baru", value=user.get('email'))
        new_pass = st.text_input("Kata Sandi Baru", type="password", placeholder="Kosongkan jika tidak ingin diubah")
        
        st.info("⚠️ Masukkan License Key Anda untuk memverifikasi perubahan.")
        v_key = st.text_input("License Key", type="password")

        if st.button("SIMPAN PERUBAHAN", use_container_width=True):
            if v_key:
                # Mode signup digunakan untuk menimpa data (Update)
                res = verify_user(new_email, new_pass, key=v_key, mode="signup")
                if res == "SUCCESS_SIGNUP":
                    st.success("Profil berhasil diperbarui! Silakan Login ulang.")
                    time.sleep(2)
                    st.session_state.authenticated = False
                    st.rerun()
                else:
                    st.error("Gagal update. Pastikan Key benar.")
            else:
                st.warning("License Key wajib diisi.")

    if st.button("⬅️ Kembali ke Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"; st.rerun()
