import streamlit as st
import time
from security import verify_user

def show_settings():
    # Header Pengaturan
    st.markdown("""
        <div style="margin-top: -50px;">
            <h1 style="color: #fbbf24; font-size: 2rem; font-weight: 800;">⚙️ Pengaturan Akun</h1>
            <p style="color: #94a3b8; font-size: 0.9rem;">Kelola informasi profil dan keamanan akses Anda.</p>
        </div>
        <hr style="border: 0.5px solid #334155; margin-bottom: 30px;">
    """, unsafe_allow_html=True)

    # Mengambil data user saat ini dari session
    user = st.session_state.get('user_data', {"nama": "", "email": ""})

    # Container Form Premium
    with st.container(border=True):
        st.subheader("Informasi Profil")
        
        col1, col2 = st.columns(2)
        with col1:
            new_nama = st.text_input("Nama Lengkap", value=user['nama'], placeholder="Masukkan nama baru")
        with col2:
            new_email = st.text_input("Email Pembelian", value=user['email'], placeholder="Masukkan email baru")
            
        st.write("---")
        st.subheader("Keamanan")
        new_pass = st.text_input("Kata Sandi Baru", type="password", placeholder="Kosongkan jika tidak ingin diubah")
        
        st.markdown("""
            <div style="background-color: #fef3c7; color: #92400e; padding: 15px; border-radius: 10px; margin: 20px 0; font-size: 0.85rem; border-left: 5px solid #fbbf24;">
                <b>⚠️ Konfirmasi Diperlukan:</b><br>
                Untuk menyimpan perubahan, Anda wajib memasukkan <b>License Key</b> yang aktif sebagai bentuk verifikasi kepemilikan akun.
            </div>
        """, unsafe_allow_html=True)
        
        verify_key = st.text_input("Masukkan License Key Anda", type="password", placeholder="BIZ-XXXXXXX")

        # Tombol Simpan
        if st.button("SIMPAN PERUBAHAN", use_container_width=True):
            if not verify_key:
                st.error("Verifikasi Gagal: License Key wajib diisi.")
            else:
                # Menggunakan mode signup di security.py untuk menimpa/update data
                # Jika password baru kosong, kita asumsikan user tidak ganti pass (logika ini tergantung security.py Anda)
                status = verify_user(new_email, new_pass, key=verify_key, mode="signup")
                
                if status == "SUCCESS_SIGNUP":
                    st.success("✅ Profil berhasil diperbarui!")
                    # Update session state lokal agar UI langsung berubah
                    st.session_state.user_data['nama'] = new_nama
                    st.session_state.user_data['email'] = new_email
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("❌ Gagal memperbarui profil. Pastikan License Key Anda benar.")

    # Tombol Kembali
    if st.button("⬅️ Kembali ke Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
