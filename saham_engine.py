import streamlit as st
import yfinance as yf
import requests

def get_stock_suggestions(query):
    """Mencari saran simbol saham secara otomatis dari Yahoo Finance API"""
    if not query:
        return []
    try:
        # Mencari ticker berdasarkan nama atau huruf yang diketik
        url = f"https://query1.finance.yahoo.com/v1/finance/search?q={query}"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        data = response.json()
        
        # Ambil hasil pencarian (Ticker + Nama Perusahaan)
        suggestions = []
        for res in data.get('quotes', []):
            symbol = res.get('symbol')
            shortname = res.get('shortname', '')
            longname = res.get('longname', '')
            name = longname if longname else shortname
            suggestions.append(f"{symbol} | {name}")
        return suggestions
    except:
        return []

def render_saham_selector(market_type):
    st.markdown("### 🔍 Cari Instrumen")
    
    # Input teks untuk pencarian (Autocomplete)
    query = st.text_input("Ketik Nama Perusahaan atau Kode Saham (Contoh: City, Telkom, Apple)", key=f"input_{market_type}")
    
    if query:
        suggestions = get_stock_suggestions(query)
        if suggestions:
            # Tampilkan pilihan yang ditemukan
            selected = st.selectbox("Hasil pencarian ditemukan:", ["-- Pilih Perusahaan --"] + suggestions, key=f"select_{market_type}")
            
            if selected != "-- Pilih Perusahaan --":
                ticker = selected.split(" | ")[0]
                tampilkan_detail_rinci(ticker)
        else:
            st.warning("Tidak ditemukan perusahaan dengan nama tersebut.")

def tampilkan_detail_rinci(ticker):
    data = yf.Ticker(ticker)
    info = data.info
    
    # 1. Header Visual yang Memanjakan Mata
    price = info.get('currentPrice', info.get('regularMarketPrice', 0))
    currency = info.get('currency', 'IDR')
    
    st.markdown(f"""
        <div style="background:#1e293b; padding:25px; border-radius:15px; border-top: 5px solid #fbbf24; margin-top:20px;">
            <p style="margin:0; color:#94a3b8; font-size:14px;">{ticker}</p>
            <h2 style="margin:0; color:white;">{info.get('longName', ticker)}</h2>
            <h1 style="color:#fbbf24; margin:0;">{currency} {price:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)

    # 2. Detail Data & Edukasi (SDM Friendly - Klik untuk baca)
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.expander("📊 Data Fundamental & Harga"):
            st.write(f"**Harga per Lembar:** {currency} {price:,.2f}")
            if "IDR" in currency or ".JK" in ticker:
                st.write(f"**Harga per Lot (100 lbr):** Rp {price*100:,.0f}")
            st.write(f"**Dividen per Tahun:** {info.get('dividendRate', 0)} ({info.get('dividendYield', 0)*100:.2f}%)")
            st.write(f"**Sektor:** {info.get('sector', 'N/A')}")

    with col2:
        with st.expander("⚖️ Analisis Risiko & Internal"):
            beta = info.get('beta', 1)
            risk = "Rendah (Aman)" if beta < 0.8 else "Tinggi (Agresif)" if beta > 1.2 else "Menengah"
            st.warning(f"**Tingkat Risiko:** {risk} (Beta: {beta})")
            st.write(f"**Karyawan:** {info.get('fullTimeEmployees', 'N/A')}")

    # 3. Keterangan Panjang yang Disembunyikan
    with st.expander("📖 Pengertian & Langkah Investasi di Sini (Baca Selengkapnya)"):
        st.markdown(f"""
        **Tentang Perusahaan:** {info.get('longBusinessSummary', 'Deskripsi tidak tersedia.')}

        **Apa yang Anda dapatkan?**
        1. **Keuntungan Kenaikan Harga:** Jika harga naik dari saat Anda beli.
        2. **Passive Income:** Jatah bagi hasil laba (Dividen) jika perusahaan untung.

        **Langkah Investasi:**
        1. Buka akun sekuritas resmi.
        2. Masukkan dana sesuai harga 1 Lot saham ini.
        3. Klik beli dan simpan untuk jangka panjang (minimal 1 tahun).
        """)

    # 4. Info Update Harian Otomatis
    st.caption(f"📅 Update Terakhir: {info.get('regularMarketTime', 'Real-time')}")
  
