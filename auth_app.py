def show_login_screen():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🔐 LOGIN", "📝 DAFTAR", "🔑 LUPA PASSWORD"])
    
    with tab1:
        # Gunakan key unik (contoh: log_email)
        e_log = st.text_input("Email", key="log_email")
        p_log = st.text_input("Password", type="password", key="log_pass")
        if st.button("MASUK", use_container_width=True, key="btn_login"):
            # ... (logika login)
            pass

    with tab2:
        st.info("Gunakan License Key dari LYNK untuk mendaftar.")
        # Gunakan key unik (contoh: reg_key)
        r_key = st.text_input("License Key", key="reg_key")
        r_email = st.text_input("Email Baru", key="reg_email")
        r_pass = st.text_input("Buat Password", type="password", key="reg_pass")
        r_pin = st.text_input("Buat PIN (6 Digit)", type="password", key="reg_pin")
        if st.button("DAFTAR AKUN", use_container_width=True, key="btn_signup"):
            # ... (logika signup)
            pass

    with tab3:
        st.subheader("Reset Password")
        # Gunakan key unik (contoh: forgot_key)
        f_email = st.text_input("Email Terdaftar", key="forgot_email")
        f_key = st.text_input("License Key", key="forgot_key")
        f_pin = st.text_input("PIN Keamanan", type="password", key="forgot_pin")
        f_new_p = st.text_input("Password Baru", type="password", key="forgot_new_pass")
        if st.button("SETEL ULANG", use_container_width=True, key="btn_reset"):
            # ... (logika reset)
            pass
