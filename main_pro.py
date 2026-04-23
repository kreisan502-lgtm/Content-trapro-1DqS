import streamlit as st
from extra_streamlit_components import CookieManager
from auth_app import show_login_screen
import datetime

# --- 1. CONFIG ---
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# --- 2. INISIALISASI COOKIE (ID UNIK) ---
cookie_manager = CookieManager(key="main_cookie_auth")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# CEK COOKIE UNTUK AUTO-LOGIN
saved_email = cookie_manager.get("vip_user_email")
saved_nama = cookie_manager.get("vip_user_nama")

if saved_email and not st.session_state.authenticated:
    st.session_state.authenticated = True
    st.session_state.user_data = {"nama": saved_nama, "email": saved_email}
    st.session_state.page = "dashboard"

# --- 3. ROUTING ---
if not st.session_state.authenticated:
    show_login_screen(cookie_manager)
else:
    # --- SIDEBAR PRO (Menampilkan Nama & Email) ---
    with st.sidebar:
        user = st.session_state.get('user_data', {"nama": "User", "email": ""})
        nama_u = user.get('nama', 'User')
        email_u = user.get('email', '')
        
        inisial = nama_u[0].upper() if nama_u else "U"
        
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 12px; background-color: #1e293b; border-radius: 12px; border: 1px solid #334155; margin-bottom: 20px;">
                <div style="background-color: #fbbf24; color: #1e293b; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; margin-right: 12px;">{inisial}</div>
                <div style="overflow: hidden;">
                    <p style="margin: 0; color: white; font-weight: bold; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{nama_u}</p>
                    <p style="margin: 0; color: #94a3b8; font-size: 11px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{email_u}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)

        if st.sidebar.button("🏠 Dashboard Utama", use_container_width=True):
            st.session_state.page = "dashboard"; st.rerun()

        st.write("---")
        if st.sidebar.button("🚪 Keluar Aplikasi", use_container_width=True):
            cookie_manager.delete("vip_user_email")
            cookie_manager.delete("vip_user_nama")
            st.session_state.authenticated = False
            st.rerun()

    # --- KONTEN DASHBOARD ---
    # (Masukkan kode tombol Investasi & HPP kamu di sini)
    st.write("Selamat Datang!")
    
