import streamlit as st
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt

# Konfigurasi halaman
st.set_page_config(page_title="EOQ – Economic Order Quantity", layout="centered")

# Judul Aplikasi
st.title("📦 EOQ – Economic Order Quantity")

# Penjelasan EOQ
st.markdown(r"""
**Economic Order Quantity (EOQ)** adalah jumlah pembelian optimal yang meminimalkan total biaya persediaan, yaitu **biaya pemesanan** dan **biaya penyimpanan**.

Rumus EOQ:

\[
EOQ = \sqrt{\frac{2DS}{H}}
\]

Keterangan:
- \( D \): Permintaan tahunan (unit per tahun)  
- \( S \): Biaya pemesanan per order (Rp)  
- \( H \): Biaya penyimpanan per unit per tahun (Rp)

Aplikasi ini akan menghitung EOQ berdasarkan input Anda dan menampilkan grafik hubungan antara kuantitas pemesanan dan total biaya.
""")

# Input pengguna
D = st.number_input("Permintaan Tahunan (unit)", value=1000)
S = st.number_input("Biaya Pemesanan per Order (Rp)", value=50000)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (Rp)", value=2000)

# Tombol hitung EOQ
if st.button("Hitung EOQ"):
    EOQ = sqrt((2 * D * S) / H)
    st.success(f"EOQ: {EOQ:.2f} unit")

    # Grafik Total Biaya
    Q = np.linspace(1, 2 * EOQ, 500)
    total_cost = (D / Q) * S + (Q / 2) * H

    plt.figure(figsize=(8, 5))
    plt.plot(Q, total_cost, label='Total Biaya', color='blue')
    plt.axvline(EOQ, color='red', linestyle='--', label=f'EOQ = {EOQ:.2f}')
    plt.title("Total Biaya vs Kuantitas Order")
    plt.xlabel("Kuantitas Order (Q)")
    plt.ylabel("Total Biaya (Rp)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()

    # Tampilkan grafik
    st.pyplot(plt.gcf())
