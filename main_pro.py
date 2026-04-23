import streamlit as st
import time
from security import verify_activation
from investasi import show_investasi
from kalkulator import show_hpp

st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")

# CSS Premium Gold & Dark
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    .auth-card {
        background: #171f2d; padding: 30px; border-radius: 15px;
        border: 1px solid #fbbf24; text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

def show_login():
    st.markdown("<br><br>", unsafe_allow_html=True)
    _, col2, _ = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
        st.title("👑 VIP ACCESS")
        st.write("Silakan masukkan Kode Aktivasi Anda")
        
        license_key = st.text_input("LICENSE KEY", placeholder="CONTOH: VIP-888", label_visibility="collapsed")
        
        if st.button("AKTIVASI SEKARANG"):
            with st.spinner("Memverifikasi Lisensi..."):
                res = verify_activation(license_key)
                
                if res['status'] == "VALID":
                    st.session_state.authenticated = True
                    st.success("✅ Selamat Datang Kembali!")
                    time.sleep(1)
                    st.rerun()
                
                elif res['status'] == "REGISTER_NEW":
                    st.warning("⚠️ Perangkat Belum Terdaftar!")
                    st.info(f"Kirimkan ID ini ke Admin untuk dikunci ke HP ini: \n\n **{res['device_id']}**")
                    st.write("Status: Kode valid, tapi butuh pendaftaran perangkat.")
                
                elif res['status'] == "LOCKED_OTHER_DEVICE":
                    st.error("❌ AKSES DITOLAK: Kode ini sudah terkunci di perangkat lain.")
                
                else:
                    st.error("❌ Kode Aktivasi Tidak Valid.")
        st.markdown("</div>", unsafe_allow_html=True)

# Logika Navigasi
if not st.session_state.authenticated:
    show_login()
else:
    # Menu Utama setelah sukses login
    if 'page' not in st.session_state: st.session_state.page = 'home'
    
    if st.session_state.page == 'home':
        st.markdown("<h1 style='text-align: center; color: #fbbf24;'>MAIN TERMINAL</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📈 INVESTMENT PRO"):
                st.session_state.page = 'investasi'
                st.rerun()
        with c2:
            if st.button("📦 BUSINESS HPP"):
                st.session_state.page = 'hpp'
                st.rerun()
    
    elif st.session_state.page == 'investasi':
        if st.button("⬅️ MENU"): st.session_state.page = 'home'; st.rerun()
        show_investasi()
    
    elif st.session_state.page == 'hpp':
        if st.button("⬅️ MENU"): st.session_state.page = 'home'; st.rerun()
        show_hpp()
        
