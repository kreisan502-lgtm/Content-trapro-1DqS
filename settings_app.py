import streamlit as st
import time
from security import verify_user

def show_settings():
    # Header minimalis dengan margin yang disesuaikan
    st.markdown("""
        <div style="margin-top: -60px; margin-bottom: 20px;">
            <h2 style="color: #fbbf24; font-weight: 800; margin-bottom: 0;">⚙️ Profil VIP</h2>
            <p style="color: #94a3b8; font-size: 0.85rem;">Kelola identitas dan keamanan akun VIP Anda.</p>
        </div>
    """, unsafe_allow_html=True)

    # Ambil data user dari session (Pastikan Ref ikut terbawa)
    user = st.session_state.get('user_data', {"nama": "Member", "email": "", "ref": ""})
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}

    # Style kustom untuk merapatkan tampilan antar baris
    st.markdown("""
        <style>
            [data-testid="stVerticalBlock"] > div { margin-top: -10px; }
            .stTextInput { margin-top: -15px; }
        </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # 1. ID VIP (Read Only)
        st.text_input("🆔 ID VIP (Order ID)", value=user.get('ref', 'Tidak Terdeteksi'), disabled=True, key="display_ref_id")
        st.write("---")

        # 2. SEKSI NAMA
        c_n1, c_n2 = st.columns([4, 1])
        with c_n1:
            if st.session_state.edit_mode["nama"]:
                st.text_input("Nama Lengkap", value=user['nama'], key="input_nama_edit")
            else:
                st.text_input("Nama Lengkap", value=user['nama'], disabled=True, key="display_nama")
        with c_n2:
            st.write("###") 
            if st.button("Ubah", key="btn_ubah_nama", use_container_width=True):
                st.session_state.edit_mode["nama"] = not st.session_state.edit_mode["nama"]
                st.rerun()

        # 3. SEKSI EMAIL
        c_e1, c_e2 = st.columns([4, 1])
        with c_e1:
            if st.session_state.edit_mode["email"]:
                st.text_input("Email", value=user['email'], key="input_email_edit")
            else:
                st.text_input("Email", value=user['email'], disabled=True, key="display_email")
        with c_e2:
            st.write("###")
            if st.button("Ubah", key="btn_ubah_email", use_container_width=True):
                st.session_state.edit_mode["email"] = not st.session_state.edit_mode["email"]
                st.rerun()

        # 4. SEKSI PASSWORD
        c_p1, c_p2 = st.columns([4, 1])
        with c_p1:
            if st.session_state.edit_mode["pass"]:
                st.text_input("Password Baru", type="password", placeholder="Ketik sandi baru...", key="input_pass_edit")
            else:
                st.text_input("Password", value="********", disabled=True, key="display_pass")
        with c_p2:
            st.write("###")
            if st.button("Ubah", key="btn_ubah_pass", use_container_width=True):
                st.session_state.edit_mode["pass"] = not st.session_state.edit_mode["pass"]
                st.rerun()

    # Form Konfirmasi (Hanya muncul jika salah satu edit_mode aktif)
    if any(st.session_state.edit_mode.values()):
        st.write("---")
        with st.container():
            st.info("🔐 Konfirmasi Keamanan")
            v_key = st.text_input("License Key", type="password", placeholder="BIZ-XXXXXXX", key="confirm_key_settings")
            
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                # Key unik untuk tombol simpan
                if st.button("💾 SIMPAN", use_container_width=True, key="btn_save_final_profile"):
                    if not v_key:
                        st.error("License Key wajib diisi!")
                    else:
                        # Ambil data dari input jika mode edit aktif, jika tidak pakai data lama
                        f_nama = st.session_state.get('input_nama_edit', user['nama'])
                        f_email = st.session_state.get('input_email_edit', user['email'])
                        f_pass = st.session_state.get('input_pass_edit', "")
                        f_ref = user.get('ref')

                        with st.spinner("Mensinkronisasi data..."):
                            res = verify_user(email=f_email, password=f_pass, key=v_key, mode="signup", nama=f_nama, ref=f_ref)
                            if res == "SUCCESS_SIGNUP":
                                # Update Session State agar sidebar & UI langsung berubah
                                st.session_state.user_data.update({"nama": f_nama, "email": f_email, "ref": f_ref})
                                st.success("Profil Berhasil Diperbarui!")
                                # Reset mode edit ke False
                                st.session_state.edit_mode = {k: False for k in st.session_state.edit_mode}
                                time.sleep(1.5)
                                st.rerun()
                            else:
                                st.error("Gagal menyimpan perubahan. Periksa License Key Anda.")
                                
            with act_col2:
                # Key unik untuk tombol batal
                if st.button("✖ BATAL", use_container_width=True, key="btn_cancel_settings"):
                    st.session_state.edit_mode = {k: False for k in st.session_state.edit_mode}
                    st.rerun()

    st.write("")
    # Tombol kembali dengan key unik
    if st.button("⬅️ Kembali ke Dashboard", use_container_width=True, key="btn_back_to_dash"):
        st.session_state.page = "dashboard"
        st.rerun()
        
