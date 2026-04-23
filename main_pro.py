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
    # --- SIDEBAR: SETTINGS (GEAR) & LOGOUT ---
    with st.sidebar:
        st.markdown("### ⚙️ PENGATURAN")
        with st.expander("Preferensi Aplikasi"):
            # Pilih Mata Uang (Global State)
            st.session_state.setting_currency = st.radio(
                "Mata Uang Utama:", 
                ["IDR", "USD"],
                index=0 if st.session_state.get('setting_currency', 'IDR') == 'IDR' else 1
            )
            
            # Pilih Bahasa
            st.session_state.setting_lang = st.selectbox(
                "Bahasa:", 
                ["Indonesia", "English"]
            )
            
            # Pilih Wilayah Default
            st.session_state.setting_region = st.selectbox(
                "Wilayah:", 
                ["Indonesia (IDX)", "Global (Wall Street)"]
            )
        
        st.write("---")
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            cookie_manager.delete("bizinvest_user")
            st.session_state.authenticated = False
            st.rerun()

    # --- HEADER DASHBOARD ---
    st.markdown(f"""
        <div style="text-align: center; padding: 20px;">
            <h1 style="color: #fbbf24; margin-bottom: 0;">PRO TERMINAL DASHBOARD</h1>
            <p style="color: #94a3b8;">VIP Access: {st.session_state.user_email}</p>
        </div>
    """, unsafe_allow_html=True)

    # Navigasi halaman
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"

    # --- KONTEN HALAMAN ---
    if st.session_state.current_page == "home":
        st.write("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #fbbf24; margin-bottom: 10px; min-height: 150px;">
                    <h3 style="margin:0; color: #fbbf24;">📈 Analisis Investasi</h3>
                    <p style="font-size: 14px; color: #cbd5e1;">Pencarian otomatis, data fundamental, dan analisis risiko cerdas.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Buka Terminal Investasi 🚀", use_container_width=True, key="nav_inv"):
                st.session_state.current_page = "investasi"
                st.rerun()

        with col2:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #10b981; margin-bottom: 10px; min-height: 150px;">
                    <h3 style="margin:0; color: #10b981;">🧮 Kalkulator HPP</h3>
                    <p style="font-size: 14px; color: #cbd5e1;">Hitung margin keuntungan dan biaya produksi secara profesional.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Buka Kalkulator Bisnis 🛠️", use_container_width=True, key="nav_hpp"):
                st.session_state.current_page = "hpp"
                st.rerun()
        
        st.write("---")
        st.caption(f"Status: Aktif | Mata Uang: {st.session_state.get('setting_currency', 'IDR')} | Region: {st.session_state.get('setting_region', 'IDR')}")

    elif st.session_state.current_page == "investasi":
        if st.button("⬅️ Kembali ke Dashboard Utama", key="back_home"):
            st.session_state.current_page = "home"
            st.rerun()
        show_investasi()

    elif st.session_state.current_page == "hpp":
        if st.button("⬅️ Kembali ke Dashboard Utama", key="back_home_hpp"):
            st.session_state.current_page = "home"
            st.rerun()
        show_hpp()
