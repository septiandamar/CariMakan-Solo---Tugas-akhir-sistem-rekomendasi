# 🗺️ CariMakan Solo
### Web-Based Hybrid Culinary Recommender System

CariMakan Solo adalah aplikasi pencarian pintar berbasis web yang berfungsi sebagai sistem rekomendasi kuliner di wilayah Kota Surakarta (Solo). Sistem ini menggunakan pendekatan *Hybrid Filtering* untuk menyajikan destinasi kuliner yang tidak hanya relevan secara karakteristik, tetapi juga terjamin kualitas reputasinya berdasarkan data riil Google Maps.

---

## 🚀 Fitur Utama

* **Dynamic Two-Layer Query Processing**  
  Mendukung pencarian fleksibel baik berbasis kata kunci kategori umum (misal: "sate", "kopi") maupun nama tempat spesifik.
  
* **Smart Hybrid Engine**  
  Menggabungkan *Content-Based Filtering* (TF-IDF & Cosine Similarity) dengan *Popularity-Based Filtering* (Rating & Jumlah Ulasan).
  
* **Optimized Feature Engineering**  
  Sistem bebas dari bias ambiguitas kategori umum dengan tingkat akurasi mencapai **96%** (Metrik *Precision at 5*).
  
* **Interactive Frontend**  
  Antarmuka bertema *Midnight Blue-Purple* yang responsif (*mobile-friendly*) dan dilengkapi filter anggaran harga.
  
* **Google Maps Integration**  
  Setiap kartu rekomendasi terintegrasi langsung dengan tombol navigasi arah menuju platform Google Maps asli.

---

## 🛠️ Tech Stack

Untuk bagian teknologi, menggunakan tabel seperti ini akan jauh lebih rapi dan "keren" di GitHub:

| Komponen | Teknologi yang Digunakan |
| :--- | :--- |
| **Backend** | Python, Flask Framework |
| **Frontend** | HTML5, CSS3, Jinja2 Template Engine |
| **Data Prep & Processing** | Google Colab, Pandas, Scikit-Learn |
| **Data Source** | Google Maps Data Scraping via Apify |
