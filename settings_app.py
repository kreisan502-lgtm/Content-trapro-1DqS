import streamlit as st
import time
from security import verify_user

def show_settings():
    st.markdown("""
        <div style="margin-top: -50px;">
            <h1 style="color: #fbbf24; font-size: 2rem; font-weight: 800;">⚙️ Pengaturan Profil</h1>
            <p style="color: #94a3b8; font-size: 0.9rem;">Kelola informasi profil Anda dengan aman.</p>
        </div>
        <hr style="border: 0.5px solid #334155; margin-bottom: 30px;">
    """, unsafe_allow_html=True)

    user = st.session_state.get('user_data', {"nama": "Member", "email": ""})

    # --- Container Data Profil ---
    with st.container(border=True):
        st.subheader("Data Akun")
        
        # 1. Baris Nama
        col_n1, col_n2 = st.columns([4, 1])
        with col_n1:
            if st.session_state.get('edit_nama'):
                new_nama = st.text_input("Ubah Nama Lengkap", value=user['nama'], key="in_nama")
            else:
                st.text_input("Nama Lengkap", value=user['nama'], disabled=True, key="dis_nama")
        with col_n2:
            st.write("###") # Penyeimbang jarak
            if st.button("Ubah", key="btn_edit_nama"):
                st.session_state.edit_nama = not st.session_state.get('edit_nama', False)
                st.rerun()

        # 2. Baris Email
        col_e1, col_e2 = st.columns([4, 1])
        with col_e1:
            if st.session_state.get('edit_email'):
                new_email = st.text_input("Ubah Email Baru", value=user['email'], key="in_email")
            else:
                st.text_input("Email Terdaftar", value=user['email'], disabled=True, key="dis_email")
        with col_e2:
            st.write("###")
            if st.button("Ubah", key="btn_edit_email"):
                st.session_state.edit_email = not st.session_state.get('edit_email', False)
                st.rerun()

        # 3. Baris Password
        col_p1, col_p2 = st.columns([4, 1])
        with col_p1:
            if st.session_state.get('edit_pass'):
                new_pass = st.text_input("Password Baru", type="password", key="in_pass")
            else:
                st.text_input("Password", value="********", disabled=True, key="dis_pass")
        with col_p2:
            st.write("###")
            if st.button("Ubah", key="btn_edit_pass"):
                st.session_state.edit_pass = not st.session_state.get('edit_pass', False)
                st.rerun()

    # --- Area Konfirmasi (Hanya muncul jika ada yang diubah) ---
    if st.session_state.get('edit_nama') or st.session_state.get('edit_email') or st.session_state.get('edit_pass'):
        st.write("---")
        st.markdown("""
            <div style="background-color: #d1ecf1; color: #0c5460; padding: 15px; border-radius: 8px; border: 1px solid #bee5eb; margin-bottom: 20px;">
                <b>🔒 Verifikasi Perubahan:</b><br>
                Masukkan <b>License Key</b> Anda untuk menyimpan perubahan data di atas.
            </div>
        """, unsafe_allow_html=True)
        
        v_key = st.text_input("License Key Verifikasi", type="password", placeholder="BIZ-XXXXXXX")
        
        c_save, c_cancel = st.columns(2)
        with c_save:
            if st.button("💾 SIMPAN PERUBAHAN", use_container_width=True):
                if v_key:
                    # Ambil nilai baru atau gunakan nilai lama jika tidak diedit
                    final_nama = st.session_state.get('in_nama', user['nama'])
                    final_email = st.session_state.get('in_email', user['email'])
                    final_pass = st.session_state.get('in_pass', "")
                    
                    with st.spinner("Mengupdate data..."):
                        res = verify_user(final_email, final_pass, key=v_key, mode="signup")
                        if res == "SUCCESS_SIGNUP":
                            st.success("Berhasil! Data Anda telah diperbarui.")
                            # Reset state edit
                            st.session_state.edit_nama = False
                            st.session_state.edit_email = False
                            st.session_state.edit_pass = False
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("Gagal update. Pastikan License Key benar.")
                else:
                    st.warning("Masukkan License Key untuk memverifikasi.")
        
        with c_cancel:
            if st.button("✖ BATAL", use_container_width=True):
                st.session_state.edit_nama = False
                st.session_state.edit_email = False
                st.session_state.edit_pass = False
                st.rerun()

    st.write("###")
    if st.button("⬅️ Kembali ke Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
        
