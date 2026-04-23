import streamlit as st
import time  # <--- TAMBAHKAN BARIS INI
from investasi import show_investasi
from kalkulator import show_hpp

# CSS UI Premium
st.set_page_config(page_title="BizInvest VIP Suite", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #0b0f19; color: white; }
    .stButton>button {
        width: 100%; border-radius: 12px;
        background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        color: #fbbf24; font-weight: bold; border: 1px solid #d97706; padding: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ... (sisa kode lainnya tetap sama)
