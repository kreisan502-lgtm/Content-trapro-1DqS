import streamlit as st
import datetime
from auth_app import show_login_screen
# Import halaman modul anda
# from investasi import show_investasi 
# from kalkulator import show_hpp

# --- 1. CONFIG (HARUS PALING ATAS) ---
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 2. ANTI-REFRESH SYSTEM (Kunci di sini) ---
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = {"nama": "", "email": ""}
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

# --- 3. LOGIKA ROUTING ---
if not st.session_state.authenticated:
    show_login_screen()
else:
    # --- SIDEBAR PRO (Gaya GitHub - Sesuai Gambar Referensi) ---
    with st.sidebar:
        nama_user = st.session_state.user_data['nama']
        email_user = st.session_state.user_data['email']
        inisial = nama_user[0].upper() if nama_user else "U"

        # Desain Header Profil
        st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 10px; background-color: #1e293b; border-radius: 12px; margin-bottom: 25px; border: 1px solid #334155;">
                <div style="width: 45px; height: 45px; background-color: #fbbf24; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: black; font-weight: bold; font-size: 20px; margin-right: 12px;">
                    {inisial}
                </div>
                <div style="overflow: hidden;">
                    <div style="font-weight: bold; color: white; font-size: 15px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{nama_user}</div>
                    <div style="font-size: 11px; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">{email_user}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigasi Sidebar
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "dashboard"; st.rerun()

        st.write("---")
        with st.expander("⚙️ PENGATURAN"):
            st.caption(f"🕒 {datetime.datetime.now().strftime('%H:%M')} WIB")
            st.button("🛡️ Privacy Policy", use_container_width=True)
            st.button("ℹ️ Credit & Info", use_container_width=True)
            
        st.write("---")
        if st.button("🚪 Sign Out", use_container_width=True, type="secondary"):
            st.session_state.authenticated = False
            st.session_state.user_data = {"nama": "", "email": ""}
            st.rerun()

    # --- KONTEN UTAMA (BODY) ---
    if st.session_state.page == "dashboard":
        st.markdown("<h1 style='text-align: center; color: #fbbf24; margin-top: -50px;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #94a3b8;'>BizInvest VIP Terminal v2.0</p>", unsafe_allow_html=True)
        st.write("---")
        
        # Menu Kartu di Tengah
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader("📈 Terminal Analisis")
                st.write("Pantau pergerakan aset & teknikal analisis real-time.")
                if st.button("BUKA TERMINAL", key="go_inv", use_container_width=True):
                    st.session_state.page = "investasi"; st.rerun()

        with col2:
            with st.container(border=True):
                st.subheader("🧮 Kalkulator Bisnis")
                st.write("Hitung HPP, proyeksi profit, dan analisis keuangan.")
                if st.button("BUKA KALKULATOR", key="go_hpp", use_container_width=True):
                    st.session_state.page = "hpp"; st.rerun()

    elif st.session_state.page == "investasi":
        if st.button("⬅️ Kembali ke Dashboard"): st.session_state.page = "dashboard"; st.rerun()
        st.info("Halaman Investasi Aktif")
        # show_investasi()

    elif st.session_state.page == "hpp":
        if st.button("⬅️ Kembali ke Dashboard"): st.session_state.page = "dashboard"; st.rerun()
        st.success("Halaman Kalkulator Aktif")
        # show_hpp()
        
