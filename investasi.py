import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

def show_investasi():
    st.markdown("<h2 style='color: #fbbf24;'>📈 Terminal Analisis & Edukasi Pro</h2>", unsafe_allow_html=True)
    
    # Menu Navigasi Internal di dalam Modul Investasi
    sub_menu = st.tabs([
        "🔍 Analisis Saham", 
        "📚 Panduan Investasi", 
        "📖 Book Guide", 
        "📊 Info Investasi Menyeluruh"
    ])

    # ---------------------------------------------------------
    # TAB 1: ANALISIS SAHAM (Data Super Lengkap)
    # ---------------------------------------------------------
    with sub_menu[0]:
        ticker = st.text_input("Masukkan Kode Saham (Contoh: BBCA.JK atau AAPL)", "BBCA.JK")
        
        if ticker:
            data = yf.Ticker(ticker)
            info = data.info
            
            # Row 1: Ringkasan Harga & Dividen
            col1, col2, col3, col4 = st.columns(4)
            price = info.get('currentPrice', 0)
            col1.metric("Harga/Lembar", f"Rp {price:,.0f}" if ".JK" in ticker else f"${price}")
            col2.metric("Harga/Lot (100 lbr)", f"Rp {price*100:,.0f}" if ".JK" in ticker else "-")
            col3.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100:.2f}%")
            col4.metric("Risk Level (Beta)", info.get('beta', 'N/A'))

            st.write("---")
            
            # Row 2: Fundamental & Internal/Eksternal
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("📋 Profil & Internal")
                st.write(f"**Sektor:** {info.get('sector', 'N/A')}")
                st.write(f"**Industri:** {info.get('industry', 'N/A')}")
                st.write(f"**Cash Flow:** {info.get('operatingCashflow', 0):,.0f}")
                st.expander("Deskripsi Perusahaan").write(info.get('longBusinessSummary', 'Tidak ada data'))
            
            with c2:
                st.subheader("🌐 Kondisi Eksternal & Risiko")
                risk = "Tinggi" if info.get('beta', 1) > 1.2 else "Moderat" if info.get('beta', 1) > 0.8 else "Rendah"
                st.warning(f"**Tingkat Risiko:** {risk}")
                st.info(f"**Rekomendasi Analis:** {info.get('recommendationKey', 'N/A').upper()}")
            
            # Row 3: Teknikal (Chart)
            st.subheader("📉 Analisis Teknikal (Harga Historis)")
            hist = data.history(period="1y")
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            st.plotly_chart(fig, use_container_width=True)

    # ---------------------------------------------------------
    # TAB 2: PANDUAN INVESTASI (Langkah demi Langkah)
    # ---------------------------------------------------------
    with sub_menu[1]:
        st.subheader("🚀 Langkah-langkah Mulai Investasi")
        col_step1, col_step2 = st.columns(2)
        with col_step1:
            st.markdown("""
            1. **Tentukan Tujuan:** (Dana darurat, DP rumah, atau Pensiun?)
            2. **Siapkan Dana Dingin:** Jangan pakai uang dapur.
            3. **Pilih Sekuritas:** Buka akun di BRIGHTS atau aplikasi resmi lainnya.
            4. **Analisis Saham:** Gunakan fitur 'Analisis' di tab sebelah.
            """)
        with col_step2:
            st.markdown("""
            5. **Set Auto-Order:** Gunakan fitur Stop Loss untuk jaga risiko.
            6. **Diversifikasi:** Jangan taruh semua telur dalam satu keranjang.
            7. **Monitoring berkala:** Cek fundamental perusahaan tiap kuartal.
            """)

    # ---------------------------------------------------------
    # TAB 3: BOOK GUIDE (Materi Penting)
    # ---------------------------------------------------------
    with sub_menu[2]:
        st.subheader("📚 Book Guide: Intisari Pembelajaran")
        with st.expander("📖 Bab 1: Psikologi Trading"):
            st.write("Mengapa disiplin lebih penting daripada kecerdasan di pasar saham.")
        with st.expander("📖 Bab 2: Fundamental Mastery"):
            st.write("Cara membaca Laporan Keuangan (NERACA, LABA RUGI, ARUS KAS).")
        with st.expander("📖 Bab 3: Technical Analysis"):
            st.write("Memahami Support, Resistance, dan Trendline.")

    # ---------------------------------------------------------
    # TAB 4: INFO INVESTASI EMAS & LAINNYA
    # ---------------------------------------------------------
    with sub_menu[3]:
        st.subheader("🟡 Informasi Investasi Logam Mulia & Obligasi")
        gold_col1, gold_col2 = st.columns(2)
        with gold_col1:
            st.markdown("""
            **Investasi Emas:**
            - Cocok untuk jangka panjang (>5 tahun).
            - Sebagai lindung nilai (Hedge) terhadap inflasi.
            - Likuiditas tinggi (mudah dijual kembali).
            """)
        with gold_col2:
            st.markdown("""
            **Investasi Obligasi (SBN/ORI):**
            - Kupon tetap tiap bulan.
            - Dijamin negara 100%.
            - Resiko hampir nol.
            """)
            
