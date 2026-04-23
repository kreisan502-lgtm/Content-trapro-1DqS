import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta
import time

# ==========================================
# 1. KONFIGURASI TEMA "DARK GOLD PREMIUM"
# ==========================================
st.set_page_config(page_title="BizInvest Pro v6.0", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #0b0f19; color: #ffffff; }
    
    .stButton>button {
        width: 100%; border-radius: 12px;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        color: #fbbf24; font-weight: 800; font-size: 16px; border: 1px solid #d97706;
        padding: 0.8rem; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(217, 119, 6, 0.2);
    }
    .stButton>button:hover {
        transform: translateY(-3px); box-shadow: 0 6px 20px rgba(217, 119, 6, 0.5);
        background: linear-gradient(135deg, #d97706 0%, #b45309 100%); color: white;
    }
    
    div[data-testid="metric-container"] {
        background: #1f2937; border-radius: 12px; padding: 15px;
        border-left: 4px solid #fbbf24; box-shadow: 0 4px 6px rgba(0,0,0,0.5);
    }
    
    /* Notifikasi AI untuk Awam */
    .ai-box {
        background: rgba(217, 119, 6, 0.1); border: 1px solid #fbbf24;
        border-radius: 10px; padding: 20px; margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DATABASE SAHAM LENGKAP (AUTOCOMPLETE)
# ==========================================
DATABASE_SAHAM = [
    # Saham Bank & Keuangan (BEI)
    "BBCA.JK - Bank Central Asia", "BBRI.JK - Bank Rakyat Indonesia", "BMRI.JK - Bank Mandiri", "BBNI.JK - Bank Negara Indonesia", "BRIS.JK - Bank Syariah Indonesia", "ARTO.JK - Bank Jago",
    # Saham Konsumsi & Retail (BEI)
    "ICBP.JK - Indofood CBP", "INDF.JK - Indofood Sukses Makmur", "UNVR.JK - Unilever Indonesia", "AMRT.JK - Alfamart", "CPIN.JK - Charoen Pokphand", "MYOR.JK - Mayora", "MAPI.JK - Mitra Adiperkasa",
    # Saham Energi, Tambang & Komoditas (BEI)
    "ADRO.JK - Adaro Energy", "PTBA.JK - Bukit Asam", "ITMG.JK - Indo Tambangraya", "ANTM.JK - Aneka Tambang", "INCO.JK - Vale Indonesia", "AMMN.JK - Amman Mineral", "BUMI.JK - Bumi Resources", "PGAS.JK - Perusahaan Gas Negara",
    # Saham Infrastruktur & Teknologi (BEI)
    "TLKM.JK - Telkom Indonesia", "GOTO.JK - GoTo Gojek Tokopedia", "ASII.JK - Astra International", "BREN.JK - Barito Renewables", "CUAN.JK - Petrindo Jaya Kreasi",
    # Saham Properti (BEI)
    "LPKR.JK - Lippo Karawaci", "BSDE.JK - Bumi Serpong Damai", "CTRA.JK - Ciputra Development",
    # Global & Crypto
    "AAPL - Apple Inc (US)", "TSLA - Tesla Inc (US)", "NVDA - NVIDIA (US)", "MSFT - Microsoft (US)",
    "BTC-USD - Bitcoin", "ETH-USD - Ethereum", "SOL-USD - Solana"
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
# 4. MODUL AI TRADING (KHUSUS AWAM & PRO)
# ==========================================
def menu_trading():
    col_bck, col_title = st.columns([1, 5])
    with col_bck: st.button("⬅️ KEMBALI", on_click=navigate, args=('home',))
    with col_title: st.markdown("<h2 style='color: #fbbf24; margin-top:-10px;'>📊 Analisis Investasi & Sinyal Pintar</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Kotak Pencarian Pintar
    pilihan_saham = st.selectbox(
        "🔍 Ketik Nama Perusahaan atau Kode Saham (Contoh: ketik 'Bank' atau 'C'):",
        options=["➕ Pilih atau Ketik Nama Saham..."] + DATABASE_SAHAM + ["✍️ Input Manual Kode Lainnya..."],
        index=0
    )
    
    if pilihan_saham == "✍️ Input Manual Kode Lainnya...":
        ticker_symbol = st.text_input("Masukkan Kode Emiten Resmi (Contoh: BRPT.JK)", "").upper()
    elif pilihan_saham != "➕ Pilih atau Ketik Nama Saham...":
        ticker_symbol = pilihan_saham.split(" - ")[0]
    else:
        ticker_symbol = None

    if st.button("🚀 Pindai Kondisi Perusahaan") and ticker_symbol:
        with st.spinner(f"AI sedang memeriksa kesehatan keuangan dan riwayat harga {ticker_symbol}..."):
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

                tab1, tab2, tab3 = st.tabs(["👶 Mode Pemula (Gampang Dipahami)", "📈 Mode Profesional", "🏢 Info Bisnis"])
                
                with tab1:
                    st.markdown("### 💡 Panduan Cerdas untuk Anda")
                    last_price = df['Close'].iloc[-1]
                    rsi = df['RSI_14'].iloc[-1]
                    beta = info.get('beta', 1.0)
                    
                    # Logika Penentu Beli/Jual (Skala 0-100)
                    # Semakin kecil RSI (oversold), semakin bagus untuk beli (skor mendekati 100)
                    skor_beli = 100 - rsi
                    
                    col_gauge1, col_gauge2 = st.columns(2)
                    
                    # Spidometer Sinyal Beli
                    with col_gauge1:
                        fig_gauge1 = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = skor_beli,
                            title = {'text': "Waktu yang Tepat untuk Beli?", 'font': {'size': 20, 'color': 'white'}},
                            gauge = {
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "white"},
                                'steps': [
                                    {'range': [0, 30], 'color': "#ef4444"}, # Merah (Jangan beli)
                                    {'range': [30, 70], 'color': "#f59e0b"}, # Kuning (Cicil)
                                    {'range': [70, 100], 'color': "#10b981"} # Hijau (Bagus untuk beli)
                                ]
                            }
                        ))
                        fig_gauge1.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig_gauge1, use_container_width=True)
                        
                    # Spidometer Risiko
                    with col_gauge2:
                        risiko_val = min(beta * 50, 100) # Normalisasi nilai beta ke 1-100
                        fig_gauge2 = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = risiko_val,
                            title = {'text': "Tingkat Risiko (Goncangan Harga)", 'font': {'size': 20, 'color': 'white'}},
                            gauge = {
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "white"},
                                'steps': [
                                    {'range': [0, 40], 'color': "#10b981"}, # Hijau (Aman)
                                    {'range': [40, 70], 'color': "#f59e0b"}, # Kuning (Sedang)
                                    {'range': [70, 100], 'color': "#ef4444"} # Merah (Bahaya)
                                ]
                            }
                        ))
                        fig_gauge2.update_layout(height=300, paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
                        st.plotly_chart(fig_gauge2, use_container_width=True)

                    # Penjelasan Bahasa Manusia Biasa
                    st.markdown("<div class='ai-box'>", unsafe_allow_html=True)
                    st.markdown(f"#### 🤖 Kesimpulan AI untuk {info.get('shortName', ticker_symbol)}:")
                    st.write(f"Harga satu lembar saat ini adalah **Rp {last_price:,.0f}**.")
                    
                    # Penjelasan Momentum Beli
                    if skor_beli >= 70:
                        st.success("🎯 **Kapan Harus Beli? SEKARANG (Waktu Sangat Bagus).** \nHarga saham ini sedang 'Diskon' atau turun cukup dalam akibat kepanikan pasar. Ini adalah waktu yang direkomendasikan untuk mulai membeli dan menyimpannya.")
                    elif skor_beli <= 30:
                        st.error("🛑 **Kapan Harus Beli? JANGAN SEKARANG (Sedang Kemahalan).** \nSaham ini sedang naik daun dan harganya sangat mahal. Banyak orang yang sudah untung besar dan bersiap menjualnya. Jika Anda beli sekarang, Anda berisiko 'nyangkut' di harga atas. Lebih baik tunggu harga turun.")
                    else:
                        st.warning("⚖️ **Kapan Harus Beli? BOLEH DICICIL.** \nHarga saat ini berada di nilai normal/tengah-tengah. Jika Anda ingin berinvestasi, belilah sedikit demi sedikit (rutin setiap bulan), jangan masukkan semua uang Anda sekaligus.")
                        
                    # Penjelasan Risiko
                    st.markdown("---")
                    if beta < 0.8:
                        st.write("🛡️ **Seberapa Besar Risikonya? RENDAH.** \nPerusahaan ini pergerakan harganya lambat tapi pasti. Sangat aman untuk pemula, orang tua, atau untuk dana pensiun. Anda bisa tidur nyenyak memegang saham ini.")
                    elif beta > 1.2:
                        st.write("🎢 **Seberapa Besar Risikonya? TINGGI.** \nHarga saham ini bisa naik 10% hari ini dan anjlok 10% besok. Sangat bergejolak! **Hanya gunakan 'Uang Dingin'** (uang yang tidak akan Anda pakai dalam 1 tahun ke depan) jika ingin membeli saham ini.")
                    else:
                        st.write("🚶‍♂️ **Seberapa Besar Risikonya? MENENGAH.** \nRisikonya standar seperti bisnis pada umumnya. Naik turunnya wajar.")
                    st.markdown("</div>", unsafe_allow_html=True)

                with tab2: # MODE PROFESIONAL (Untuk yang sudah paham chart)
                    st.markdown("### Terminal Grafik Teknikal")
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.8])
                    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Harga'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], line=dict(color='#fbbf24', width=1.5), name='EMA 20'), row=1, col=1)
                    v_colors = ['#10b981' if df.iloc[i]['Close'] >= df.iloc[i]['Open'] else '#ef4444' for i in range(len(df))]
                    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=v_colors, name='Volume'), row=2, col=1)
                    fig.update_layout(template='plotly_dark', height=550, xaxis_rangeslider_visible=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                    st.plotly_chart(fig, use_container_width=True)

                with tab3: # PROFIL BISNIS
                    st.markdown("### Apa yang Perusahaan ini Lakukan?")
                    st.write(info.get('longBusinessSummary', 'Deskripsi tidak tersedia.'))
                    st.markdown("---")
                    col_f1, col_f2 = st.columns(2)
                    with col_f1:
                        st.write(f"**Industri:** {info.get('industry', 'N/A')}")
                        st.write(f"**Karyawan:** {info.get('fullTimeEmployees', 'N/A')} orang")
                    with col_f2:
                        st.write(f"**Keuntungan Bersih Perusahaan (Profit Margin):** {info.get('profitMargins', 0)*100:.2f}%")
                        st.write(f"*(Jika persentase keuntungan ini minus, berarti perusahaan sedang rugi/bakar uang)*")

            except Exception as e:
                st.error(f"Gagal memproses data. Terjadi kesalahan koneksi ke bursa saham.")

# ==========================================
# 5. MODUL KALKULATOR HPP
# ==========================================
def menu_hpp():
    col_bck, col_title = st.columns([1, 5])
    with col_bck: st.button("⬅️ KEMBALI", on_click=navigate, args=('home',))
    with col_title: st.markdown("<h2 style='color: #fbbf24; margin-top:-10px;'>📦 AI Business & HPP Optimizer</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### Input Biaya Modal")
        bahan = st.number_input("Biaya Bahan Baku (Rp)", value=1000000)
        tenaga = st.number_input("Biaya Tenaga Kerja (Rp)", value=300000)
        lain = st.number_input("Overhead / Operasional (Rp)", value=200000)
    with col_b:
        st.markdown("#### Strategi Penjualan")
        qty = st.number_input("Estimasi Unit Terjual", value=100)
        margin = st.slider("Target Profit Margin (%)", 5, 100, 35)
        
    if st.button("Kalkulasi & Minta Saran AI"):
        total = bahan + tenaga + lain
        hpp = total / qty if qty > 0 else 0
        jual = hpp * (1 + margin/100)
        laba_satuan = jual - hpp
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Modal per Unit (HPP)", f"Rp {hpp:,.0f}")
        c2.metric("Saran Harga Jual", f"Rp {jual:,.0f}")
        c3.metric("Potensi Laba/Unit", f"Rp {laba_satuan:,.0f}")

# ==========================================
# 6. HALAMAN UTAMA (LANDING PAGE)
# ==========================================
if check_password():
    if st.session_state['page'] == 'home':
        st.markdown("<div style='text-align: center; margin-top: 5vh;'>", unsafe_allow_html=True)
        st.markdown("<h1 style='color: #fbbf24; font-size: 3rem;'>BIZINVEST PRO v6.0</h1>", unsafe_allow_html=True)
        st.markdown("<p style='color: #9ca3af; font-size: 1.2rem; margin-bottom: 50px;'>Sahabat Investasi Pintar & Ramah Pemula</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📈 Cek Saham & Analisis Investasi"): navigate('trading')
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📦 Kalkulator Bisnis & HPP"): navigate('hpp')
            
    elif st.session_state['page'] == 'trading': menu_trading()
    elif st.session_state['page'] == 'hpp': menu_hpp()
                    
