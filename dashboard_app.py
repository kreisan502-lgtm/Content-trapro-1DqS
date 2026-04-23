import streamlit as st

def show_main_dashboard():
    st.markdown("<h1 style='text-align: center; color: #fbbf24; margin-top: -50px;'>👑 VIP TERMINAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #94a3b8;'>Solusi Analisis Investasi & Bisnis</p>", unsafe_allow_html=True)
    st.write("---")
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container(border=True):
            st.subheader("📈 Terminal Analisis")
            st.write("Pantau pergerakan aset & teknikal analisis real-time.")
            if st.button("BUKA TERMINAL", key="btn_inv", use_container_width=True):
                st.session_state.page = "investasi"; st.rerun()

    with col2:
        with st.container(border=True):
            st.subheader("🧮 Kalkulator Bisnis")
            st.write("Hitung HPP dan analisis keuangan bisnis Anda.")
            if st.button("BUKA KALKULATOR", key="btn_hpp", use_container_width=True):
                st.session_state.page = "hpp"; st.rerun()
              
