import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta

# ==========================================
# 1. KONFIGURASI TEMA "DARK GOLD PREMIUM"
# ==========================================
st.set_page_config(page_title="BizInvest Pro v7.0", layout="wide", initial_sidebar_state="collapsed")

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
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE SAHAM LENGKAP & AKURAT
# ==========================================
DB_LOKAL = [
    "BBCA.JK - PT Bank Central Asia Tbk", "BBRI.JK - PT Bank Rakyat Indonesia (Persero) Tbk", 
    "BMRI.JK - PT Bank Mandiri (Persero) Tbk", "BBNI.JK - PT Bank Negara Indonesia (Persero) Tbk", 
    "TLKM.JK - PT Telkom Indonesia (Persero) Tbk", "ASII.JK - PT Astra International Tbk", 
    "GOTO.JK - PT GoTo Gojek Tokopedia Tbk", "ADRO.JK - PT Adaro Energy Indonesia Tbk", 
    "PTBA.JK - PT Bukit Asam Tbk", "ANTM.JK - PT Aneka Tambang Tbk", 
    "ICBP.JK - PT Indofood CBP Sukses Makmur Tbk", "UNVR.JK - PT Unilever Indonesia Tbk",
    "CPIN.JK - PT Charoen Pokphand Indonesia Tbk", "AMMN.JK - PT Amman Mineral Internasional Tbk",
    "BRPT.JK - PT Barito Pacific Tbk", "BUMI.JK - PT Bumi Resources Tbk"
]

DB_GLOBAL = [
    "AAPL - Apple Inc.", "MSFT - Microsoft Corporation", "TSLA - Tesla, Inc.", 
    "NVDA - NVIDIA Corporation", "AMZN - Amazon.com, Inc.", "GOOGL - Alphabet Inc. (Google)", 
    "META - Meta Platforms, Inc. (Facebook)", "NFLX - Netflix, Inc."
]

