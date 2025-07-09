import streamlit as st
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import pandas as pd

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

Aplikasi ini akan menghitung EOQ berdasarkan input Anda dan menampilkan grafik serta memungkinkan ekspor hasil.
""")

# Input pengguna
st.subheader("📝 Input Parameter")
D = st.slider("Permintaan Tahunan (D)", min_value=100, max_value=10000, value=1000, step=100)
S = st.slider("Biaya Pemesanan per Order (S)", min_value=1000, max_value=100000, value=50000, step=1000)
H = st.slider("Biaya Penyimpanan per Unit per Tahun (H)", min_value=100, max_value=10000, value=2000, step=100)

# Tombol hitung EOQ
if st.button("🔍 Hitung EOQ"):
    EOQ = sqrt((2 * D * S) / H)
    st.success(f"EOQ Optimal: {EOQ:.2f} unit")

    # Buat grafik
    Q = np.linspace(1, 2 * EOQ, 500)
    total_cost = (D / Q) * S + (Q / 2) * H

    plt.figure(figsize=(8, 5))
    plt.plot(Q, total_cost, label='Total Biaya (Rp)', color='blue')
    plt.axvline(EOQ, color='red', linestyle='--', label=f'EOQ = {EOQ:.2f}')
    plt.title("📊 Total Biaya vs Kuantitas Order")
    plt.xlabel("Kuantitas Order (Q)")
    plt.ylabel("Total Biaya (Rp)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt.gcf())

    # Export ke CSV
    df = pd.DataFrame({
        'Order Quantity (Q)': Q,
        'Total Cost (Rp)': total_cost
    })

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Hasil dalam CSV",
        data=csv,
        file_name='hasil_perhitungan_eoq.csv',
        mime='text/csv'
    )

    # Info tambahan
    st.info(f"Semakin dekat kuantitas ke {EOQ:.2f}, semakin optimal total biaya persediaan.")
