import streamlit as st
from auth_app import show_login_screen, cookie_manager
from investasi import show_investasi
from kalkulator import show_hpp

st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# --- SISTEM CEK STATUS LOGIN ---
def init_auth():
    saved_user = cookie_manager.get("bizinvest_user")
    if saved_user and 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
        st.session_state.user_email = saved_user

init_auth()

# --- LOGIKA PERGANTIAN HALAMAN ---
if not st.session_state.get('authenticated'):
    show_login_screen()
else:
    # HALAMAN SETELAH LOGIN DIMULAI DI SINI
    st.sidebar.title("💎 VIP MEMBER")
    st.sidebar.write(f"User: {st.session_state.user_email}")
    
    menu = st.sidebar.radio("Pilih Modul:", ["Dashboard Utama", "Analisis Investasi", "Kalkulator HPP"])
    
    if st.sidebar.button("🚪 LOGOUT"):
        cookie_manager.delete("bizinvest_user")
        st.session_state.authenticated = False
        st.rerun()

    if menu == "Dashboard Utama":
        st.title("Selamat Datang di Terminal Pro")
        st.info("Gunakan menu di samping untuk mulai menganalisis.")
        
    elif menu == "Analisis Investasi":
        show_investasi()
        
    elif menu == "Kalkulator HPP":
        show_hpp()
