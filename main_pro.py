# ... (bagian CSS tetap sama)

def show_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.title("👑 VIP ACTIVATION")
        st.write("Masukkan kode yang Anda terima dari LYNK")
        
        license_key = st.text_input("LICENSE KEY", type="password")
        
        if st.button("AKTIVASI"):
            res = verify_activation(license_key)
            
            if res['status'] == "VALID":
                st.session_state.authenticated = True
                st.rerun()
                
            elif res['status'] == "FIRST_TIME_LOCK":
                st.success("✅ AKTIVASI BERHASIL!")
                st.info(f"Lisensi Anda telah dikunci secara otomatis ke perangkat ini.")
                st.write(f"Device ID Anda: {res['device_id']}")
                # Karena kita tidak pakai API Write, user cukup klik lanjut
                st.session_state.authenticated = True
                st.rerun()
                
            elif res['status'] == "LOCKED_OTHER_DEVICE":
                st.error("❌ KODE SUDAH TERPAKAI!")
                st.write("Lisensi ini sudah terikat dengan perangkat lain. 1 Lisensi = 1 Perangkat.")
            else:
                st.error("❌ Kode tidak valid.")
        st.markdown("</div>", unsafe_allow_html=True)
