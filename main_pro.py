import streamlit as st
from auth_app import show_login_screen, cookie_manager
from investasi import show_investasi
from kalkulator import show_hpp

# Pengaturan dasar halaman (Harus paling atas)
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# --- 1. SISTEM AUTHENTICATION & SESSION ---
def init_app_state():
    # Cek cookie untuk auto-login
    saved_user = cookie_manager.get("bizinvest_user")
    if saved_user and 'authenticated' not in st.session_state:
        st.session_state.authenticated = True
        st.session_state.user_email = saved_user
    
    # Inisialisasi pengaturan default jika belum ada
    if 'setting_currency' not in st.session_state:
        st.session_state.setting_currency = "IDR"
    if 'setting_lang' not in st.session_state:
        st.session_state.setting_lang = "Indonesia"
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"

init_app_state()

# --- 2. LOGIKA TAMPILAN (LOGIN VS DASHBOARD) ---
if not st.session_state.get('authenticated'):
    show_login_screen()
else:
    # --- 3. SIDEBAR: GEAR SETTINGS & LOGOUT ---
    with st.sidebar:
        st.markdown("### ⚙️ PENGATURAN SISTEM")
        with st.expander("Preferensi Aplikasi", expanded=False):
            # Mata Uang (Mempengaruhi hitungan di saham_engine)
            st.session_state.setting_currency = st.radio(
                "Mata Uang (Currency):", 
                ["IDR", "USD"],
                index=0 if st.session_state.setting_currency == "IDR" else 1,
                help="Merubah tampilan harga saham secara otomatis."
            )
            
            # Bahasa (Mempengaruhi teks di seluruh aplikasi)
            st.session_state.setting_lang = st.selectbox(
                "Bahasa (Language):", 
                ["Indonesia", "English"],
                index=0 if st.session_state.setting_lang == "Indonesia" else 1
            )
            
            # Wilayah
            st.session_state.setting_region = st.selectbox(
                "Wilayah (Region):", 
                ["Indonesia (IDX)", "Global (Wall Street)"]
            )
        
        st.write("---")
        # Informasi User
        st.caption(f"👤 Akun: {st.session_state.user_email}")
        st.caption(f"🌍 Mode: {st.session_state.setting_lang} | {st.session_state.setting_currency}")
        
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            cookie_manager.delete("bizinvest_user")
            st.session_state.authenticated = False
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
                        Analisis Saham, Emas, & Crypto dengan pencarian otomatis dan kalkulasi risiko presisi.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Buka Terminal Analisis 🚀", use_container_width=True, key="btn_to_inv"):
                st.session_state.current_page = "investasi"
                st.rerun()

        with col2:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 25px; border-radius: 15px; border-left: 8px solid #10b981; min-height: 180px;">
                    <h2 style="margin:0; color: #10b981;">🧮 Kalkulator</h2>
                    <p style="color: #cbd5e1; font-size: 15px; margin-top: 10px;">
                        Hitung Harga Pokok Produksi (HPP) dan margin keuntungan bisnis Anda secara akurat.
                    </p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("Buka Kalkulator Bisnis 🛠️", use_container_width=True, key="btn_to_hpp"):
                st.session_state.current_page = "hpp"
                st.rerun()
        
        st.write("---")
        # Tips harian singkat
        st.info("💡 **Tips:** Gunakan tombol gear di sidebar untuk merubah tampilan mata uang ke Rupiah (IDR).")

    elif st.session_state.current_page == "investasi":
        # Navigasi kembali ke home
        if st.button("⬅️ Kembali ke Dashboard Utama", key="back_to_home_inv"):
            st.session_state.current_page = "home"
            st.rerun()
        
        # Memanggil file investasi.py
        show_investasi()

    elif st.session_state.current_page == "hpp":
        # Navigasi kembali ke home
        if st.button("⬅️ Kembali ke Dashboard Utama", key="back_to_home_hpp"):
            st.session_state.current_page = "home"
            st.rerun()
        
        # Memanggil file kalkulator.py (show_hpp)
        show_hpp()
    