DB_KRIPTO = [
    "BTC-USD - Bitcoin", "ETH-USD - Ethereum", "SOL-USD - Solana", 
    "BNB-USD - Binance Coin", "XRP-USD - Ripple", "DOGE-USD - Dogecoin"
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
            st.text_input("Masukkan Lisensi:", type="password", key="pwd_input")
            if st.button("Masuk"):
                if st.session_state.pwd_input == "AksesPremium123":
                    st.session_state["password_correct"] = True
                    st.rerun()
                else: st.error("❌ Lisensi tidak valid.")
        return False
    return st.session_state["password_correct"]

# ==========================================
# 4. MODUL AI TRADING SANGAT DETAIL
# ==========================================
def menu_trading():
    col_bck, col_title = st.columns([1, 5])
    with col_bck: st.button("⬅️ KEMBALI MENU", on_click=navigate, args=('home',))
    with col_title: st.markdown("<h3 style='color: #fbbf24; margin-top:-5px;'>📊 Terminal Analisis Real-Time</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    # FILTER PASAR
    jenis_pasar = st.radio("🌍 Pilih Kategori Pasar:", ["🇮🇩 Saham Lokal (Bursa Efek Indonesia)", "🇺🇸 Saham Global (Wall Street)", "🪙 Aset Kripto (Cryptocurrency)"], horizontal=True)
    
    # MENENTUKAN LIST DROPDOWN BERDASARKAN PASAR
    if "Lokal" in jenis_pasar:
        options_list = DB_LOKAL
        mata_uang = "Rp"
        tipe_aset = "Saham (Ekuitas Publik)"
    elif "Global" in jenis_pasar:
        options_list = DB_GLOBAL
        mata_uang = "$"
        tipe_aset = "Saham Global (Ekuitas US)"
    else:
        options_list = DB_KRIPTO
        mata_uang = "$"
        tipe_aset = "Mata Uang Kripto (Aset Digital)"

    pilihan_saham = st.selectbox(
        "🔍 Cari Nama Perusahaan atau Kode:",
        options=["➕ Pilih/Ketik di sini..."] + options_list + ["✍️ Input Manual Kode Ticker..."]
    )
    
    if pilihan_saham == "✍️ Input Manual Kode Ticker...":
        ticker_symbol = st.text_input("Ketik Kode Resmi (Contoh: ARTO.JK)", "").upper()
    elif pilihan_saham != "➕ Pilih/Ketik di sini...":
        ticker_symbol = pilihan_saham.split(" - ")[0]
    else:
        ticker_symbol = None

    if st.button("🚀 Pindai Kondisi Real-Time") and ticker_symbol:
        with st.spinner(f"Mengambil data langsung dari bursa untuk {ticker_symbol}..."):
            try:
                data_raw = yf.Ticker(ticker_symbol)
                df = data_raw.history(period="1y")
                info = data_raw.info
                
                if df.empty:
                    st.error("Data tidak ditemukan. Pastikan kode benar.")
                    return
                
                df.ta.macd(append=True)
                df.ta.rsi(length=14, append=True)
                df.ta.ema(length=20, append=True)
                df.ta.ema(length=50, append=True)

                tab1, tab2, tab3 = st.tabs(["👶 Laporan Pemula & Harga Lot", "📈 Terminal Pro Chart", "🏢 Detail Perusahaan"])
                
                with tab1:
                    st.markdown(f"### 📋 Ringkasan Aset: {info.get('longName', ticker_symbol)}")
                    st.write(f"**Kategori:** {tipe_aset} | **Sektor:** {info.get('sector', 'Teknologi/Keuangan')}")
                    
                    last_price = df['Close'].iloc[-1]
                    
                    # PERHITUNGAN HARGA PER LEMBAR DAN PER LOT
                    st.markdown("<div class='info-box'>", unsafe_allow_html=True)
                    st.markdown("#### 💰 Rincian Harga Pembelian")
                    col_p1, col_p2 = st.columns(2)
                    with col_p1:
                        if mata_uang == "Rp":
                            st.metric("Harga 1 Lembar Saham", f"Rp {last_price:,.0f}")
                        else:
                            st.metric("Harga 1 Unit Aset", f"$ {last_price:,.2f}")
                            
                    with col_p2:
                        if "Lokal" in jenis_pasar:
                            harga_lot = last_price * 100
                            st.metric("Harga 1 LOT (Minimal Beli)", f"Rp {harga_lot:,.0f}")
                            st.caption("*Di Indonesia, Anda wajib membeli minimal 1 Lot (100 lembar saham).")
                        else:
                            st.metric("Minimal Pembelian", "Bisa Pecahan (Fraksional)")
                            st.caption("*Aset global/kripto dapat dibeli dalam bentuk pecahan (misal: 0.1 atau 0.005 unit) tergantung aplikasi broker Anda.")
                    st.markdown("</div>", unsafe_allow_html=True)

                    # LOGIKA AI & SPIDOMETER
                    rsi = df['RSI_14'].iloc[-1]
                    beta = info.get('beta', 1.0)
                    skor_beli = 100 - rsi
                    
                    st.markdown("### 🤖 Panduan Keputusan AI")
                    col_gauge1, col_gauge2 = st.columns(2)
                    
                    with col_gauge1:
                        fig_gauge1 = go.Figure(go.Indicator(
                            mode = "gauge+number", value = skor_beli,
                            title = {'text': "Waktu yang Tepat untuk Beli?", 'font': {'size': 16, 'color': 'white'}},
                            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "white"},
                                     'steps': [{'range': [0, 30], 'color': "#ef4444"}, {'range': [30, 70], 'color': "#f59e0b"}, {'range': [70, 100], 'color': "#10b981"}]}
                        ))
                        fig_gauge1.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig_gauge1, use_container_width=True)
                        
                        if skor_beli >= 70: st.success("🎯 **KESIMPULAN: BELI.** Harga sedang jatuh/diskon. Momen bagus untuk masuk.")
                        elif skor_beli <= 30: st.error("🛑 **KESIMPULAN: JANGAN BELI.** Harga sedang di puncak termahal. Rawan turun.")
                        else: st.warning("⚖️ **KESIMPULAN: NETRAL.** Boleh dibeli dengan cara dicicil sedikit-sedikit.")

                    with col_gauge2:
                        risiko_val = min(abs(beta) * 50, 100) if beta else 50
                        fig_gauge2 = go.Figure(go.Indicator(
                            mode = "gauge+number", value = risiko_val,
                            title = {'text': "Tingkat Risiko Goncangan", 'font': {'size': 16, 'color': 'white'}},
                            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "white"},
                                     'steps': [{'range': [0, 40], 'color': "#10b981"}, {'range': [40, 70], 'color': "#f59e0b"}, {'range': [70, 100], 'color': "#ef4444"}]}
                        ))
                        fig_gauge2.update_layout(height=250, margin=dict(l=20, r=20, t=50, b=20), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig_gauge2, use_container_width=True)
                        
                        if risiko_val < 40: st.success("🛡️ **RISIKO RENDAH.** Pergerakan harga lambat dan stabil. Aman untuk pemula.")
                        elif risiko_val > 70: st.error("🎢 **RISIKO TINGGI.** Harga naik-turun dengan sangat ganas. Hanya untuk trader nekat.")
                        else: st.warning("🚶‍♂️ **RISIKO SEDANG.** Fluktuasi normal layaknya bisnis pada umumnya.")

                with tab2:
                    st.markdown("### Terminal Grafik Interaktif")
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.8])
                    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Harga'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], line=dict(color='#fbbf24', width=1.5), name='EMA 20'), row=1, col=1)
                    v_colors = ['#10b981' if df.iloc[i]['Close'] >= df.iloc[i]['Open'] else '#ef4444' for i in range(len(df))]
                    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=v_colors, name='Volume'), row=2, col=1)
                    fig.update_layout(template='plotly_dark', height=550, xaxis_rangeslider_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)

                with tab3:
                    st.markdown("### Profil Lengkap Perusahaan")
                    col_info1, col_info2 = st.columns(2)
                    with col_info1:
                        st.write(f"**Nama Resmi Hukum:** {info.get('longName', 'Tidak tersedia')}")
                        st.write(f"**Tipe Bisnis (Industri):** {info.get('industry', 'Tidak tersedia')}")
                        st.write(f"**Jumlah Pegawai:** {info.get('fullTimeEmployees', 'Tidak dicantumkan')} orang")
                    with col_info2:
                        st.write(f"**Margin Laba Bersih:** {info.get('profitMargins', 0)*100:.2f}% *(Keuntungan yang masuk kantong perusahaan)*")
                        st.write(f"**Situs Web Resmi:** {info.get('website', 'Tidak dicantumkan')}")
                    
                    st.markdown("---")
                    st.markdown("#### Ringkasan Apa yang Mereka Jual/Lakukan:")
                    st.write(info.get('longBusinessSummary', 'Data profil tidak tersedia secara publik dari bursa.'))

            except Exception as e:
                st.error("Gagal mengambil data. Bursa mungkin sedang tutup atau kode tidak valid.")

