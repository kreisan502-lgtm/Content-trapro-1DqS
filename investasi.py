import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta

def show_investasi():
    st.markdown("<h2 style='color: #fbbf24; text-align: center;'>🏦 Intelligent Investment Terminal v10.0</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: gray;'>Data Real-Time & Analisis Fundamental Mendalam</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    # 1. PENCARIAN ASET
    col_search1, col_search2 = st.columns([1, 3])
    with col_search1:
        market = st.selectbox("Pilih Pasar:", ["Indonesia (BEI)", "Global (US)", "Crypto"])
    with col_search2:
        if market == "Indonesia (BEI)":
            ticker = st.text_input("Ketik Kode Saham (Contoh: BBCA.JK, ASII.JK, GOTO.JK):", "BBCA.JK").upper()
        elif market == "Global (US)":
            ticker = st.text_input("Ketik Kode Saham US (Contoh: AAPL, TSLA, NVDA):", "AAPL").upper()
        else:
            ticker = st.text_input("Ketik Kode Crypto (Contoh: BTC-USD, ETH-USD):", "BTC-USD").upper()

    if st.button("🚀 MULAI ANALISIS KOMPREHENSIF"):
        try:
            with st.spinner("Menghubungkan ke Bursa & Menarik Laporan Keuangan..."):
                asset = yf.Ticker(ticker)
                df = asset.history(period="1y")
                info = asset.info
                
                if df.empty:
                    st.error("Data tidak ditemukan. Pastikan kode ticker benar.")
                    return

                # Indikator Teknikal untuk Profesional
                df.ta.rsi(length=14, append=True)
                df.ta.macd(append=True)
                df.ta.ema(length=20, append=True)
                df.ta.ema(length=50, append=True)

                # --- HEADER INFORMASI UTAMA ---
                c_header1, c_header2, c_header3 = st.columns([2, 1, 1])
                with c_header1:
                    st.subheader(f"🏢 {info.get('longName', ticker)}")
                    st.write(f"**Sektor:** {info.get('sector', 'N/A')} | **Industri:** {info.get('industry', 'N/A')}")
                with c_header2:
                    current_price = df['Close'].iloc[-1]
                    currency = "Rp" if ".JK" in ticker else "$"
                    st.metric("Harga Terakhir", f"{currency} {current_price:,.2f}", f"{((current_price - df['Close'].iloc[-2])/df['Close'].iloc[-2]*100):.2f}%")
                with c_header3:
                    st.metric("Volume 24 Jam", f"{df['Volume'].iloc[-1]:,.0f}")

                # --- NAVIGATION TABS ---
                tab1, tab2, tab3, tab4 = st.tabs([
                    "🤖 AI Investor Advisor", 
                    "💎 Analisis Fundamental & Valuasi", 
                    "📊 Grafik Teknikal Pro", 
                    "📂 Profil & Laporan Internal"
                ])

                # --- TAB 1: AI ADVISOR (UNTUK PEMULA) ---
                with tab1:
                    st.markdown("### 🤖 Rekomendasi Berbasis Kecerdasan Buatan")
                    rsi = df['RSI_14'].iloc[-1]
                    beta = info.get('beta', 1.0)
                    
                    st.markdown("<div style='background: rgba(251, 191, 36, 0.1); padding: 20px; border-radius: 10px; border-left: 5px solid #fbbf24;'>", unsafe_allow_html=True)
                    if rsi < 35:
                        st.success("🎯 **STATUS: BUY (DISCOUNT).** Harga sedang 'lelah' jatuh. Secara statistik, peluang memantul naik sangat tinggi. Cocok untuk koleksi.")
                    elif rsi > 65:
                        st.error("🛑 **STATUS: OVERBOUGHT (MAHAL).** Harga sedang euforia. Risiko 'nyangkut' sangat besar. Tunggu koreksi di area EMA 20.")
                    else:
                        st.info("⚖️ **STATUS: NEUTRAL.** Harga bergerak stabil. Disarankan beli secara bertahap (DCA).")
                    
                    st.markdown(f"**Tingkat Risiko:** {'TINGGI' if beta > 1.2 else 'RENDAH' if beta < 0.8 else 'MODERAT'}")
                    st.write(f"Aset ini memiliki volatilitas sebesar {beta:.2f}x lipat dari pasar. {'Waspada goncangan!' if beta > 1.2 else 'Cenderung stabil.'}")
                    st.markdown("</div>", unsafe_allow_html=True)

                # --- TAB 2: FUNDAMENTAL (UNTUK PROFESIONAL) ---
                with tab2:
                    st.markdown("### 💎 Metrik Fundamental (Value Investing)")
                    f1, f2, f3 = st.columns(3)
                    
                    # Kolom 1: Valuasi
                    with f1:
                        st.write("**📊 Valuasi (Murah/Mahal)**")
                        per = info.get('trailingPE', 0)
                        pbv = info.get('priceToBook', 0)
                        st.write(f"• PER Ratio: {per:.2f}x")
                        st.write(f"• PBV Ratio: {pbv:.2f}x")
                        st.caption("PER < 15 & PBV < 1 sering dianggap 'Salah Harga' atau Murah.")

                    # Kolom 2: Profitabilitas
                    with f2:
                        st.write("**💰 Profitabilitas**")
                        roe = info.get('returnOnEquity', 0) * 100
                        npm = info.get('profitMargins', 0) * 100
                        st.write(f"• ROE: {roe:.2f}%")
                        st.write(f"• Net Profit Margin: {npm:.2f}%")
                        st.caption("ROE > 15% menandakan perusahaan sangat efisien mencetak laba.")

                    # Kolom 3: Dividen & Cash
                    with f3:
                        st.write("**🎁 Bonus & Dividen**")
                        dy = info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0
                        der = info.get('debtToEquity', 0)
                        st.write(f"• Dividend Yield: {dy:.2f}%")
                        st.write(f"• Debt to Equity (DER): {der:.2f}%")
                        st.caption("DER < 100% menandakan hutang yang sehat & terkendali.")

                # --- TAB 3: GRAFIK TEKNIKAL ---
                with tab3:
                    st.markdown("### 📊 Interactive Pro Chart")
                    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.8])
                    
                    # Candlestick
                    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], name='Price'), row=1, col=1)
                    # EMA Lines
                    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_20'], line=dict(color='#fbbf24', width=1), name='EMA 20 (Trend Jangka Pendek)'), row=1, col=1)
                    fig.add_trace(go.Scatter(x=df.index, y=df['EMA_50'], line=dict(color='#00d2ff', width=1), name='EMA 50 (Trend Jangka Menengah)'), row=1, col=1)
                    # Volume
                    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='gray'), row=2, col=1)

                    fig.update_layout(template='plotly_dark', height=600, xaxis_rangeslider_visible=False, margin=dict(l=0, r=0, t=0, b=0))
                    st.plotly_chart(fig, use_container_width=True)

                # --- TAB 4: PROFIL INTERNAL ---
                with tab4:
                    st.markdown("### 📂 Corporate Business Summary")
                    st.write(info.get('longBusinessSummary', 'Data deskripsi tidak tersedia.'))
                    st.markdown("---")
                    st.write(f"**Website Resmi:** {info.get('website', 'N/A')}")
                    st.write(f"**Total Karyawan:** {info.get('fullTimeEmployees', 'N/A')}")

        except Exception as e:
            st.error(f"⚠️ Terjadi kesalahan: {e}. Pastikan simbol ticker sudah benar.")
