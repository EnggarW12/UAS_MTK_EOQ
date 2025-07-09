import streamlit as st
import numpy as np
from math import sqrt
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl.chart import LineChart, Reference

# Konfigurasi halaman
st.set_page_config(page_title="EOQ – Debug Mode", layout="centered")

# Judul
st.title("🛠️ EOQ Debug Tool")

st.markdown("Masukkan nilai-nilai yang masuk akal (contoh: D=8000, S=20000, H=4000)")

# Input
D = st.number_input("Permintaan Tahunan (D)", min_value=1, value=8000)
S = st.number_input("Biaya Pemesanan per Order (S)", min_value=1, value=20000)
H = st.number_input("Biaya Penyimpanan per Unit per Tahun (H)", min_value=1, value=4000)

# Validasi angka agar tidak salah input titik/koma
if D > 1e6 or S > 1e6 or H > 1e6:
    st.warning("⚠️ Nilai input terlalu besar. Periksa apakah kamu salah tulis ribuan (misal 8000 bukan 8.000.000).")

# Tombol hitung
if st.button("🔍 Hitung EOQ"):
    EOQ = sqrt((2 * D * S) / H)
    st.success(f"✅ EOQ yang dihitung: {EOQ:.2f} unit")

    # Simulasi Q
    Q = np.linspace(1, 2 * EOQ, 500)
    biaya_pemesanan = (D / Q) * S
    biaya_penyimpanan = (Q / 2) * H
    total_cost = biaya_pemesanan + biaya_penyimpanan

    # Cek nilai minimum
    min_index = np.argmin(total_cost)
    optimal_Q = Q[min_index]
    optimal_cost = total_cost[min_index]
    st.info(f"💡 EOQ optimal berdasarkan simulasi: {optimal_Q:.2f} unit")
    st.info(f"💰 Total biaya minimum: Rp {optimal_cost:,.0f}")

    # Tabel
    df = pd.DataFrame({
        'Order Quantity (Q)': Q,
        'Total Cost (Rp)': total_cost,
        'Biaya Pemesanan (Rp)': biaya_pemesanan,
        'Biaya Penyimpanan (Rp)': biaya_penyimpanan
    })

    st.dataframe(df.head(10))  # tampilkan 10 data awal untuk cek logika

    # Grafik
    fig, ax = plt.subplots()
    ax.plot(Q, total_cost, label='Total Biaya')
    ax.axvline(optimal_Q, color='red', linestyle='--', label=f'EOQ Optimal = {optimal_Q:.2f}')
    ax.set_xlabel("Order Quantity (Q)")
    ax.set_ylabel("Total Cost (Rp)")
    ax.set_title("Grafik Total Biaya vs Order Quantity")
    ax.legend()
    st.pyplot(fig)

    # Export ke CSV
    csv = df.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button("⬇️ Download CSV", data=csv, file_name="hasil_eoq_debug.csv", mime="text/csv")
