import streamlit as st
import yfinance as yf
import requests
from datetime import datetime

def get_stock_suggestions(query, market_type):
    if not query: return []
    try:
        # Menambahkan filter lokasi agar saham luar tidak campur ke saham Indo
        suffix = ".JK" if market_type == "Indo" else ""
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers).json()
        
        suggestions = []
        for res in response.get('quotes', []):
            symbol = res.get('symbol')
            # Filter: Jika cari Indo, harus ada .JK. Jika Luar, tidak boleh ada .JK
            if market_type == "Indo" and not symbol.endswith(".JK"): continue
            if market_type == "Luar" and symbol.endswith(".JK"): continue
            
            name = res.get('longname', res.get('shortname', symbol))
            suggestions.append(f"{symbol} | {name}")
        return suggestions
    except: return []

def format_indo_date(timestamp):
    # Memperbaiki keterangan update yang sebelumnya cuma angka
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%d %B %Y | %H:%M WIB")
    except: return "Data Real-time"

def tampilkan_detail_rinci(ticker):
    data = yf.Ticker(ticker)
    info = data.info
    
    # 1. KONVERSI MATA UANG & EMAS
    price = info.get('currentPrice', info.get('regularMarketPrice', 0))
    currency = info.get('currency', 'USD')
    
    # Jika Emas (GC=F), kita konversi ke estimasi Rupiah per Gram
    if ticker == "GC=F":
        # Estimasi: Harga global per troy ounce ke Rupiah per gram
        # (Price / 31.1035) * Kurs (Asumsi 16.000)
        price_idr_gram = (price / 31.1035) * 16000 
        display_price = f"Rp {price_idr_gram:,.0f} / Gram"
        info_label = "Estimasi Harga Logam Mulia"
    else:
        display_price = f"{currency} {price:,.2f}"
        info_label = ticker

    st.markdown(f"""
        <div style="background:#1e293b; padding:20px; border-radius:15px; border-left: 5px solid #fbbf24;">
            <p style="color:#94a3b8; margin:0;">{info_label}</p>
            <h2 style="margin:0; color:white;">{info.get('longName', ticker)}</h2>
            <h1 style="color:#fbbf24; margin:0;">{display_price}</h1>
        </div>
    """, unsafe_allow_html=True)

    # 2. ANALISIS RISIKO & PREDIKSI (Persentase)
    st.write("---")
    col1, col2 = st.columns(2)
    
    with col1:
        beta = info.get('beta', 1)
        # Menghitung persentase risiko berdasarkan volatilitas (Beta)
        risk_pct = min(beta * 50, 100) # Simulasi perhitungan risiko
        st.subheader("⚠️ Analisis Risiko")
        st.progress(risk_pct/100)
        st.write(f"**Tingkat Risiko:** {risk_pct:.1f}%")
        st.caption("Semakin tinggi persentase, harga semakin mudah naik-turun tajam.")

    with col2:
        # Prediksi sederhana berdasarkan Moving Average 50 hari
        ma50 = info.get('fiftyDayAverage', 0)
        trend = "📈 BULLISH (Naik)" if price > ma50 else "📉 BEARISH (Turun)"
        st.subheader("🔮 Prediksi Kedepan")
        st.write(f"**Tren Saat Ini:** {trend}")
        st.write(f"**Target Analis:** {currency} {info.get('targetMeanPrice', 'N/A')}")

    # 3. KETERANGAN UPDATE (Tanggal & Jam yang Jelas)
    update_time = info.get('regularMarketTime')
    st.markdown(f"📅 **Update Terakhir:** {format_indo_date(update_time)}")

    # 4. KETERANGAN RINCI (SDM Friendly)
    with st.expander("📖 Penjelasan Lengkap (Klik untuk Ilmu)"):
        st.markdown(f"""
        ### Mengenal Perusahaan
        {info.get('longBusinessSummary', 'Data tidak tersedia')}
        
        ### Proyeksi Masa Depan
        Berdasarkan data internal, perusahaan ini memiliki pertumbuhan pendapatan sebesar **{info.get('revenueGrowth', 0)*100:.1f}%**. 
        Jika tren ini bertahan, kemungkinan nilai investasi Anda akan bertumbuh stabil.
        """)
        
