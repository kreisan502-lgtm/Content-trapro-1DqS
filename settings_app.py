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

    # 1. AMBIL DATA USER (Sangat Penting: Memastikan 'ref' ikut terbawa)
    user = st.session_state.get('user_data', {"nama": "Member", "email": "", "ref": ""})
    
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}

    # Container Input Profil
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
                new_pass = st.text_input("Password Baru", type="password", placeholder="Isi hanya jika ingin ganti sandi", key="input_pass")
            else:
                st.text_input("Password", value="********", disabled=True)
        with col_p2:
            st.write("###")
            if st.button("Ubah", key="btn_p"):
                st.session_state.edit_mode["pass"] = not st.session_state.edit_mode["pass"]
                st.rerun()

    # --- BAGIAN KONFIRMASI (MUNCUL JIKA ADA EDIT) ---
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
                    st.error("License Key wajib diisi sebagai verifikasi!")
                else:
                    # 2. LOGIKA FALLBACK DATA (Cegah data jadi kosong/None)
                    final_nama = st.session_state.get('input_nama', user['nama'])
                    final_email = st.session_state.get('input_email', user['email'])
                    final_pass = st.session_state.get('input_pass', "")
                    final_ref = user.get('ref') # Kunci Ref dari baris 15

                    with st.spinner("Sinkronisasi ke Google Sheets..."):
                        # 3. CALL SECURITY FUNCTION (Dengan Ref sebagai parameter wajib)
                        res = verify_user(
                            email=final_email, 
                            password=final_pass, 
                            key=v_key, 
                            mode="signup", 
                            nama=final_nama, 
                            ref=final_ref
                        )
                        
                        if res == "SUCCESS_SIGNUP":
                            # 4. UPDATE LOCAL SESSION (Agar Sidebar Langsung Ganti Nama)
                            st.session_state.user_data['nama'] = final_nama
                            st.session_state.user_data['email'] = final_email
                            # Ref tetap dijaga agar tidak hilang untuk edit berikutnya
                            st.session_state.user_data['ref'] = final_ref 
                            
                            st.success(f"✅ Profil {final_nama} Berhasil Diperbarui!")
                            st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}
                            time.sleep(2)
                            st.rerun()
                        else:
                            st.error("❌ Gagal Simpan. Pastikan License Key benar dan koneksi stabil.")
        with c2:
            if st.button("✖ BATAL", use_container_width=True):
                st.session_state.edit_mode = {"nama": False, "email": False, "pass": False}
                st.rerun()

    # Navigasi Kembali
    st.write("---")
    if st.button("⬅️ Kembali ke Dashboard", use_container_width=True):
        st.session_state.page = "dashboard"
        st.rerun()
        
