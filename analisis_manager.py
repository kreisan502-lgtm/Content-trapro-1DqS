import streamlit as st
import saham_engine  # Mengimpor mesin pencari otomatis

def show_menu():
    """Fungsi utama untuk menampilkan menu analisis investasi"""
    
    st.markdown("""
        <style>
        .sub-header {
            background-color: #1e293b;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            border-bottom: 3px solid #fbbf24;
        }
        </style>
        <div class="sub-header">
            <h2 style="margin:0; color:#fbbf24;">📊 TERMINAL ANALISIS PRO</h2>
            <p style="margin:0; color:#94a3b8; font-size:14px;">Data Real-time & Edukasi Investasi Terintegrasi</p>
        </div>
    """, unsafe_allow_html=True)

    # Inisialisasi State untuk Sub-Menu agar tidak reset saat klik
    if 'sub_pilihan' not in st.session_state:
        st.session_state.sub_pilihan = "🇮🇩 Saham Indonesia"

    # Barisan Tombol Navigasi (UI Modern)
    col1, col2, col3, col4 = st.columns(4)
    
    if col1.button("🟡 EMAS", use_container_width=True):
        st.session_state.sub_pilihan = "🟡 Emas"
    if col2.button("🇮🇩 SAHAM INDO", use_container_width=True):
        st.session_state.sub_pilihan = "🇮🇩 Saham Indonesia"
    if col3.button("🌎 SAHAM LUAR", use_container_width=True):
        st.session_state.sub_pilihan = "🌎 Saham Luar Negeri"
    if col4.button("🚀 CRYPTO", use_container_width=True):
        st.session_state.sub_pilihan = "🚀 Crypto"

    st.write("---")

    # LOGIKA PER PINDAHAN MENU
    if st.session_state.sub_pilihan == "🟡 Emas":
        render_emas_section()
    
    elif st.session_state.sub_pilihan == "🇮🇩 Saham Indonesia":
        # Memanggil mesin pencari otomatis dari saham_engine.py
        saham_engine.render_saham_selector("Indo")

    elif st.session_state.sub_pilihan == "🌎 Saham Luar Negeri":
        # Memanggil mesin pencari otomatis dari saham_engine.py
        saham_engine.render_saham_selector("Luar")
        
    elif st.session_state.sub_pilihan == "🚀 Crypto":
        render_crypto_section()

def render_emas_section():
    st.subheader("🟡 Analisis Logam Mulia (Emas)")
    st.info("Fitur ini menampilkan harga emas Antam dan Global spot.")
    
    # Contoh penggunaan expander untuk edukasi (Sesuai permintaan: Sembunyikan detail)
    with st.expander("📖 Mengapa Harus Investasi Emas? (Penting untuk Pemula)"):
        st.markdown("""
        **Emas adalah Safe Haven.** Artinya, saat ekonomi dunia sedang kacau atau inflasi tinggi, harga emas cenderung naik atau stabil.
        
        **Keuntungan:**
        1. **Lindung Nilai:** Menjaga kekayaan Anda dari penurunan nilai mata uang.
        2. **Mudah Dijual:** Bisa dicairkan menjadi uang tunai kapan saja di toko emas atau pegadaian.
        3. **Tanpa Bunga:** Berbeda dengan tabungan bank, emas tidak memiliki biaya admin bulanan.
        
        **Langkah Investasi:**
        1. Beli saat harga sedang koreksi (turun tipis).
        2. Simpan minimal 3-5 tahun untuk melihat keuntungan signifikan.
        """)
    
    # Integrasi pencarian harga emas global (Simulasi menggunakan Ticker GC=F)
    saham_engine.tampilkan_detail_rinci("GC=F")

def render_crypto_section():
    st.subheader("🚀 Analisis Aset Kripto")
    st.warning("Perhatian: Crypto memiliki volatilitas sangat tinggi. Gunakan dana dingin.")
    
    # Gunakan mesin pencari otomatis tapi khusus untuk Crypto
    # User bisa ketik BTC-USD, ETH-USD, dll.
    saham_engine.render_saham_selector("Crypto")
    
    with st.expander("📖 Panduan Belajar Crypto & Blockchain"):
        st.markdown("""
        **Apa itu Crypto?** Aset digital yang menggunakan teknologi kriptografi untuk keamanan transaksi. Tidak dikontrol oleh Bank Sentral mana pun.
        
        **Istilah Penting:**
        - **HODL:** Menahan aset dalam jangka waktu sangat lama.
        - **Wallet:** Dompet digital tempat menyimpan aset Anda.
        - **Halving:** Peristiwa 4 tahunan Bitcoin yang biasanya memicu kenaikan harga.
        """)
