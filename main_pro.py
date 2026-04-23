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
    # --- HEADER DASHBOARD ---
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #fbbf24; margin-bottom: 0;">PRO TERMINAL DASHBOARD</h1>
            <p style="color: #94a3b8;">Selamat datang kembali, {st.session_state.user_email}</p>
        </div>
    """, unsafe_allow_html=True)

    # Inisialisasi session state untuk navigasi halaman jika belum ada
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"

    # Tombol Logout di Sidebar tetap ada sebagai cadangan
    if st.sidebar.button("🚪 Keluar Aplikasi"):
        cookie_manager.delete("bizinvest_user")
        st.session_state.authenticated = False
        st.rerun()

    # --- LOGIKA NAVIGASI HALAMAN ---
    if st.session_state.current_page == "home":
        # TAMPILAN MENU UTAMA (KARTU)
        st.write("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #fbbf24; margin-bottom: 10px;">
                    <h3 style="margin:0;">📈 Analisis Investasi</h3>
                    <p style="font-size: 14px; color: #cbd5e1;">Analisis teknikal saham dan pergerakan harga real-time.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Buka Analisis Saham 🚀", use_container_width=True, key="nav_inv"):
                st.session_state.current_page = "investasi"
                st.rerun()

        with col2:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #10b981; margin-bottom: 10px;">
                    <h3 style="margin:0;">🧮 Kalkulator HPP</h3>
                    <p style="font-size: 14px; color: #cbd5e1;">Hitung harga pokok produksi dan margin keuntungan bisnis.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Buka Kalkulator HPP 🛠️", use_container_width=True, key="nav_hpp"):
                st.session_state.current_page = "hpp"
                st.rerun()
        
        st.write("---")
        st.caption("Informasi Akun: VIP Member Active | Auto-Sync Cloud Database")

    # --- HALAMAN MODUL ---
    elif st.session_state.current_page == "investasi":
        if st.button("⬅️ Kembali ke Dashboard"):
            st.session_state.current_page = "home"
            st.rerun()
        show_investasi()

    elif st.session_state.current_page == "hpp":
        if st.button("⬅️ Kembali ke Dashboard"):
            st.session_state.current_page = "home"
            st.rerun()
        show_hpp()
