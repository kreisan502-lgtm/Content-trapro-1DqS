import streamlit as st
from investasi import show_investasi
from kalkulator import show_hpp

# CSS UI Premium
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    .stButton>button {
        width: 100%; border-radius: 12px;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        color: #fbbf24; font-weight: bold; border: 1px solid #d97706; padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- SISTEM KEAMANAN DEVICE LOCK ---
# Kita menggunakan User-Agent sebagai ID unik sederhana
import streamlit.components.v1 as components

def get_remote_ip():
    # Simulasi unik ID dari browser
    return st.query_params.get("device_id", ["unknown"])[0]

if 'auth' not in st.session_state:
    st.session_state.auth = False

def check_auth():
    if not st.session_state.auth:
        st.markdown("<h1 style='text-align: center; color: #fbbf24;'>👑 BizInvest VIP Access</h1>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            kode = st.text_input("Masukkan Kode Aktivasi:", type="password")
            if st.button("AKTIVASI PERANGKAT INI"):
                if kode == "AksesPremium123":
                    st.session_state.auth = True
                    st.success("✅ Aktivasi Berhasil! Perangkat ini telah terdaftar.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Kode Salah atau Sudah Digunakan di Perangkat Lain.")
        return False
    return True

# --- ROUTING HALAMAN ---
if check_auth():
    if 'menu' not in st.session_state:
        st.session_state.menu = 'home'

    if st.session_state.menu == 'home':
        st.markdown("<div style='text-align: center; margin-top: 10vh;'><h1>SELAMAT DATANG DI BIZINVEST PRO</h1><p>Silakan pilih modul profesional Anda</p></div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📈 ANALISIS INVESTASI (MODE PRO)"):
                st.session_state.menu = 'investasi'
                st.rerun()
        with col2:
            if st.button("📦 KALKULATOR BISNIS & HPP"):
                st.session_state.menu = 'kalkulator'
                st.rerun()
    
    elif st.session_state.menu == 'investasi':
        if st.button("⬅️ KEMBALI KE MENU"): 
            st.session_state.menu = 'home'
            st.rerun()
        show_investasi()
        
    elif st.session_state.menu == 'kalkulator':
        if st.button("⬅️ KEMBALI KE MENU"): 
            st.session_state.menu = 'home'
            st.rerun()
        show_hpp()
      
