import streamlit as st
import time # Penyelamat agar tidak blank screen
from security import verify_activation
from investasi import show_investasi
from kalkulator import show_hpp

# Konfigurasi Halaman Dasar
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# CSS Premium Gold & Dark
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    .auth-card {
        background: #171f2d; padding: 40px; border-radius: 20px;
        border: 2px solid #fbbf24; text-align: center;
        box-shadow: 0 10px 25px rgba(251, 191, 36, 0.2);
    }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3em;
        background: linear-gradient(135deg, #fbbf24 0%, #d97706 100%);
        color: black; font-weight: bold; border: none;
    }
    </style>
""", unsafe_allow_html=True)

# State Management
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def show_login():
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.title("👑 VIP ACTIVATION")
        st.write("Sistem Autopilot: Masukkan Kode Lisensi Anda")
        
        license_key = st.text_input("LICENSE KEY", type="password", placeholder="Ketik Kode Anda di Sini")
        
        if st.button("AKTIVASI SEKARANG"):
            if license_key:
                with st.spinner("Menghubungkan ke Server Keamanan..."):
                    res = verify_activation(license_key)
                    
                    if res['status'] in ["VALID", "FIRST_TIME_LOCK"]:
                        st.session_state.authenticated = True
                        st.success("✅ AKSES DITERIMA!")
                        time.sleep(1)
                        st.rerun()
                    elif res['status'] == "LOCKED_OTHER_DEVICE":
                        st.error("❌ KODE TERKUNCI! Lisensi ini sudah terikat di perangkat lain.")
                    else:
                        st.error("❌ KODE TIDAK VALID! Pastikan kode benar.")
            else:
                st.warning("Mohon isi kode terlebih dahulu.")
        st.markdown("</div>", unsafe_allow_html=True)

# Logika Navigasi App
try:
    if not st.session_state.authenticated:
        show_login()
    else:
        if 'page' not in st.session_state: st.session_state.page = 'home'
        
        if st.session_state.page == 'home':
            st.markdown("<h1 style='text-align: center; color: #fbbf24; margin-top: 5vh;'>TERMINAL UTAMA</h1>", unsafe_allow_html=True)
            st.markdown("<p style='text-align: center;'>Pilih modul profesional Anda</p>", unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("📈 INVESTMENT TERMINAL"):
                    st.session_state.page = 'investasi'
                    st.rerun()
            with c2:
                if st.button("📦 BUSINESS CALCULATOR"):
                    st.session_state.page = 'hpp'
                    st.rerun()
        
        elif st.session_state.page == 'investasi':
            if st.button("⬅️ KEMBALI"): st.session_state.page = 'home'; st.rerun()
            show_investasi()
        
        elif st.session_state.page == 'hpp':
            if st.button("⬅️ KEMBALI"): st.session_state.page = 'home'; st.rerun()
            show_hpp()
except Exception as e:
    st.error(f"Terjadi kesalahan sistem: {e}")
    st.info("Pastikan file investasi.py dan kalkulator.py sudah ada di GitHub Anda.")
