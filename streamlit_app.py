import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta

# ==========================================
# 1. KONFIGURASI TEMA "DARK GOLD PREMIUM"
# ==========================================
st.set_page_config(page_title="BizInvest Pro v9.0", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #0b0f19; color: #ffffff; }
    
    .stButton>button {
        width: 100%; border-radius: 8px;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        color: #fbbf24; font-weight: bold; border: 1px solid #d97706;
        padding: 0.7rem; transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%); color: white;
    }
    
    div[data-testid="metric-container"] {
        background: #171f2d; border-radius: 10px; padding: 15px;
        border-left: 4px solid #fbbf24; border-top: 1px solid #374151;
    }
    .info-box {
        background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981;
        border-radius: 8px; padding: 15px; margin-bottom: 15px;
    }
    .ai-report {
        background: rgba(217, 119, 6, 0.1); border: 1px solid #fbbf24;
        border-radius: 10px; padding: 20px; font-size: 16px; line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE SAHAM RAKSASA (AUTOCOMPLETE)
# ==========================================
DB_LOKAL = [
    # Perbankan & Keuangan
    "BBCA.JK - PT Bank Central Asia Tbk", "BBRI.JK - PT Bank Rakyat Indonesia Tbk", "BMRI.JK - PT Bank Mandiri Tbk", "BBNI.JK - PT Bank Negara Indonesia Tbk", "BRIS.JK - PT Bank Syariah Indonesia Tbk", "ARTO.JK - PT Bank Jago Tbk", "BBTN.JK - PT Bank Tabungan Negara Tbk", "BDMN.JK - PT Bank Danamon Tbk", "BNGA.JK - PT Bank CIMB Niaga Tbk",
    # Konsumer & Retail
    "ICBP.JK - PT Indofood CBP Sukses Makmur Tbk", "INDF.JK - PT Indofood Sukses Makmur Tbk", "UNVR.JK - PT Unilever Indonesia Tbk", "MYOR.JK - PT Mayora Indah Tbk", "CPIN.JK - PT Charoen Pokphand Indonesia Tbk", "JPFA.JK - PT Japfa Comfeed Tbk", "AMRT.JK - PT Sumber Alfaria Trijaya Tbk (Alfamart)", "MIDI.JK - PT Midi Utama Indonesia Tbk (Alfamidi)", "MAPI.JK - PT Mitra Adiperkasa Tbk", "LPPF.JK - PT Matahari Department Store Tbk", "KLBF.JK - PT Kalbe Farma Tbk", "SIDO.JK - PT Industri Jamu dan Farmasi Sido Muncul Tbk",
    # Energi, Tambang, & Komoditas
    "ADRO.JK - PT Adaro Energy Indonesia Tbk", "PTBA.JK - PT Bukit Asam Tbk", "ITMG.JK - PT Indo Tambangraya Megah Tbk", "HRUM.JK - PT Harum Energy Tbk", "BUMI.JK - PT Bumi Resources Tbk", "ANTM.JK - PT Aneka Tambang Tbk", "INCO.JK - PT Vale Indonesia Tbk", "MDKA.JK - PT Merdeka Copper Gold Tbk", "AMMN.JK - PT Amman Mineral Internasional Tbk", "PGAS.JK - PT Perusahaan Gas Negara Tbk", "MEDC.JK - PT Medco Energi Internasional Tbk", "AKRA.JK - PT AKR Corporindo Tbk",
    # Infrastruktur, Industri & Teknologi
    "TLKM.JK - PT Telkom Indonesia Tbk", "GOTO.JK - PT GoTo Gojek Tokopedia Tbk", "BUKA.JK - PT Bukalapak.com Tbk", "MTEL.JK - PT Dayamitra Telekomunikasi Tbk", "ASII.JK - PT Astra International Tbk", "UNTR.JK - PT United Tractors Tbk", "BRPT.JK - PT Barito Pacific Tbk", "TPIA.JK - PT Chandra Asri Petrochemical Tbk", "BREN.JK - PT Barito Renewables Energy Tbk", "CUAN.JK - PT Petrindo Jaya Kreasi Tbk", "JSMR.JK - PT Jasa Marga Tbk",
    # Properti & Konstruksi
    "BSDE.JK - PT Bumi Serpong Damai Tbk", "CTRA.JK - PT Ciputra Development Tbk", "PWON.JK - PT Pakuwon Jati Tbk", "SMRA.JK - PT Summarecon Agung Tbk", "LPKR.JK - PT Lippo Karawaci Tbk", "PTPP.JK - PT PP (Persero) Tbk", "WIKA.JK - PT Wijaya Karya Tbk", "ADHI.JK - PT Adhi Karya Tbk"
]

DB_GLOBAL = [
    # Top Tech (Magnificent Seven & Lainnya)
    "AAPL - Apple Inc.", "MSFT - Microsoft Corp.", "NVDA - NVIDIA Corp.", "TSLA - Tesla Inc.", "GOOGL - Alphabet Inc. (Google)", "AMZN - Amazon.com Inc.", "META - Meta Platforms Inc. (Facebook/IG)", "NFLX - Netflix Inc.", "ADBE - Adobe Inc.", "CRM - Salesforce Inc.", "AMD - Advanced Micro Devices", "INTC - Intel Corp.", "CSCO - Cisco Systems", "ORCL - Oracle Corp.",
    # Finansial & Pembayaran
    "V - Visa Inc.", "MA - Mastercard Inc.", "PYPL - PayPal Holdings", "JPM - JPMorgan Chase", "BAC - Bank of America", "WFC - Wells Fargo", "BRK-B - Berkshire Hathaway (Warren Buffett)",
    # Konsumsi & Retail AS
    "WMT - Walmart Inc.", "TGT - Target Corp.", "COST - Costco Wholesale", "KO - The Coca-Cola Co.", "PEP - PepsiCo Inc.", "MCD - McDonald's Corp.", "SBUX - Starbucks Corp.", "NKE - NIKE Inc.", "PG - Procter & Gamble", "JNJ - Johnson & Johnson",
    # Otomotif, Hiburan & Lainnya
    "F - Ford Motor Co.", "GM - General Motors", "DIS - The Walt Disney Co.", "BA - Boeing Co.", "XOM - Exxon Mobil", "CVX - Chevron Corp."
]

DB_KRIPTO = [
    "BTC-USD - Bitcoin", "ETH-USD - Ethereum", "USDT-USD - Tether", "BNB-USD - Binance Coin", "SOL-USD - Solana", "XRP-USD - Ripple", "USDC-USD - USD Coin", "ADA-USD - Cardano", "AVAX-USD - Avalanche", "DOGE-USD - Dogecoin", "DOT-USD - Polkadot", "LINK-USD - Chainlink", "TRX-USD - TRON", "MATIC-USD - Polygon", "SHIB-USD - Shiba Inu", "LTC-USD - Litecoin", "BCH-USD - Bitcoin Cash", "UNI-USD - Uniswap", "ATOM-USD - Cosmos"
]

# ==========================================
# 3. STATE NAVIGASI & LOGIN
# ==========================================
if 'page' not in st.session_state: st.session_state['page'] = 'home'
def navigate(page_name): st.session_state['page'] = page_name

def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("<h2 style='text-align: center; color: #fbbf24; margin-top: 10vh;'>👑 Akses VIP BizInvest Pro</h2>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input("Masukkan Lisensi / Password:", type="password", key="pwd_input")
            if st.button("Masuk"):
                if st.session_state.pwd_input == "AksesPremium123":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else: st.error("❌ Lisensi tidak valid.")
        return False
    return st.session_state["password_correct"]

# ==========================================
# 4. KECERDASAN BUATAN (AI ADVISOR)
# ==========================================
def generate_ai_insight(info, rsi, nama_aset):
    pe_ratio = info.get('trailingPE', 0)
    pbv_ratio = info.get('priceToBook', 0)
    profit_margin = info.get('profitMargins', 0) * 100
    div_yield = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
    
    insight = f"Berdasarkan analisis kecerdasan buatan kami terhadap **{nama_aset}**, berikut adalah laporan lengkapnya:\n\n"
    
    # Analisis Valuasi (Mahal/Murah)
    insight += "🎯 **Apakah Harga Saham Ini Sedang Murah atau Mahal?**\n"
    if pe_ratio > 0:
        if pe_ratio < 15 and pbv_ratio < 1.5:
            insight += f"Aset ini sedang **SANGAT MURAH (Undervalued)**. Harga pasar saat ini lebih rendah dari nilai asli perusahaannya. Ibaratnya, Anda membeli barang bermerek dengan harga diskon cuci gudang.\n\n"
        elif pe_ratio > 30 or pbv_ratio > 4:
            insight += f"Hati-hati, aset ini dinilai **KEMAHALAN (Overvalued)**. Investor berani membayar sangat tinggi karena harapan masa depan, tapi risikonya sangat besar jika kinerja perusahaan tiba-tiba menurun.\n\n"
        else:
            insight += f"Harga saham ini **WAJAR (Fair Value)**. Harganya sepadan dengan keuntungan yang dihasilkan perusahaan saat ini.\n\n"
    else:
        insight += "Aset ini bergerak sangat liar dan sulit dinilai menggunakan rumus tradisional (kemungkinan ini adalah Kripto atau perusahaan teknologi yang sedang membakar uang).\n\n"

    # Analisis Momentum (Teknikal)
    insight += "📊 **Bagaimana Momentum Jual-Belinya Saat Ini?**\n"
    if rsi < 35:
        insight += "Saat ini banyak orang yang sedang panik menjual. Namun kabar baiknya, harga sudah **Sangat Jatuh (Jenuh Jual)**. Ini sering menjadi titik pantul naik, membuatnya sangat menarik untuk mulai dicicil beli.\n\n"
    elif rsi > 65:
        insight += "Aset ini sedang *Viral* (banyak yang berebut beli). Harga sudah **Berada di Pucuk (Jenuh Beli)**. Sangat tidak disarankan membeli sekarang, lebih baik tunggu harga turun (diskon) terlebih dahulu.\n\n"
    else:
        insight += "Pergerakan harga sedang stabil dan normal. Tidak ada kepanikan atau euforia berlebihan dari para trader.\n\n"
        
    # Analisis Kinerja Bisnis
    insight += "🏢 **Bagaimana Kesehatan Bisnisnya?**\n"
    if profit_margin > 15:
        insight += f"Bisnis ini **SANGAT MENGUNTUNGKAN**. Mereka berhasil menyimpan {profit_margin:.1f}% dari pemasukannya sebagai laba bersih murni. Perusahaan yang sangat sehat secara finansial! "
    elif profit_margin < 0:
        insight += "Waspada! Perusahaan ini sedang **MERUGI/BAKAR UANG**. Mereka lebih banyak mengeluarkan biaya operasional daripada pemasukan yang didapat. "
        
    if div_yield > 3:
        insight += f"Kabar luar biasa lainnya: Perusahaan ini sangat dermawan. Mereka membagikan dividen (bonus uang tunai) rutin sekitar **{div_yield:.1f}%** per tahun langsung ke rekening Anda hanya dengan menyimpan sahamnya tanpa perlu Anda apa-apakan."
        
    return insight

# ==========================================
# 5. MODUL AI TRADING UTAMA
# ==========================================
def menu_trading():
    col_bck, col_title = st.columns([1, 5])
    with col_bck: st.button("⬅️ KEMBALI MENU", on_click=navigate, args=('home',))
    with col_title: st.markdown("<h3 style='color: #fbbf24; margin-top:-5px;'>📊 Terminal Analisis Real-Time & AI</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    jenis_pasar = st.radio("🌍 Pilih Kategori Pasar:", ["🇮🇩 Saham Lokal (BEI)", "🇺🇸 Saham Global (US)", "🪙 Kripto"], horizontal=True)
    
    if "Lokal" in jenis_pasar:
        options_list = DB_LOKAL
        mata_uang = "Rp"
    elif "Global" in jenis_pasar:
        options_list = DB_GLOBAL
        mata_uang = "$"
    else:
        options_list = DB_KRIPTO
        mata_uang = "$"

    st.markdown("<p style='color:gray; font-size:14px;'><i>Ketik huruf awal (misal: 'Bank' atau 'Telkom') agar AI memunculkan daftarnya otomatis. Jika nama perusahaan tidak ada di daftar ini, Anda tetap bisa mengeceknya dengan memilih opsi 'Input Manual Ticker' paling bawah.</i></p>", unsafe_allow_html=True)
    
    pilihan_saham = st.selectbox("🔍 Cari Nama Perusahaan / Aset:", options=["➕ Pilih / Ketik di sini..."] + options_list + ["✍️ Input Manual Ticker Global (Untuk saham yang tidak ada di daftar)..."])
    
    if pilihan_saham == "✍️ Input Manual Ticker Global (Untuk saham yang tidak ada di daftar)...":
        ticker_symbol = st.text_input("Ketik Kode Resmi Global (Contoh: BRPT.JK, TSLA, BTC-USD)", "").upper()
    elif pilihan_saham != "➕ Pilih / Ketik di sini...":
        ticker_symbol = pilihan_saham.split(" - ")[0]
    else: ticker_symbol = None

    if st.button("🚀 Pindai dengan AI & Analisis Mendalam") and ticker_symbol:
        with st.spinner(f"AI sedang menarik data rahasia pasar dari server global untuk {ticker_symbol}..."):
            try:
                data_raw = yf.Ticker(ticker_symbol)
                df = data_raw.history(period="1y")
                info = data_raw.info
                
                if df.empty:
                    st.error("Data tidak ditemukan. Pastikan bursa sedang tidak libur panjang atau kode yang Anda ketik benar.")
                    return
                
                df.ta.macd(append=True)
                df.ta.rsi(length=14, append=True)
                df.ta.ema(length=20, append=True)

                tab1, tab2, tab3, tab4 = st.tabs(["🤖 Laporan AI Khusus Awam", "📋 Ringkasan & Harga Beli", "🏢 Fundamental (Kesehatan Bisnis)", "📈 Grafik Profesional"])
                
                with tab1:
                    st.markdown(f"### 🤖 Laporan Bahasa Manusia oleh AI")
                    rsi = df['RSI_14'].iloc[-1]
                    nama_perusahaan = info.get('longName', ticker_symbol)
                    
                    st.markdown("<div class='ai-report'>", unsafe_allow_html=True)
                    st.write(generate_ai_insight(info, rsi, nama_perusahaan))
                    st.markdown("</div>", unsafe_allow_html=True)

                with tab2:
                    last_price = df['Close'].iloc[-1]
                    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                    st.markdown("#### 💰 Keputusan Harga Pembelian Terkini")
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        if mata_uang == "Rp": st.metric("Harga 1 Lembar Saat Ini", f"Rp {last_price:,.0f}")
                        else: st.metric("Harga 1 Unit Saat Ini", f"$ {last_price:,.2f}")
                    with col_p2:
                        if "Lokal" in jenis_pasar:
                            st.metric("Dana Disiapkan untuk 1 LOT (Wajib Minimal Beli)", f"Rp {last_price * 100:,.0f}")
                        else:
                            st.metric("Sistem Pembelian Aset", "Bisa Pecahan (Fraksional)")
                    st.markdown("</div>", unsafe_allow_html=True)

                    skor_beli = 100 - rsi
                    col_gauge1, col_gauge2 = st.columns(2)
                    with col_gauge1:
                        fig_g1 = go.Figure(go.Indicator(mode = "gauge+number", value = skor_beli, title = {'text': "Seberapa Bagus Waktu Belinya?", 'font': {'color': 'white', 'size':16}}, gauge = {'axis': {'range': [0, 100]}, 'steps': [{'range': [0, 30], 'color': "#ef4444"}, {'range': [30, 70], 'color': "#f59e0b"}, {'range': [70, 100], 'color': "#10b981"}]}))
                        fig_g1.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig_g1, use_container_width=True)
                    with col_gauge2:
                        beta = info.get('beta', 1.0)
                        fig_g2 = go.Figure(go.Indicator(mode = "gauge+number", value = min(abs(beta) * 50, 100) if beta else 50, title = {'text': "Tingkat Goncangan Harga (Risiko)", 'font': {'color': 'white', 'size':16}}, gauge = {'axis': {'range': [0, 100]}, 'steps': [{'range': [0, 40], 'color': "#10b981"}, {'range': [40, 70], 'color': "#f59e0b"}, {'range': [70, 100], 'color': "#ef4444"}]}))
                        fig_g2.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig_g2, use_container_width=True)

                with tab3:
                    st.markdown("### 🏢 Fundamental Perusahaan (Rapor Bisnis)")
                    st.write("*Jangan bingung dengan istilah dewa saham. AI kami sudah memberikan terjemahannya di setiap baris!*")
                    st.markdown("---")
                    
                    c_fun1, c_fun2 = st.columns(2)
                    with c_fun1:
                        mc = info.get('marketCap', 0)
                        st.write(f"**1. Kapitalisasi Pasar:** {mata_uang} {mc:,.0f}")
                        st.caption("*(Total harga jika Anda menjadi sultan dan ingin membeli seluruh perusahaan ini beserta seluruh gedungnya. Semakin besar angkanya, semakin perusahaan ini kebal terhadap kebangkrutan).*")
                        
                        pe = info.get('trailingPE', 0)
                        st.write(f"**2. Valuasi PER (Price to Earnings):** {pe:.2f}x")
                        st.caption("*(Mengukur kemahalan saham. Artinya butuh waktu {pe:.0f} tahun agar modal investasi Anda balik 100% dari keuntungan perusahaan).*")
                        
                        pbv = info.get('priceToBook', 0)
                        st.write(f"**3. Valuasi PBV (Price to Book):** {pbv:.2f}x")
                        st.caption("*(Perbandingan harga saham dengan harta fisik perusahaan. Jika angkanya 1, harganya wajar. Jika di bawah 1, harga sangat murah/diskon).*")
                        
                    with c_fun2:
                        pm = info.get('profitMargins', 0) * 100
                        st.write(f"**4. Margin Laba Bersih:** {pm:.2f}%")
                        st.caption("*(Keringat keuntungan. Dari setiap Rp 100 ribu barang yang mereka jual, mereka mengantongi untung bersih sebesar {pm:.1f} ribu).*")
                        
                        dy = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
                        st.write(f"**5. Bunga Dividen Tahunan:** {dy:.2f}% per tahun")
                        st.caption("*(Mirip bunga deposito. Ini adalah bonus uang tunai yang akan otomatis masuk ke rekening Anda setiap tahun).*")
                        
                        deb = info.get('debtToEquity', 0)
                        st.write(f"**6. Rasio Tumpukan Hutang:** {deb}%")
                        st.caption("*(Tingkat hutang dibandingkan modal sendiri. Jika di atas 100%, tandanya hutang mereka lebih besar dari modal mereka. Bahaya jika ekonomi krisis).*")

                with tab4:
                    st.markdown("### Terminal Grafik Teknikal")
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.8])
                    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Harga'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], line=dict(color='#fbbf24', width=1.5), name='Tren Menengah (EMA)'), row=1, col=1)
                    v_colors = ['#10b981' if df.iloc[i]['Close'] >= df.iloc[i]['Open'] else '#ef4444' for i in range(len(df))]
                    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=v_colors, name='Aktivitas Jual-Beli'), row=2, col=1)
                    fig.update_layout(template='plotly_dark', height=500, xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error("Server kami gagal menghubungi bursa global. Pastikan koneksi internet lancar atau kode saham yang Anda masukkan benar.")

# ==========================================
# 6. MODUL HPP
# ==========================================
def menu_hpp():
    col_bck, col_title = st.columns([1, 5])
    with col_bck: st.button("⬅️ KEMBALI MENU", on_click=navigate, args=('home',))
    with col_title: st.markdown("<h3 style='color: #fbbf24; margin-top:-5px;'>📦 AI Kalkulator Harga Jual (HPP)</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        bahan = st.number_input("Total Bahan Baku (Rp)", value=1500000)
        tenaga = st.number_input("Total Tenaga Kerja (Rp)", value=500000)
        lain = st.number_input("Biaya Lain (Listrik, dll) (Rp)", value=200000)
    with col_b:
        qty = st.number_input("Berapa Pcs Dihasilkan?", value=100)
        margin = st.slider("Target Keuntungan (%)", 5, 100, 35)
        
    if st.button("Hitung Otomatis"):
        total = bahan + tenaga + lain
        hpp = total / qty if qty > 0 else 0
        jual = hpp * (1 + margin/100)
        c1, c2, c3 = st.columns(3)
        c1.metric("Modal 1 Pcs (HPP)", f"Rp {hpp:,.0f}")
        c2.metric("Saran Harga Jual", f"Rp {jual:,.0f}")
        c3.metric("Laba Bersih per Pcs", f"Rp {jual-hpp:,.0f}")

# ==========================================
# 7. LANDING PAGE
# ==========================================
if check_password():
    if st.session_state['page'] == 'home':
        st.markdown("<div style='text-align: center; margin-top: 5vh;'><h1 style='color: #fbbf24; font-size: 3.5rem; margin-bottom: 0px;'>BIZINVEST PRO</h1><p style='color: #9ca3af; font-size: 1.2rem; margin-bottom: 50px;'>Sahabat Investasi Pintar & Kalkulator Bisnis UMKM</p></div>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("📈 Cek Saham & Panduan Investasi", on_click=navigate, args=('trading',))
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("📦 Kalkulator Modal & Harga Jual", on_click=navigate, args=('hpp',))
    elif st.session_state['page'] == 'trading': menu_trading()
    elif st.session_state['page'] == 'hpp': menu_hpp()
