import streamlit as st
import time
from security import verify_user

def show_settings():
    st.markdown("""
        <div style="margin-top: -50px;">
            <h1 style="color: #fbbf24; font-size: 2rem; font-weight: 800;">⚙️ Profil VIP</h1>
            <p style="color: #94a3b8; font-size: 0.9rem;">Kelola identitas dan keamanan akun Anda secara real-time.</p>
        </div>
        <hr style="border: 0.5px solid #334155; margin-bottom: 30px;">
    """, unsafe_allow_html=True)

    # 1. AMBIL DATA USER (Pastikan 'ref' ada)
    user = st.session_state.get('user_data', {"nama": "Member", "email": "", "ref": ""})
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}

    # Container Input Profil
    with st.container(border=True):
        # --- SEKSI NAMA ---
        col_n1, col_n2 = st.columns([5, 1])
        with col_n1:
            if st.session_state.edit_mode["nama"]:
                # Gunakan value tetap dari session agar tidak kosong saat rerun
                st.text_input("Ubah Nama Lengkap", value=user['nama'], key="input_nama")
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
                st.text_input("Ubah Email", value=user['email'], key="input_email")
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
                st.text_input("Password Baru", type="password", placeholder="Isi jika ingin ganti", key="input_pass")
            else:
                st.text_input("Password", value="********", disabled=True)
        with col_p2:
            st.write("###")
            if st.button("Ubah", key="btn_p"):
                st.session_state.edit_mode["pass"] = not st.session_state.edit_mode["pass"]
                st.rerun()

    # --- BAGIAN KONFIRMASI ---
    if any(st.session_state.edit_mode.values()):
        st.markdown("""
            <div style="background: #1e293b; padding: 20px; border-radius: 12px; border: 1px solid #fbbf24; margin-top: 20px;">
                <p style="color: #fbbf24; margin-bottom: 10px; font-weight: bold;">🔐 Konfirmasi Keamanan</p>
                <p style="color: #94a3b8; font-size: 0.8rem; margin-top: -10px;">Gunakan License Key asli Anda untuk menyimpan perubahan.</p>
            </div>
        """, unsafe_allow_html=True)
        
        v_key = st.text_input("License Key", type="password", placeholder="BIZ-XXXXXXX", key="confirm_key")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 SIMPAN PERUBAHAN", use_container_width=True):
                if not v_key:
                    st.error("License Key wajib diisi!")
                else:
                    # AMBIL DATA SECARA AMAN DARI SESSION STATE
                    # Jika user tidak mengaktifkan mode edit, gunakan data user asli
                    f_nama = st.session_state.input_nama if "input_nama" in st.session_state else user['nama']
                    f_email = st.session_state.input_email if "input_email" in st.session_state else user['email']
                    f_pass = st.session_state.input_pass if "input_pass" in st.session_state else ""
                    f_ref = user.get('ref') # Kunci Ref

                    if not f_ref:
                        st.warning("⚠️ Data Ref tidak ditemukan. Silakan Logout dan Login ulang terlebih dahulu.")
                    else:
                        with st.spinner("Menghubungkan ke server..."):
                            # PANGGIL KE SECURITY
                            res = verify_user(
                                email=f_email, 
                                password=f_pass, 
                                key=v_key, 
                                mode="signup", 
                                nama=f_nama, 
                                ref=f_ref
                            )
                            
                            if res == "SUCCESS_SIGNUP":
                                # UPDATE SESSION DATA
                                st.session_state.user_data['nama'] = f_nama
                                st.session_state.user_data['email'] = f_email
                                st.session_state.user_data['ref'] = f_ref 
                                
                                st.success(f"✅ Profil {f_nama} Berhasil Diperbarui!")
                                # Reset mode edit
                                st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}
                                time.sleep(2)
                                st.rerun()
                            else:
                                st.error("❌ Gagal Simpan. Cek License Key Anda atau coba lagi.")
        with c2:
            if st.button("✖ BATAL", use_container_width=True):
                st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}
                st.rerun()

    st.write("---")
    if st.button("⬅️ Kembali ke Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
