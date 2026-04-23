    with tab2:
        st.markdown("""
            <div style="background-color: #1e3a8a; padding: 15px; border-radius: 10px; border-left: 5px solid #3b82f6; margin-bottom: 20px;">
                <p style="color: white; margin: 0; font-size: 14px;">
                    💡 <b>Sistem Pendaftaran Otomatis:</b><br>
                    Masukkan License Key Anda, sistem akan memvalidasi Nama & Email Anda secara otomatis.
                </p>
            </div>
        """, unsafe_allow_html=True)

        r_key = st.text_input("License Key", key="signup_key_input")
        
        # Logika Cek Key Otomatis
        if r_key:
            from security import get_key_info
            info = get_key_info(r_key)
            
            if info:
                if info['status'] == "AKTIF":
                    st.success(f"Key Valid! Data ditemukan.")
                    # Menampilkan Nama & Email (Disabled agar tidak bisa diedit)
                    st.text_input("Nama Anda", value=info['nama'], disabled=True)
                    st.text_input("Email Anda", value=info['email'], disabled=True)
                    
                    r_pass = st.text_input("Buat Password Baru", type="password", key="signup_pass_input")
                    
                    if st.button("KONFIRMASI DAFTAR", use_container_width=True, key="btn_signup_submit"):
                        if r_pass:
                            res = verify_user(info['email'], r_pass, key=r_key, mode="signup")
                            if res == "SUCCESS_SIGNUP":
                                st.success("Pendaftaran Berhasil! Silakan Login.")
                                st.balloons()
                            else:
                                st.error(f"Gagal: {res}")
                        else:
                            st.warning("Silakan buat password terlebih dahulu.")
                else:
                    st.error("Key ini sudah terpakai atau diblokir.")
            else:
                st.warning("Key tidak ditemukan. Pastikan sudah klaim kode.")
                
