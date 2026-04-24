import streamlit as st
import time
from security import verify_user

def show_settings():
    # Header minimalis
    st.markdown("""
        <div style="margin-top: -60px; margin-bottom: 20px;">
            <h2 style="color: #fbbf24; font-weight: 800; margin-bottom: 0;">⚙️ Profil VIP</h2>
            <p style="color: #94a3b8; font-size: 0.85rem;">Kelola identitas akun VIP Anda.</p>
        </div>
    """, unsafe_allow_html=True)

    user = st.session_state.get('user_data', {"nama": "Member", "email": "", "ref": ""})
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}

    # Style kustom untuk merapatkan komponen
    st.markdown("""
        <style>
            [data-testid="stVerticalBlock"] > div { margin-top: -10px; }
            .stTextInput { margin-top: -15px; }
        </style>
    """, unsafe_allow_html=True)

    with st.container(border=True):
        # 1. ID VIP (Read Only) - Tetap satu baris penuh untuk visibilitas
        st.text_input("🆔 ID VIP (Order ID)", value=user.get('ref', 'Tidak Terdeteksi'), disabled=True)
        st.write("---")

        # 2. SEKSI NAMA (Berdampingan)
        c_n1, c_n2 = st.columns([4, 1])
        with c_n1:
            if st.session_state.edit_mode["nama"]:
                st.text_input("Nama Lengkap", value=user['nama'], key="input_nama")
            else:
                st.text_input("Nama Lengkap", value=user['nama'], disabled=True)
        with c_n2:
            st.write("###") # Menyejajarkan tombol dengan input
            if st.button("Ubah", key="btn_n", use_container_width=True):
                st.session_state.edit_mode["nama"] = not st.session_state.edit_mode["nama"]
                st.rerun()

        # 3. SEKSI EMAIL (Berdampingan)
        c_e1, c_e2 = st.columns([4, 1])
        with c_e1:
            if st.session_state.edit_mode["email"]:
                st.text_input("Email", value=user['email'], key="input_email")
            else:
                st.text_input("Email", value=user['email'], disabled=True)
        with c_e2:
            st.write("###")
            if st.button("Ubah", key="btn_e", use_container_width=True):
                st.session_state.edit_mode["email"] = not st.session_state.edit_mode["email"]
                st.rerun()

        # 4. SEKSI PASSWORD (Berdampingan)
        c_p1, c_p2 = st.columns([4, 1])
        with c_p1:
            if st.session_state.edit_mode["pass"]:
                st.text_input("Password", type="password", placeholder="Baru...", key="input_pass")
            else:
                st.text_input("Password", value="********", disabled=True)
        with c_p2:
            st.write("###")
            if st.button("Ubah", key="btn_p", use_container_width=True):
                st.session_state.edit_mode["pass"] = not st.session_state.edit_mode["pass"]
                st.rerun()

    # Form Konfirmasi (Hanya muncul jika ada perubahan)
    if any(st.session_state.edit_mode.values()):
        st.write("---")
        with st.container():
            st.info("🔐 Konfirmasi Keamanan")
            v_key = st.text_input("License Key", type="password", placeholder="BIZ-XXXXXXX", key="confirm_key")
            
            # Tombol Aksi Sejajar
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                if st.button("💾 SIMPAN", use_container_width=True):
                    if not v_key:
                        st.error("Wajib diisi!")
                    else:
                        f_nama = st.session_state.get('input_nama', user['nama'])
                        f_email = st.session_state.get('input_email', user['email'])
                        f_pass = st.session_state.get('input_pass', "")
                        f_ref = user.get('ref')

                        with st.spinner("Proses..."):
                            res = verify_user(email=f_email, password=f_pass, key=v_key, mode="signup", nama=f_nama, ref=f_ref)
                            if res == "SUCCESS_SIGNUP":
                                st.session_state.user_data.update({"nama": f_nama, "email": f_email, "ref": f_ref})
                                st.success("Update Berhasil!")
                                st.session_state.edit_mode = {k: False for k in st.session_state.edit_mode}
                                time.sleep(1.5); st.rerun()
                            else:
                                st.error("Gagal simpan!")
            with act_col2:
                if st.button("✖ BATAL", use_container_width=True):
                    st.session_state.edit_mode = {k: False for k in st.session_state.edit_mode}
                    st.rerun()

    st.write("")
    if st.button("⬅️ Kembali ke Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"; st.rerun()
