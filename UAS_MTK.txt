import streamlit as st
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="EOQ – Economic Order Quantity", layout="centered")

# Judul Aplikasi
st.title("📦 EOQ – Economic Order Quantity")

# Input pengguna
D = st.number_input("Permintaan Tahunan (unit)", value=1000)
S = st.number_input("Biaya Pemesanan per Order (Rp)", value=50000)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

# Tombol hitung EOQ
if st.button("Hitung EOQ"):
    EOQ = sqrt((2 * D * S) / H)
    st.success(f"EOQ: {EOQ:.2f} unit")

    # Grafik Total Cost
    Q = np.linspace(1, 2 * EOQ, 500)
    TC = (D / Q) * S + (Q / 2) * H

    plt.figure()
    plt.plot(Q, TC, label='Total Cost')
    plt.axvline(EOQ, color='r', linestyle='--', label=f'EOQ = {EOQ:.2f}')
    plt.title("Total Biaya vs. Kuantitas Order")
    plt.xlabel("Order Quantity (Q)")
    plt.ylabel("Total Biaya (Rp)")
    plt.legend()
    st.pyplot(plt)
