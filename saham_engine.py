import streamlit as st
import yfinance as yf
import requests
from datetime import datetime

def get_stock_suggestions(query, market_type):
    if not query: return []
    try:
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers).json()
        
        suggestions = []
        for res in response.get('quotes', []):
            symbol = res.get('symbol')
            # Filter pasar
            if market_type == "Indo" and not symbol.endswith(".JK"): continue
            if market_type == "Luar" and symbol.endswith(".JK"): continue
            
            name = res.get('longname', res.get('shortname', symbol))
            suggestions.append(f"{symbol} | {name}")
        return suggestions
    except: return []

def render_saham_selector(market_type):
    st.markdown("### 🔍 Cari Instrumen")
    query = st.text_input("Ketik Nama Perusahaan...", key=f"input_{market_type}")
    
    if query:
        suggestions = get_stock_suggestions(query, market_type)
        if suggestions:
            selected = st.selectbox("Hasil ditemukan:", ["-- Pilih --"] + suggestions, key=f"sel_{market_type}")
            if selected != "-- Pilih --":
                ticker = selected.split(" | ")[0]
                tampilkan_detail_rinci(ticker)
        else:
            st.warning("Data tidak ditemukan.")

def tampilkan_detail_rinci(ticker):
    data = yf.Ticker(ticker)
    info = data.info
    
    # Ambil Setting Global
    pref_currency = st.session_state.get('setting_currency', 'IDR')
    kurs_usd_to_idr = 16200 # Simulasi kurs fix, bisa ambil API kurs jika mau
    
    # Logika Konversi Harga
    raw_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
    stock_currency = info.get('currency', 'USD')
    
    final_price = raw_price
    if pref_currency == "IDR" and stock_currency == "USD":
        final_price = raw_price * kurs_usd_to_idr
        symbol_price = "Rp"
    elif pref_currency == "USD" and stock_currency == "IDR":
        final_price = raw_price / kurs_usd_to_idr
        symbol_price = "$"
    else:
        symbol_price = "Rp" if pref_currency == "IDR" else "$"

    # Header Tampilan
    st.markdown(f"""
        <div style="background:#1e293b; padding:20px; border-radius:15px; border-top: 5px solid #fbbf24; margin-top:20px;">
            <p style="margin:0; color:#94a3b8;">{ticker}</p>
            <h2 style="margin:0; color:white;">{info.get('longName', ticker)}</h2>
            <h1 style="color:#fbbf24; margin:0;">{symbol_price} {final_price:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Edukasi Risiko & Analisis Kedepan
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        beta = info.get('beta', 1)
        risk_pct = min(beta * 50, 100)
        st.subheader("⚠️ Analisis Risiko")
        st.progress(risk_pct/100)
        st.write(f"Persentase Risiko: **{risk_pct:.1f}%**")
    
    with c2:
        ma50 = info.get('fiftyDayAverage', 0)
        trend = "Naik (Bullish)" if raw_price > ma50 else "Turun (Bearish)"
        st.subheader("🔮 Prediksi Tren")
        st.write(f"Status: **{trend}**")

    # Waktu Indonesia
    up_time = info.get('regularMarketTime')
    if up_time:
        dt = datetime.fromtimestamp(up_time)
        st.caption(f"📅 Update: {dt.strftime('%d %B %Y | %H:%M WIB')}")
        
