import streamlit as st
import yfinance as yf
import requests
from datetime import datetime

# Kamus Bahasa (Terjemahan)
TRANSLATIONS = {
    "Indonesia": {
        "search_label": "Cari Instrumen (Ketik Nama/Kode):",
        "risk_title": "⚠️ Analisis Risiko",
        "trend_title": "🔮 Prediksi Tren",
        "update_label": "📅 Update Terakhir:",
        "desc_title": "📖 Penjelasan Lengkap",
        "step_title": "🚀 Langkah Investasi",
        "buy_guide": "Beli di harga rendah, simpan jangka panjang."
    },
    "English": {
        "search_label": "Search Instrument (Type Name/Code):",
        "risk_title": "⚠️ Risk Analysis",
        "trend_title": "🔮 Trend Prediction",
        "update_label": "📅 Last Update:",
        "desc_title": "📖 Full Description",
        "step_title": "🚀 Investment Steps",
        "buy_guide": "Buy low, hold for the long term."
    }
}

def get_stock_suggestions(query, market_type):
    if not query or len(query) < 2: return []
    try:
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers).json()
        suggestions = []
        for res in response.get('quotes', []):
            symbol = res.get('symbol')
            # Filter Wilayah berdasarkan Setting
            if market_type == "Indo" and not symbol.endswith(".JK"): continue
            if market_type == "Luar" and symbol.endswith(".JK"): continue
            
            name = res.get('longname', res.get('shortname', symbol))
            suggestions.append(f"{symbol} | {name}")
        return suggestions
    except: return []

def render_saham_selector(market_type):
    lang = st.session_state.get('setting_lang', 'Indonesia')
    t = TRANSLATIONS[lang]

    # Fitur Autocomplete Nyata menggunakan Selectbox Searchable
    st.markdown(f"**{t['search_label']}**")
    
    # Input pencarian sementara
    search_query = st.text_input("Ketik di sini...", key=f"q_{market_type}", placeholder="Contoh: City, Telkom, Apple")
    
    if len(search_query) >= 2:
        suggestions = get_stock_suggestions(search_query, market_type)
        if suggestions:
            selected = st.selectbox("Hasil ditemukan (Pilih satu):", suggestions, key=f"sel_{market_type}")
            if selected:
                ticker = selected.split(" | ")[0]
                tampilkan_detail_rinci(ticker)
        else:
            st.warning("Data tidak ditemukan.")

def tampilkan_detail_rinci(ticker):
    lang = st.session_state.get('setting_lang', 'Indonesia')
    t = TRANSLATIONS[lang]
    pref_curr = st.session_state.get('setting_currency', 'IDR')
    
    data = yf.Ticker(ticker)
    info = data.info
    raw_price = info.get('currentPrice', info.get('regularMarketPrice', 0))
    stock_currency = info.get('currency', 'USD')
    
    # Konversi Kurs Otomatis (Fix rate 16,300)
    final_price = raw_price
    symbol_display = "Rp" if pref_curr == "IDR" else "$"
    
    if pref_curr == "IDR" and stock_currency == "USD":
        final_price = raw_price * 16300
    elif pref_curr == "USD" and stock_currency == "IDR":
        final_price = raw_price / 16300

    # Layout UI
    st.markdown(f"""
        <div style="background:#1e293b; padding:25px; border-radius:15px; border-left: 8px solid #fbbf24; margin-top:20px;">
            <h2 style="margin:0; color:white;">{info.get('longName', ticker)}</h2>
            <h1 style="color:#fbbf24; margin:0;">{symbol_display} {final_price:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # Analisis Risiko Rinci
    beta = info.get('beta', 1)
    risk_score = min(max(beta * 50, 10), 100) # Kalkulasi risiko %
    
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(t['risk_title'])
        st.progress(risk_score/100)
        st.write(f"Tingkat Risiko: **{risk_score:.1f}%**")
        st.caption("Analisis berdasarkan volatilitas pasar 5 tahun terakhir.")

    with col2:
        st.subheader(t['trend_title'])
        ma50 = info.get('fiftyDayAverage', 0)
        trend = "Bullish (Naik)" if raw_price > ma50 else "Bearish (Turun)"
        st.write(f"Status Tren: **{trend}**")

    # Update Waktu
    up_time = info.get('regularMarketTime')
    if up_time:
        dt = datetime.fromtimestamp(up_time)
        st.markdown(f"*{t['update_label']} {dt.strftime('%d %B %Y | %H:%M WIB')}*")
        
