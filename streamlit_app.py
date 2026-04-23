import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta

# ==========================================
# 1. KONFIGURASI TEMA "DARK GOLD PREMIUM"
# ==========================================
st.set_page_config(page_title="BizInvest Pro v8.0", layout="wide", initial_sidebar_state="collapsed")

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
# 2. DATABASE SAHAM
# ==========================================
DB_LOKAL = [
    "BBCA.JK - PT Bank Central Asia Tbk", "BBRI.JK - PT Bank Rakyat Indonesia Tbk", 
    "BMRI.JK - PT Bank Mandiri Tbk", "BBNI.JK - PT Bank Negara Indonesia Tbk", 
    "TLKM.JK - PT Telkom Indonesia Tbk", "ASII.JK - PT Astra International Tbk", 
    "GOTO.JK - PT GoTo Gojek Tokopedia Tbk", "ADRO.JK - PT Adaro Energy Indonesia Tbk", 
    "PTBA.JK - PT Bukit Asam Tbk", "ANTM.JK - PT Aneka Tambang Tbk", 
    "ICBP.JK - PT Indofood CBP Sukses Makmur Tbk", "UNVR.JK - PT Unilever Indonesia Tbk",
    "AMMN.JK - PT Amman Mineral Internasional Tbk", "BUMI.JK - PT Bumi Resources Tbk"
]
DB_GLOBAL = ["AAPL - Apple Inc.", "MSFT - Microsoft", "TSLA - Tesla, Inc.", "NVDA - NVIDIA", "GOOGL - Alphabet (Google)"]
DB_KRIPTO = ["BTC-USD - Bitcoin", "ETH-USD - Ethereum", "SOL-USD - Solana", "DOGE-USD - Dogecoin"]

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
            st.text_input("Masukkan Lisensi:", type="password", key="pwd_input")
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
            insight += f"Aset ini sedang **SANGAT MURAH (Undervalued)**. Harga pasar saat ini lebih rendah dari nilai asli perusahaannya (PBV: {pbv_ratio:.2f}x). Ini adalah kesempatan langka seperti membeli barang bermerek dengan harga diskon.\n\n"
        elif pe_ratio > 30 or pbv_ratio > 4:
            insight += f"Hati-hati, aset ini dinilai **KEMAHALAN (Overvalued)**. Investor berani membayar sangat tinggi (PBV: {pbv_ratio:.2f}x) karena harapan masa depan, tapi risikonya sangat besar jika kinerja menurun.\n\n"
        else:
            insight += f"Harga saham ini **WAJAR (Fair Value)**. Harganya sepadan dengan keuntungan yang dihasilkan perusahaan saat ini.\n\n"
    else:
        insight += "Aset ini sulit dinilai secara tradisional (mungkin Kripto atau perusahaan yang sedang merugi).\n\n"

    # Analisis Momentum (Teknikal)
    insight += "📊 **Bagaimana Momentum Jual-Belinya Saat Ini?**\n"
    if rsi < 35:
        insight += "Saat ini banyak investor yang sedang panik menjual saham ini. Namun kabar baiknya, harga sudah **Sangat Jatuh (Jenuh Jual)**, membuatnya sangat menarik untuk dibeli karena potensi naiknya lebih besar daripada turunnya.\n\n"
    elif rsi > 65:
        insight += "Saham ini sedang *FOMO* (banyak yang berebut beli). Harga sudah **Berada di Pucuk (Jenuh Beli)**. Sangat tidak disarankan membeli sekarang, lebih baik tunggu harga turun (koreksi).\n\n"
    else:
        insight += "Pergerakan harga sedang stabil dan normal. Tidak ada kepanikan atau euforia berlebihan.\n\n"
        
    # Analisis Kinerja Bisnis
    insight += "🏢 **Bagaimana Kesehatan Bisnisnya?**\n"
    if profit_margin > 15:
        insight += f"Bisnis ini **SANGAT MENGUNTUNGKAN**. Mereka bisa menyimpan {profit_margin:.1f}% dari pemasukannya sebagai laba bersih. Perusahaan yang kaya raya! "
    elif profit_margin < 0:
        insight += "Perusahaan ini sedang **MERUGI/BAKAR UANG**. Mereka lebih banyak mengeluarkan biaya daripada pemasukan. Sangat berisiko! "
        
    if div_yield > 3:
        insight += f"Selain itu, perusahaan ini sangat dermawan. Mereka membagikan dividen (bonus tahunan) sebesar **{div_yield:.1f}%** per tahun langsung ke rekening Anda hanya dengan menyimpan sahamnya."
        
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

    pilihan_saham = st.selectbox("🔍 Cari Nama Perusahaan atau Kode:", options=["➕ Pilih/Ketik di sini..."] + options_list + ["✍️ Input Manual Ticker..."])
    
    if pilihan_saham == "✍️ Input Manual Ticker...":
        ticker_symbol = st.text_input("Ketik Kode Resmi", "").upper()
    elif pilihan_saham != "➕ Pilih/Ketik di sini...":
        ticker_symbol = pilihan_saham.split(" - ")[0]
    else: ticker_symbol = None

    if st.button("🚀 Analisis Mendalam") and ticker_symbol:
        with st.spinner(f"AI sedang menarik data rahasia pasar untuk {ticker_symbol}..."):
            try:
                data_raw = yf.Ticker(ticker_symbol)
                df = data_raw.history(period="1y")
                info = data_raw.info
                
                if df.empty:
                    st.error("Data tidak ditemukan.")
                    return
                
                df.ta.macd(append=True)
                df.ta.rsi(length=14, append=True)
                df.ta.ema(length=20, append=True)

                tab1, tab2, tab3, tab4 = st.tabs(["🤖 Laporan AI Khusus", "📋 Ringkasan & Harga Lot", "🏢 Fundamental & Valuasi Lengkap", "📈 Grafik Pro"])
                
                with tab1:
                    st.markdown(f"### 🤖 Laporan Rahasia AI untuk Anda")
                    rsi = df['RSI_14'].iloc[-1]
                    nama_perusahaan = info.get('longName', ticker_symbol)
                    
                    st.markdown("<div class='ai-report'>", unsafe_allow_html=True)
                    st.write(generate_ai_insight(info, rsi, nama_perusahaan))
                    st.markdown("</div>", unsafe_allow_html=True)

                with tab2:
                    last_price = df['Close'].iloc[-1]
                    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                    st.markdown("#### 💰 Keputusan Harga Pembelian")
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        if mata_uang == "Rp": st.metric("Harga 1 Lembar", f"Rp {last_price:,.0f}")
                        else: st.metric("Harga 1 Unit", f"$ {last_price:,.2f}")
                    with col_p2:
                        if "Lokal" in jenis_pasar:
                            st.metric("Harga 1 LOT (Minimal Beli)", f"Rp {last_price * 100:,.0f}")
                        else:
                            st.metric("Sistem Pembelian", "Bisa Pecahan (Fraksional)")
                    st.markdown("</div>", unsafe_allow_html=True)

                    skor_beli = 100 - rsi
                    col_gauge1, col_gauge2 = st.columns(2)
                    with col_gauge1:
                        fig_g1 = go.Figure(go.Indicator(mode = "gauge+number", value = skor_beli, title = {'text': "Waktu Tepat Beli?", 'font': {'color': 'white'}}, gauge = {'axis': {'range': [0, 100]}, 'steps': [{'range': [0, 30], 'color': "#ef4444"}, {'range': [30, 70], 'color': "#f59e0b"}, {'range': [70, 100], 'color': "#10b981"}]}))
                        fig_g1.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig_g1, use_container_width=True)
                    with col_gauge2:
                        beta = info.get('beta', 1.0)
                        fig_g2 = go.Figure(go.Indicator(mode = "gauge+number", value = min(abs(beta) * 50, 100) if beta else 50, title = {'text': "Tingkat Risiko Goncangan", 'font': {'color': 'white'}}, gauge = {'axis': {'range': [0, 100]}, 'steps': [{'range': [0, 40], 'color': "#10b981"}, {'range': [40, 70], 'color': "#f59e0b"}, {'range': [70, 100], 'color': "#ef4444"}]}))
                        fig_g2.update_layout(height=250, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig_g2, use_container_width=True)

                with tab3:
                    st.markdown("### 🏢 Fundamental Perusahaan (Kesehatan Bisnis)")
                    st.write("*Penjelasan ini dirancang khusus agar mudah dipahami oleh pemula.*")
                    st.markdown("---")
                    
                    c_fun1, c_fun2 = st.columns(2)
                    with c_fun1:
                        mc = info.get('marketCap', 0)
                        st.write(f"**1. Kapitalisasi Pasar:** {mata_uang} {mc:,.0f}")
                        st.caption("*(Total harga jika Anda ingin membeli seluruh perusahaan ini beserta gedungnya. Semakin besar, semakin aman dari kebangkrutan).*")
                        
                        pe = info.get('trailingPE', 0)
                        st.write(f"**2. Valuasi PER (Price to Earnings):** {pe:.2f}x")
                        st.caption("*(Menunjukkan berapa lama modal Anda akan balik. Di bawah 15x dianggap murah. Di atas 25x dianggap mahal).*")
                        
                        pbv = info.get('priceToBook', 0)
                        st.write(f"**3. Valuasi PBV (Price to Book):** {pbv:.2f}x")
                        st.caption("*(Harga saham dibanding nilai kekayaan perusahaan. Angka 1 artinya harga wajar. Di bawah 1 berarti hancur/sangat murah).*")
                        
                    with c_fun2:
                        pm = info.get('profitMargins', 0) * 100
                        st.write(f"**4. Margin Keuntungan Bersih:** {pm:.2f}%")
                        st.caption("*(Berapa persen laba bersih yang masuk kantong perusahaan dari total penjualannya).*")
                        
                        dy = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
                        st.write(f"**5. Dividen Tahunan:** {dy:.2f}% per tahun")
                        st.caption("*(Bonus uang tunai dari keuntungan perusahaan yang akan ditransfer ke rekening Anda setiap tahun).*")
                        
                        deb = info.get('debtToEquity', 0)
                        st.write(f"**6. Rasio Hutang (Debt to Equity):** {deb}%")
                        st.caption("*(Jika di atas 100%, berarti hutang perusahaan lebih besar dari modalnya. Hati-hati!).*")

                with tab4:
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.8])
                    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Harga'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], line=dict(color='#fbbf24', width=1.5), name='EMA 20'), row=1, col=1)
                    v_colors = ['#10b981' if df.iloc[i]['Close'] >= df.iloc[i]['Open'] else '#ef4444' for i in range(len(df))]
                    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=v_colors, name='Volume'), row=2, col=1)
                    fig.update_layout(template='plotly_dark', height=500, xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error("Gagal menarik data. Coba lagi atau gunakan kode yang valid.")

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
