import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_ta as ta

def show_investasi():
    st.markdown("<h2 style='color: #fbbf24;'>📈 Terminal Investasi Global v10.0</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Database Terintegrasi
    pasar = st.radio("Pilih Market:", ["Indonesia (BEI)", "Global (US)", "Crypto"], horizontal=True)
    ticker = st.text_input("Ketik Kode Saham/Aset (Contoh: BBCA.JK, AAPL, atau BTC-USD)", "BBCA.JK").upper()

    if st.button("🔍 Mulai Analisis Mendalam"):
        try:
            with st.spinner("AI sedang memproses data real-time..."):
                data = yf.Ticker(ticker)
                df = data.history(period="1y")
                if df.empty:
                    st.error("Data tidak ditemukan.")
                    return
                
                # Teknikal Indikator
                df.ta.rsi(append=True)
                df.ta.ema(length=20, append=True)
                
                tab1, tab2 = st.tabs(["🤖 Analisis AI & Fundamental", "📊 Grafik Pro"])
                
                with tab1:
                    last_price = df['Close'].iloc[-1]
                    info = data.info
                    st.markdown(f"### {info.get('longName', ticker)}")
                    
                    c1, c2 = st.columns(2)
                    c1.metric("Harga Saat Ini", f"{last_price:,.2f}")
                    c2.metric("Rasio Hutang (DER)", f"{info.get('debtToEquity', 0)}%")
                    
                    st.markdown("#### 🤖 Kesimpulan Pintar AI:")
                    rsi = df['RSI_14'].iloc[-1]
                    if rsi < 35:
                        st.success("🎯 **SINYAL: DISKON BESAR.** Banyak orang panik menjual, saatnya Anda beli di harga murah.")
                    elif rsi > 65:
                        st.error("🛑 **SINYAL: KEMAHALAN.** Jangan beli sekarang, Anda rawan nyangkut di harga tinggi.")
                    else:
                        st.warning("⚖️ **SINYAL: NETRAL.** Harga stabil, cocok untuk cicil rutin (DCA).")
                
                with tab2:
                    fig = make_subplots(rows=1, cols=1)
                    fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close']))
                    fig.update_layout(template='plotly_dark', height=500, xaxis_rangeslider_visible=False)
                    st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error: {e}")
          
