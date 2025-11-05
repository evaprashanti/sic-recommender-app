import streamlit as st
import pandas as pd
import joblib
import requests
import gzip
import os

st.title("💡 Sistem Rekomendasi Produk E-Commerce (SIC)")
st.write("Aplikasi ini menampilkan rekomendasi produk mirip berdasarkan kemiripan data pelanggan.")

# 🔹 URL file model dari Google Drive
url = "https://drive.google.com/uc?export=download&id=1VLiZOTkp9GvQzXVyExIP4EK7FUCyXop-"

# 🔹 Unduh model hanya jika belum ada di folder
model_path = "recommender_model_compressed.joblib"
if not os.path.exists(model_path):
    with st.spinner("Mengunduh model dari Google Drive..."):
        r = requests.get(url)
        with open(model_path, "wb") as f:
            f.write(r.content)
        st.success("Model berhasil diunduh!")


# 🔹 Load model rekomendasi (tanpa gzip)
model = joblib.load(model_path)

# 🔹 Ambil daftar produk dari model
product_list = list(model.columns)

# 🔹 Pilihan produk
selected_product = st.selectbox("Pilih Produk:", product_list)

# 🔹 Fungsi rekomendasi
def rekomendasi_produk(nama_produk, similarity_df, n=5):
    if nama_produk not in similarity_df.index:
        st.warning(f"Produk '{nama_produk}' tidak ditemukan.")
        return []
    rekomendasi = similarity_df[nama_produk].sort_values(ascending=False)[1:n+1]
    return rekomendasi

# 🔹 Tombol tampilkan hasil
if st.button("Tampilkan Rekomendasi"):
    hasil = rekomendasi_produk(selected_product, model)
    st.subheader(f"Rekomendasi produk mirip dengan **{selected_product}**:")
    st.table(hasil)

