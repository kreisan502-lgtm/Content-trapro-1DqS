import streamlit as st
import time
from security import verify_user
from investasi import show_investasi
from kalkulator import show_hpp

st.set_page_config(page_title="BizInvest VIP Suite", layout="centered")

# CSS Premium
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    .auth-container { background: #171f2d; padding: 30px; border-radius: 15px; border: 1px solid #fbbf24; }
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def show_auth_page():
    st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 MASUK", "📝 DAFTAR AKUN BARU"])
    
    with tab1:
        st.write("Silakan masuk dengan akun terdaftar")
        email_log = st.text_input("Email", key="l_email")
        pass_log = st.text_input("Password", type="password", key="l_pass")
        
        if st.button("LOGIN", use_container_width=True):
            with st.spinner("Memverifikasi..."):
                res = verify_user(email_log, pass_log, mode="login")
                if res == "SUCCESS_LOGIN":
                    st.session_state.authenticated = True
                    st.success("Selamat Datang!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Email atau Password salah!")

    with tab2:
        st.write("Gunakan Kode Aktivasi dari LYNK untuk mendaftar")
        reg_key = st.text_input("Kode Aktivasi (License Key)", placeholder="Contoh: BIZ-XXX-VIP")
        reg_email = st.text_input("Email Baru", placeholder="email@anda.com")
        reg_pass = st.text_input("Buat Password", type="password")
        
        if st.button("DAFTAR SEKARANG", use_container_width=True):
            if reg_key and reg_email and reg_pass:
                with st.spinner("Mendaftarkan Akun..."):
                    res = verify_user(reg_email, reg_pass, key=reg_key, mode="signup")
                    if res == "SUCCESS_SIGNUP":
                        st.success("Akun Berhasil Dibuat! Silakan login di tab MASUK.")
                    elif res == "KEY_ALREADY_USED":
                        st.error("Kode ini sudah pernah digunakan untuk mendaftar.")
                    else:
                        st.error("Kode Aktivasi tidak valid.")
            else:
                st.warning("Mohon lengkapi semua data.")

# Logika Navigasi
if not st.session_state.authenticated:
    show_auth_page()
else:
    # (Menu Utama Investasi & HPP seperti sebelumnya)
    st.sidebar.success(f"VIP Member Aktif")
    if st.sidebar.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
        
    # Tampilkan menu navigasi aplikasi kamu di sini
    st.title("Main Dashboard")
    # ... (tampilkan show_investasi() atau show_hpp())
