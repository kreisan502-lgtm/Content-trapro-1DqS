import streamlit as st
import time
from datetime import datetime
import pytz

def show_main_dashboard():
    # --- HEADER ---
    st.markdown("""
        <div style="margin-top: -50px;">
            <h1 style="color: #fbbf24; margin-bottom: 0;">PRO TERMINAL</h1>
            <p style="color: #94a3b8;">Intelligence Asset & Business Analysis</p>
        </div>
    """, unsafe_allow_html=True)

    # --- WIDGET JAM (TARUH DI SIDEBAR AGAR RAPI) ---
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 🕒 Real-time Clock")
        placeholder_jam = st.empty() # Wadah untuk jam

    # --- MENU DATA MARKET (DENGAN FITUR SEMBUNYIKAN) ---
    # expanded=True artinya menu terbuka saat pertama kali dilihat
    with st.expander("📊 MARKET INTELLIGENCE", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("IHSG (IDX)", "7,240.12", "+0.42%")
            st.info("**IHSG:** Indikator utama kesehatan ekonomi Indonesia. Penting untuk melihat minat investor asing.")
            
        with col2:
            st.metric("GOLD (XAU/USD)", "$2,341.50", "-0.12%")
            st.info("**GOLD:** Aset pelindung nilai (Safe Haven). Pantau ini saat ekonomi dunia sedang tidak stabil.")
            
        with col3:
            st.metric("USD / IDR", "16,125.00", "0.00")
            st.info("**Kurs USD:** Sangat krusial untuk bisnismu ke depan, terutama untuk riset ekspor briket.")

    st.markdown("---")
    
    # --- LOGIKA JAM BERDETAK ---
    # Kita update jamnya tanpa mengganggu UI utama
    # Catatan: Di Streamlit, cara ini akan membuat spinner berputar terus, 
    # tapi jam akan terlihat 'hidup' (detik berjalan).
    
    tz_jkt = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz_jkt)
    jam_sekarang = now.strftime("%H:%M:%S")
    
    placeholder_jam.markdown(f"""
        <div style="background: #1e293b; padding: 15px; border-radius: 12px; border: 1px solid #fbbf24; text-align: center;">
            <h2 style="color: white; margin: 0; font-family: monospace;">{jam_sekarang}</h2>
            <p style="color: #fbbf24; margin: 0; font-size: 0.8rem;">WIB - JAKARTA</p>
        </div>
    """, unsafe_allow_html=True)

    # Trik agar jam update tiap 1 detik tanpa memacetkan menu lain
    time.sleep(1)
    st.rerun()
