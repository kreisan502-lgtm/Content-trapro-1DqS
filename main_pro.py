import streamlit as st
from auth_app import show_login_screen
from investasi import show_investasi
from kalkulator import show_hpp

# Pengaturan dasar halaman (Harus paling atas)
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 1. SISTEM SESSION INITIALIZATION ---
def init_app_state():
    # Inisialisasi status login jika belum ada
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Inisialisasi pengaturan default jika belum ada
    if 'setting_currency' not in st.session_state:
        st.session_state.setting_currency = "IDR"
    if 'setting_lang' not in st.session_state:
        st.session_state.setting_lang = "Indonesia"
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"

init_app_state()

# --- 2. LOGIKA TAMPILAN (LOGIN VS DASHBOARD) ---
if not st.session_state.authenticated:
    show_login_screen()
else:
    # --- 3. SIDEBAR: SETTINGS & LOGOUT ---
    with st.sidebar:
        st.markdown("### ⚙️ PENGATURAN SISTEM")
        with st.expander("Preferensi Aplikasi", expanded=False):
            st.session_state.setting_currency = st.radio(
                "Mata Uang (Currency):", 
                ["IDR", "USD"],
                index=0 if st.session_state.setting_currency == "IDR" else 1
            )
            
            st.session_state.setting_lang = st.selectbox(
                "Bahasa (Language):", 
                ["Indonesia", "English"],
                index=0 if st.session_state.setting_lang == "Indonesia" else 1
            )
            
            st.session_state.setting_region = st.selectbox(
                "Wilayah (Region):", 
                ["Indonesia (IDX)", "Global (Wall Street)"]
            )
        
        st.write("---")
        st.caption(f"👤 Akun: {st.session_state.user_email}")
        st.caption(f"🌍 Mode: {st.session_state.setting_lang} | {st.session_state.setting_currency}")
        
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            # Reset session state
            st.session_state.authenticated = False
            st.session_state.user_email = None
            st.rerun()

    # --- 4. HEADER DINAMIS ---
    title_text = "DASHBOARD UTAMA" if st.session_state.setting_lang == "Indonesia" else "MAIN DASHBOARD"
    st.markdown(f"""
        <div style="text-align: center; padding: 10px; margin-bottom: 20px;">
            <h1 style="color: #fbbf24; margin-bottom: 0;">👑 {title_text}</h1>
            <p style="color: #94a3b8; font-size: 14px;">BizInvest VIP Terminal v2.0</p>
        </div>
    """, unsafe_allow_html=True)

    # --- 5. NAVIGASI HALAMAN ---
    if st.session_state.current_page == "home":
        st.write("---")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 25px; border-radius: 15px; border-left: 8px solid #fbbf24; min-height: 180px;">
                    <h2 style="margin:0; color: #fbbf24;">📈 Investasi</h2>
                    <p style="color: #cbd5e1; font-size: 15px; margin-top: 10px;">
                        Analisis Saham, Emas, & Crypto dengan kalkulasi risiko presisi.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Buka Terminal Analisis 🚀", use_container_width=True):
                st.session_state.current_page = "investasi"
                st.rerun()

        with col2:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 25px; border-radius: 15px; border-left: 8px solid #10b981; min-height: 180px;">
                    <h2 style="margin:0; color: #10b981;">🧮 Kalkulator</h2>
                    <p style="color: #cbd5e1; font-size: 15px; margin-top: 10px;">
                        Hitung Harga Pokok Produksi (HPP) dan margin keuntungan bisnis Anda.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Buka Kalkulator Bisnis 🛠️", use_container_width=True):
                st.session_state.current_page = "hpp"
                st.rerun()
        
        st.write("---")
        st.info("💡 **Tips:** Gunakan sidebar untuk merubah tampilan mata uang.")

    elif st.session_state.current_page == "investasi":
        if st.button("⬅️ Kembali ke Dashboard Utama"):
            st.session_state.current_page = "home"
            st.rerun()
        show_investasi()

    elif st.session_state.current_page == "hpp":
        if st.button("⬅️ Kembali ke Dashboard Utama"):
            st.session_state.current_page = "home"
            st.rerun()
        show_hpp()
        
