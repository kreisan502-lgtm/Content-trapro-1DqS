import streamlit as st

def show_hpp():
    st.markdown("<h2 style='color: #fbbf24;'>📦 AI Business & HPP Optimizer</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("#### 📝 Input Biaya Produksi")
        bahan = st.number_input("Total Bahan Baku (Rp)", value=1500000, step=50000)
        tenaga = st.number_input("Total Tenaga Kerja (Rp)", value=500000, step=50000)
        lain = st.number_input("Biaya Operasional (Rp)", value=200000, step=10000)
    with col_b:
        st.markdown("#### 🎯 Strategi Profit")
        qty = st.number_input("Berapa Unit Dihasilkan?", value=100, min_value=1)
        margin = st.slider("Target Keuntungan Bersih (%)", 5, 100, 35)
        
    if st.button("🚀 Hitung Struktur Harga"):
        total = bahan + tenaga + lain
        hpp = total / qty
        jual = hpp * (1 + margin/100)
        
        st.markdown("---")
        c1, c2, c3 = st.columns(3)
        c1.metric("Modal/Unit (HPP)", f"Rp {hpp:,.0f}")
        c2.metric("Harga Jual Ideal", f"Rp {jual:,.0f}")
        c3.metric("Laba Bersih/Pcs", f"Rp {jual-hpp:,.0f}")
