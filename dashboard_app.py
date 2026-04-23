import streamlit as st
from datetime import datetime
import pytz

def show_main_dashboard():
    # --- LOGIKA WAKTU & PASAR ---
    tz_jkt = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz_jkt)
    current_time = now.strftime("%H:%M:%S")
    
    # Status Pasar (Senin-Jumat, 09:00 - 16:00 WIB)
    is_weekday = now.weekday() < 5
    is_market_open = is_weekday and (9 <= now.hour < 16)
    
    status_text = "PASAR BUKA" if is_market_open else "PASAR TUTUP"
    status_color = "#22c55e" if is_market_open else "#ef4444" # Hijau vs Merah

    # --- HEADER SECTION ---
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: -50px; padding: 10px 0;">
            <div>
                <h1 style="margin: 0; color: #fbbf24; font-size: 2rem; font-weight: 800; letter-spacing: -1px;">VIP TERMINAL</h1>
                <p style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Intelligence Asset & Business Analysis</p>
            </div>
            <div style="text-align: right; background: #1e293b; padding: 10px 20px; border-radius: 12px; border: 1px solid #334155;">
                <div style="color: #94a3b8; font-size: 0.75rem; font-weight: bold; margin-bottom: 2px;">WAKTU JAKARTA (WIB)</div>
                <div style="color: white; font-size: 1.2rem; font-family: monospace; font-weight: bold;">{current_time}</div>
                <div style="color: {status_color}; font-size: 0.7rem; font-weight: bold; letter-spacing: 1px;">● {status_text}</div>
            </div>
        </div>
        <hr style="margin: 20px 0; border: 0.5px solid #334155;">
    """, unsafe_allow_html=True)

    # --- METRICS BANNERS ---
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 15px; border-radius: 15px; border: 1px solid #334155;">
            <p style="color: #94a3b8; margin:0; font-size: 0.8rem;">IHSG (IDX)</p>
            <h3 style="margin:0; color: #22c55e;">7,240.12 <span style="font-size: 0.7rem;">+0.42%</span></h3>
        </div>""", unsafe_allow_html=True)
    with m2:
        st.markdown("""<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 15px; border-radius: 15px; border: 1px solid #334155;">
            <p style="color: #94a3b8; margin:0; font-size: 0.8rem;">GOLD (XAU/USD)</p>
            <h3 style="margin:0; color: #fbbf24;">$2,341.50 <span style="font-size: 0.7rem;">-0.12%</span></h3>
        </div>""", unsafe_allow_html=True)
    with m3:
        st.markdown("""<div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); padding: 15px; border-radius: 15px; border: 1px solid #334155;">
            <p style="color: #94a3b8; margin:0; font-size: 0.8rem;">USD / IDR</p>
            <h3 style="margin:0; color: white;">16,125.00</h3>
        </div>""", unsafe_allow_html=True)

    st.write("###")

    # --- MAIN NAVIGATION CARDS ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
            <div style="background: #1e293b; padding: 30px; border-radius: 20px; border: 1px solid #334155; min-height: 250px; position: relative; transition: 0.3s;">
                <div style="font-size: 40px; margin-bottom: 10px;">📈</div>
                <h2 style="color: white; margin-bottom: 10px;">Terminal Analisis</h2>
                <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">
                    Akses data teknikal saham, crypto, dan komoditas secara mendalam. Dilengkapi dengan indikator presisi untuk membantu pengambilan keputusan investasi Anda.
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Luncurkan Terminal 🚀", key="btn_inv", use_container_width=True):
            st.session_state.page = "investasi"
            st.rerun()

    with col2:
        st.markdown("""
            <div style="background: #1e293b; padding: 30px; border-radius: 20px; border: 1px solid #334155; min-height: 250px; position: relative;">
                <div style="font-size: 40px; margin-bottom: 10px;">🧮</div>
                <h2 style="color: white; margin-bottom: 10px;">Kalkulator Bisnis</h2>
                <p style="color: #94a3b8; font-size: 0.95rem; line-height: 1.6;">
                    Hitung Harga Pokok Produksi (HPP), Proyeksi Margin Profit, dan Analisis Break Even Point (BEP) untuk operasional manufaktur atau retail.
                </p>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Buka Kalkulator 🛠️", key="btn_hpp", use_container_width=True):
            st.session_state.page = "hpp"
            st.rerun()

    # --- FOOTER ---
    st.markdown("""
        <div style="margin-top: 50px; text-align: center; color: #475569; font-size: 0.8rem;">
            VIP Terminal v2.0 &copy; 2026 Professional Investment Suite.
        </div>
    """, unsafe_allow_html=True)
    
