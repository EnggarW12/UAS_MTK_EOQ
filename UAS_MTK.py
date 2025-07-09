import streamlit as st
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import pandas as pd
from PIL import Image

# Konfigurasi halaman
st.set_page_config(page_title="EOQ – Economic Order Quantity", layout="centered")

# Judul Aplikasi
st.title("📦 EOQ – Economic Order Quantity")

# Penjelasan EOQ
st.markdown("""
**Economic Order Quantity (EOQ)** adalah jumlah pembelian optimal yang meminimalkan total biaya persediaan, yaitu **biaya pemesanan** dan **biaya penyimpanan**.
""")

# Gambar rumus EOQ
st.subheader("📐 Rumus EOQ")
st.image(
    "https://latex.codecogs.com/png.image?\\dpi{300}&space;EOQ%20=%20\\sqrt{\\frac{2DS}{H}}",
    caption="Rumus EOQ: Economic Order Quantity",
    width=280
)

st.markdown("""
Keterangan:
- **D**: Permintaan tahunan (unit per tahun)  
- **S**: Biaya pemesanan per order (Rp)  
- **H**: Biaya penyimpanan per unit per tahun (Rp)

Masukkan nilai numerik tanpa titik pemisah ribuan. Contoh: `8000`, bukan `8.000`.
""")

# Input pengguna (FIXED: pakai number_input agar tidak salah ribuan)
st.subheader("📝 Input Parameter")
D = st.number_input("Permintaan Tahunan (D)", value=8000, min_value=1)
S = st.number_input("Biaya Pemesanan per Order (S)", value=20000, min_value=1)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", value=4000, min_value=1)

# Tombol hitung EOQ
if st.button("🔍 Hitung EOQ"):
    EOQ = sqrt((2 * D * S) / H)
    st.success(f"EOQ Optimal: {EOQ:.2f} unit")

    # Debug nilai input
    st.write(f"📌 Dibaca oleh sistem: D = {D}, S = {S}, H = {H}")

    # Buat range Q dan hitung biaya
    Q = np.linspace(1, 2 * EOQ, 500)
    biaya_pemesanan = (D / Q) * S
    biaya_penyimpanan = (Q / 2) * H
    total_cost = biaya_pemesanan + biaya_penyimpanan

    # EOQ optimal dari simulasi
    min_index = np.argmin(total_cost)
    best_Q = Q[min_index]
    min_cost = total_cost[min_index]

    st.info(f"💡 EOQ terbaik hasil simulasi: {best_Q:.2f} unit")
    st.info(f"💰 Total biaya minimum: Rp {min_cost:,.0f}")

    # Grafik
    plt.figure(figsize=(8, 5))
    plt.plot(Q, total_cost, label='Total Biaya (Rp)', color='blue')
    plt.axvline(best_Q, color='red', linestyle='--', label=f'EOQ Optimal = {best_Q:.2f}')
    plt.xlabel("Kuantitas Order (Q)")
    plt.ylabel("Total Biaya (Rp)")
    plt.title("📊 Total Biaya vs Kuantitas Order")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    st.pyplot(plt.gcf())

    # Tabel ke DataFrame
    df = pd.DataFrame({
        'Order Quantity (Q)': Q,
        'Total Cost (Rp)': total_cost,
        'Biaya Pemesanan (Rp)': biaya_pemesanan,
        'Biaya Penyimpanan (Rp)': biaya_penyimpanan
    })

    # Export CSV
    csv = df.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button(
        label="⬇️ Download Hasil dalam CSV (Excel Friendly)",
        data=csv,
        file_name='hasil_perhitungan_eoq.csv',
        mime='text/csv'
    )
