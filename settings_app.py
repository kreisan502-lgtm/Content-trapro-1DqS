import streamlit as st
import time
from security import verify_user

def show_settings():
    st.markdown("### ⚙️ Pengaturan Akun")
    st.write("Ubah informasi profil dan keamanan Anda.")
    
    user = st.session_state.user_data
    
    with st.form("form_settings"):
        new_nama = st.text_input("Ganti Nama", value=user['nama'])
        new_email = st.text_input("Ganti Email", value=user['email'])
        new_pass = st.text_input("Ganti Kata Sandi Baru", type="password", placeholder="Isi jika ingin merubah")
        
        st.warning("⚠️ Perubahan data memerlukan verifikasi License Key Anda.")
        verify_key = st.text_input("Masukkan License Key Anda", type="password")
        
        if st.form_submit_button("SIMPAN PERUBAHAN", use_container_width=True):
            if verify_key:
                # Gunakan fungsi signup dari security untuk menimpa data lama (Update)
                status = verify_user(new_email, new_pass, key=verify_key, mode="signup")
                if status == "SUCCESS_SIGNUP":
                    st.success("Profil berhasil diperbarui! Silakan login ulang.")
                    time.sleep(1.5)
                    st.session_state.authenticated = False
                    st.rerun()
                else:
                    st.error("Gagal memperbarui. Pastikan Key benar.")
            else:
                st.error("License Key wajib diisi untuk keamanan.")
