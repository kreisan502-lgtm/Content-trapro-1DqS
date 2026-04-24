import streamlit as st
import time
from datetime import datetime
import pytz

def show_main_dashboard():
    # --- LOGIKA WAKTU & TANGGAL ---
    tz_jkt = pytz.timezone('Asia/Jakarta')
    now = datetime.now(tz_jkt)
    
    # Format Tanggal: Jumat, 24 April 2026
    hari_list = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    bulan_list = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", 
                  "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    
    nama_hari = hari_list[now.weekday()]
    nama_bulan = bulan_list[now.month - 1]
    tanggal_lengkap = f"{nama_hari}, {now.day} {nama_bulan} {now.year}"
    
    # Logika Status Pasar Saham (BEI: Senin-Jumat, 09:00 - 16:00 WIB)
    is_weekday = now.weekday() < 5
    is_market_hours = 9 <= now.hour < 16
    
    if is_weekday and is_market_hours:
        status_pasar = "🟢 MARKET OPEN (BEI)"
        jam_operasional = "Tutup pukul 16:00 WIB"
    else:
        status_pasar = "🔴 MARKET CLOSED"
        jam_operasional = "Buka kembali Senin pukul 09:00 WIB" if now.weekday() >= 4 else "Buka pukul 09:00 WIB"

    # --- TAMPILAN HEADER ---
    st.markdown(f"""
        <div style="background: #1e293b; padding: 20px; border-radius: 15px; border-left: 5px solid #fbbf24; margin-bottom: 25px;">
            <h1 style="color: #fbbf24; margin: 0;">VIP TERMINAL</h1>
            <p style="color: #94a3b8; margin: 0; font-size: 1.1rem;">{tanggal_lengkap}</p>
        </div>
    """, unsafe_allow_html=True)

    # --- TOMBOL NAVIGASI CEPAT (ANALISIS & HPP) ---
    st.write("### 🚀 Quick Actions")
    c_btn1, c_btn2 = st.columns(2)
    with c_btn1:
        if st.button("📊 ANALISIS SAHAM", use_container_width=True):
            st.session_state.page = "investasi"
            st.rerun()
    with c_btn2:
        if st.button("🧮 KALKULATOR HPP", use_container_width=True):
            st.session_state.page = "hpp"
            st.rerun()

    st.markdown("---")

    # --- WIDGET JAM & STATUS PASAR (SIDEBAR) ---
    with st.sidebar:
        st.markdown("### 🕒 System Clock")
        placeholder_jam = st.empty()
        st.markdown(f"**Status:** {status_pasar}")
        st.caption(f"Ket: {jam_operasional}")
        st.markdown("---")

    # --- DATA MARKET (DENGAN FITUR SEMBUNYIKAN) ---
    with st.expander("📊 MARKET INTELLIGENCE", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("IHSG (IDX)", "7,240.12", "+0.42%")
            st.caption("Indeks Saham Indonesia")
        with col2:
            st.metric("GOLD (XAU/USD)", "$2,341.50", "-0.12%")
            st.caption("Harga Emas Dunia")
        with col3:
            st.metric("USD / IDR", "16,125.00", "0.00")
            st.caption("Kurs Rupiah")

    # --- LOOP UPDATE JAM ---
    jam_sekarang = now.strftime("%H:%M:%S")
    placeholder_jam.markdown(f"""
        <div style="background: #0f172a; padding: 15px; border-radius: 10px; border: 1px solid #fbbf24; text-align: center;">
            <h2 style="color: white; margin: 0; font-family: 'Courier New', monospace;">{jam_sekarang}</h2>
            <p style="color: #fbbf24; margin: 0; font-size: 0.8rem;">WIB - JAKARTA</p>
        </div>
    """, unsafe_allow_html=True)

    time.sleep(1)
    st.rerun()
    
