import streamlit as st
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image
from io import BytesIO
from openpyxl import Workbook

# Konfigurasi halaman
st.set_page_config(page_title="EOQ – Economic Order Quantity", layout="centered")

# Judul Aplikasi
st.title("📦 EOQ – Economic Order Quantity")

# Penjelasan EOQ
st.markdown("""
**Economic Order Quantity (EOQ)** adalah jumlah pembelian optimal yang meminimalkan total biaya persediaan, yaitu **biaya pemesanan** dan **biaya penyimpanan**.
""")

# Gambar rumus EOQ (tajam, tidak blur)
st.subheader("📐 Rumus EOQ")
st.image(
    "https://latex.codecogs.com/png.image?\\dpi{300}&space;EOQ%20=%20\\sqrt{\\frac{2DS}{H}}",
    caption="Rumus EOQ: Economic Order Quantity",
    width=280  # Ukuran tetap agar tidak blur
)

st.markdown("""
Keterangan:
- **D**: Permintaan tahunan (unit per tahun)  
- **S**: Biaya pemesanan per order (Rp)  
- **H**: Biaya penyimpanan per unit per tahun (Rp)

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

    # Buat range Q dan hitung biaya
    Q = np.linspace(1, 2 * EOQ, 500)
    biaya_pemesanan = (D / Q) * S
    biaya_penyimpanan = (Q / 2) * H
    total_cost = biaya_pemesanan + biaya_penyimpanan

    # Tampilkan grafik
    plt.figure(figsize=(8, 5))
    plt.plot(Q, total_cost, label='Total Biaya (Rp)', color='blue')
    plt.axvline(EOQ, color='red', linestyle='--', label=f'EOQ = {EOQ:.2f}')
    plt.xlabel("Kuantitas Order (Q)")
    plt.ylabel("Total Biaya (Rp)")
    plt.title("📊 Total Biaya vs Kuantitas Order")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt.gcf())

    # Buat DataFrame untuk ekspor
    df = pd.DataFrame({
        'Order Quantity (Q)': Q,
        'Total Cost (Rp)': total_cost,
        'Biaya Pemesanan (Rp)': biaya_pemesanan,
        'Biaya Penyimpanan (Rp)': biaya_penyimpanan
    })

    # Export ke Excel .xlsx
    output = BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Hasil EOQ"

    # Header
    ws.append(list(df.columns))

    # Data rows
    for row in df.itertuples(index=False):
        ws.append(row)

    # Simpan ke file in-memory
    wb.save(output)
    output.seek(0)

    # Tombol download Excel
    st.download_button(
        label="⬇️ Download Hasil dalam Excel (.xlsx)",
        data=output,
        file_name='hasil_perhitungan_eoq.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.info(f"Semakin dekat kuantitas ke {EOQ:.2f}, semakin optimal total biaya persediaan.")
