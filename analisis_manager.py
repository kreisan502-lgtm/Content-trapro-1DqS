import streamlit as st
import saham_engine

def show_menu():
    st.markdown("### 📊 Panel Analisis Instrumen")
    
    # Sub-menu menggunakan Button Group agar terlihat profesional
    col1, col2, col3, col4 = st.columns(4)
    if 'sub_analisis' not in st.session_state:
        st.session_state.sub_analisis = "Emas"

    if col1.button("🟡 Emas", use_container_width=True): st.session_state.sub_analisis = "Emas"
    if col2.button("🇮🇩 Saham Indo", use_container_width=True): st.session_state.sub_analisis = "Indo"
    if col3.button("🌎 Saham Luar", use_container_width=True): st.session_state.sub_analisis = "Luar"
    if col4.button("🚀 Crypto", use_container_width=True): st.session_state.sub_analisis = "Crypto"

    st.write("---")

    if st.session_state.sub_analisis == "Indo":
        st.subheader("🇮🇩 Pasar Saham Bursa Efek Indonesia")
        # Panggil Engine Pencarian
        saham_engine.render_saham_selector(market="Indo")

    elif st.session_state.sub_analisis == "Luar":
        st.subheader("🌎 Global Market (Wall Street)")
        saham_engine.render_saham_selector(market="Luar")
        
    elif st.session_state.sub_analisis == "Emas":
        st.write("Analisis Harga Emas Real-time...")
        # Tambahkan fungsi emas di sini nanti
      
