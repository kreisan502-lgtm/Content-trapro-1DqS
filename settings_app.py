import streamlit as st
import time
from security import verify_user

def show_settings():
    st.markdown("""
        <div style="margin-top: -50px;">
            <h1 style="color: #fbbf24; font-size: 2rem; font-weight: 800;">⚙️ Profil VIP</h1>
            <p style="color: #94a3b8; font-size: 0.9rem;">Kelola identitas dan keamanan akun Anda.</p>
        </div>
        <hr style="border: 0.5px solid #334155; margin-bottom: 30px;">
    """, unsafe_allow_html=True)

    # Ambil data user saat ini
    user = st.session_state.get('user_data', {"nama": "Member", "email": ""})
    
    # Inisialisasi state agar data tidak hilang saat refresh
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}

    with st.container(border=True):
        # --- SEKSI NAMA ---
        col_n1, col_n2 = st.columns([5, 1])
        with col_n1:
            if st.session_state.edit_mode["nama"]:
                new_nama = st.text_input("Ubah Nama Lengkap", value=user['nama'], key="input_nama")
            else:
                st.text_input("Nama Lengkap", value=user['nama'], disabled=True)
        with col_n2:
            st.write("###")
            if st.button("Ubah", key="btn_n"):
                st.session_state.edit_mode["nama"] = not st.session_state.edit_mode["nama"]
                st.rerun()

        # --- SEKSI EMAIL ---
        col_e1, col_e2 = st.columns([5, 1])
        with col_e1:
            if st.session_state.edit_mode["email"]:
                new_email = st.text_input("Ubah Email", value=user['email'], key="input_email")
            else:
                st.text_input("Email", value=user['email'], disabled=True)
        with col_e2:
            st.write("###")
            if st.button("Ubah", key="btn_e"):
                st.session_state.edit_mode["email"] = not st.session_state.edit_mode["email"]
                st.rerun()

        # --- SEKSI PASSWORD ---
        col_p1, col_p2 = st.columns([5, 1])
        with col_p1:
            if st.session_state.edit_mode["pass"]:
                new_pass = st.text_input("Password Baru", type="password", placeholder="Ketik sandi baru...", key="input_pass")
            else:
                st.text_input("Password", value="********", disabled=True)
        with col_p2:
            st.write("###")
            if st.button("Ubah", key="btn_p"):
                st.session_state.edit_mode["pass"] = not st.session_state.edit_mode["pass"]
                st.rerun()

    # Tampilkan Verifikasi hanya jika ada yang sedang diubah
    if any(st.session_state.edit_mode.values()):
        st.markdown("""
            <div style="background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #fbbf24; margin-top: 20px;">
                <p style="color: #fbbf24; margin-bottom: 10px; font-weight: bold;">🔐 Konfirmasi Perubahan</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: -10px;">Masukkan License Key untuk memverifikasi bahwa ini benar Anda.</p>
            </div>
        """, unsafe_allow_html=True)
        
        v_key = st.text_input("License Key", type="password", placeholder="BIZ-XXXXXXX")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 SIMPAN PERUBAHAN", use_container_width=True):
                if not v_key:
                    st.error("License Key wajib diisi!")
                else:
                    # LOGIKA PENTING: Jika tidak diubah, gunakan data lama (User Data)
                    final_nama = st.session_state.get('input_nama', user['nama'])
                    final_email = st.session_state.get('input_email', user['email'])
                    # Untuk password, jika tidak diubah kirim string kosong (tergantung security.py anda)
                    final_pass = st.session_state.get('input_pass', "")

                    with st.spinner("Menyimpan..."):
                        # Memanggil fungsi update ke database
                        res = verify_user(final_email, final_pass, key=v_key, mode="signup")
                        
                        if res == "SUCCESS_SIGNUP":
                            st.success("Perubahan Berhasil Disimpan!")
                            # Update Session State agar UI langsung berubah
                            st.session_state.user_data = {"nama": final_nama, "email": final_email}
                            st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("Gagal. Pastikan License Key Anda benar.")
        with c2:
            if st.button("✖ BATAL", use_container_width=True):
                st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}
                st.rerun()

    if st.button("⬅️ Kembali ke Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
        
