import streamlit as st
import datetime
from auth_app import show_login_screen
# Pastikan fungsi ini ada di file investasi.py dan kalkulator.py
from investasi import show_investasi 
from kalkulator import show_hpp

# --- 1. CONFIG (Wajib Paling Atas) ---
st.set_page_config(
    page_title="BizInvest VIP Suite", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# --- 2. ANTI-REFRESH SYSTEM ---
# Variabel ini akan menjaga status login meskipun halaman di-refresh
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'page' not in st.session_state:
    st.session_state.page = "dashboard"

# --- 3. LOGIKA TAMPILAN ---
if not st.session_state.authenticated:
    show_login_screen()
else:
    # --- SIDEBAR (Hanya untuk Info & Pengaturan) ---
    with st.sidebar:
        st.markdown("### 🛠️ PENGATURAN")
        st.caption(f"👤 Login as: {st.session_state.user_email}")
        
        # Widget Waktu & Tanggal
        now = datetime.datetime.now()
        st.info(f"📅 {now.strftime('%A, %d %B %Y')}\n\n🕒 {now.strftime('%H:%M')} WIB")
        
        st.write("---")
        with st.expander("ℹ️ Introduce & Credit"):
            st.write("**BizInvest VIP v2.0**")
            st.write("Developed by Reno Business Analyst")
            st.caption("© 2026 All Rights Reserved")
            
        with st.expander("🛡️ Privasi"):
            st.caption("Data Anda aman dan terenkripsi dalam sistem cloud kami.")

        st.write("---")
        if st.button("🚪 Keluar Aplikasi", use_container_width=True):
            st.session_state.authenticated = False
            st.rerun()

    # --- KONTEN UTAMA ---
    # Tombol Kembali ke Dashboard (Hanya muncul jika tidak di dashboard)
    if st.session_state.page != "dashboard":
        if st.button("⬅️ Kembali ke Menu Utama"):
            st.session_state.page = "dashboard"
            st.rerun()

    # 1. TAMPILAN MENU UTAMA (KARTU)
    if st.session_state.page == "dashboard":
        st.markdown("""
            <div style="text-align: center; padding: 20px;">
                <h1 style="color: #fbbf24; font-size: 3rem;">👑 VIP TERMINAL</h1>
                <p style="color: #94a3b8;">Sistem Analisis Bisnis & Investasi Profesional</p>
            </div>
        """, unsafe_allow_html=True)

        st.write("### Silakan Pilih Layanan:")
        
        # Desain Layout Kartu
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 10px solid #3b82f6; min-height: 180px;">
                    <h2 style="color: white;">📈 Terminal Analisis</h2>
                    <p style="color: #cbd5e1;">Pantau pergerakan aset, teknikal analisis, dan monitoring portofolio secara real-time.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("BUKA TERMINAL ANALISIS", use_container_width=True, type="primary"):
                st.session_state.page = "investasi"
                st.rerun()

        with col2:
            st.markdown("""
                <div style="background-color: #1e293b; padding: 20px; border-radius: 15px; border-left: 10px solid #10b981; min-height: 180px;">
                    <h2 style="color: white;">🧮 Kalkulator Bisnis</h2>
                    <p style="color: #cbd5e1;">Hitung HPP, proyeksi profit, dan analisis keuangan usaha Anda dengan akurat.</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("BUKA KALKULATOR BISNIS", use_container_width=True, type="primary"):
                st.session_state.page = "hpp"
                st.rerun()

    # 2. HALAMAN INVESTASI
    elif st.session_state.page == "investasi":
        st.subheader("📈 Terminal Analisis Aset")
        show_investasi()

    # 3. HALAMAN KALKULATOR
    elif st.session_state.page == "hpp":
        st.subheader("🧮 Kalkulator Proyeksi Bisnis")
        show_hpp()
        