# ==========================================
# 5. MODUL KALKULATOR HPP
# ==========================================
def menu_hpp():
    col_bck, col_title = st.columns([1, 5])
    with col_bck: st.button("⬅️ KEMBALI MENU", on_click=navigate, args=('home',))
    with col_title: st.markdown("<h3 style='color: #fbbf24; margin-top:-5px;'>📦 AI Kalkulator Harga Jual (HPP)</h3>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 1. Input Biaya Pengeluaran")
        bahan = st.number_input("Total Biaya Bahan Baku (Rp)", value=1500000)
        tenaga = st.number_input("Total Biaya Tukang/Karyawan (Rp)", value=500000)
        lain = st.number_input("Biaya Lain (Listrik, Bensin, dll) (Rp)", value=200000)
    with col_b:
        st.markdown("#### 2. Target Penjualan")
        qty = st.number_input("Berapa Pcs/Unit yang Dihasilkan?", value=100)
        margin = st.slider("Target Keuntungan Bersih (%)", 5, 100, 35)
        
    if st.button("Hitung Otomatis"):
        total = bahan + tenaga + lain
        hpp = total / qty if qty > 0 else 0
        jual = hpp * (1 + margin/100)
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Modal Pembuatan 1 Pcs (HPP)", f"Rp {hpp:,.0f}")
        c2.metric("Harga Jual Disarankan ke Pembeli", f"Rp {jual:,.0f}")
        c3.metric("Keuntungan Bersih per Pcs", f"Rp {jual-hpp:,.0f}")

# ==========================================
# 6. HALAMAN UTAMA (LANDING PAGE)
# ==========================================
if check_password():
    if st.session_state['page'] == 'home':
        st.markdown("<div style='text-align: center; margin-top: 5vh;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #fbbf24; font-size: 3.5rem; margin-bottom: 0px;'>BIZINVEST PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 1.2rem; margin-bottom: 50px;'>Sahabat Investasi Pintar & Kalkulator Bisnis UMKM</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.button("📈 Cek Saham & Panduan Investasi", on_click=navigate, args=('trading',))
            st.markdown("<br>", unsafe_allow_html=True)
            st.button("📦 Kalkulator Modal & Harga Jual", on_click=navigate, args=('hpp',))
            
    elif st.session_state['page'] == 'trading': menu_trading()
    elif st.session_state['page'] == 'hpp': menu_hpp()
                        
