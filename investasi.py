import streamlit as st
import analisis_manager
import panduan
import book_guide

def show_investasi():
    # Menggunakan container agar tampilan rapi di tengah
    st.markdown("<h2 style='text-align: center; color: #fbbf24;'>💎 VIP INVESTMENT TERMINAL</h2>", unsafe_allow_html=True)
    
    # Inisialisasi state menu jika belum ada
    if 'menu_aktif' not in st.session_state:
        st.session_state.menu_aktif = "Analisis"

    # Barisan Tombol Menu Utama (Tampilan Tatap Muka)
    # Dibuat besar agar mudah diklik sesuai permintaan
    st.write("---")
    m1, m2, m3 = st.columns(3)
    
    with m1:
        if st.button("📊 ANALISIS\nINSTRUMEN", use_container_width=True, key="main_btn_analisis"):
            st.session_state.menu_aktif = "Analisis"
            
    with m2:
        if st.button("📚 PANDUAN\nPEMULA", use_container_width=True, key="main_btn_guide"):
            st.session_state.menu_aktif = "Guide"
            
    with m3:
        if st.button("📖 BOOK\nGUIDE VIP", use_container_width=True, key="main_btn_book"):
            st.session_state.menu_aktif = "Book"
    
    st.write("---")

    # LOGIKA PEMANGGILAN FILE LAIN
    # Menu ini tidak akan hilang saat refresh karena status disimpan di session_state
    
    if st.session_state.menu_aktif == "Analisis":
        # Memanggil file analisis_manager.py yang sudah kita buat tadi
        analisis_manager.show_menu()

    elif st.session_state.menu_aktif == "Guide":
        # Memanggil file panduan.py
        st.markdown("### 📚 Panduan Investasi Langkah Demi Langkah")
        panduan.show_content()

    elif st.session_state.menu_aktif == "Book":
        # Memanggil file book_guide.py
        st.markdown("### 📖 Perpustakaan Strategi & Psikologi")
        book_guide.show_content()

    # Footer Informasi Aktif
    st.sidebar.markdown("---")
    st.sidebar.info(f"📍 Menu Aktif: {st.session_state.menu_aktif}")
    
