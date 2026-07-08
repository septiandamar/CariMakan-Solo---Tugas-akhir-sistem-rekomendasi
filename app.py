from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# --- 1. MEMUAT DAN PERSIAPAN DATA ---
df = pd.read_csv('data_kuliner_bersih_rating.csv')

# Pastikan kolom ulasan dibaca sebagai angka agar filter berfungsi
df['reviewsCount'] = pd.to_numeric(df['reviewsCount'], errors='coerce').fillna(0)

# --- 2. VEKTORISASI TF-IDF ---
tf = TfidfVectorizer()
tfidf_matrix = tf.fit_transform(df['deskripsi_gabungan'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

# --- 3. RUTE HALAMAN UTAMA ---
@app.route('/')
def home():
    return render_template('index.html')

# --- 4. RUTE PEMROSESAN REKOMENDASI ---
@app.route('/rekomendasi', methods=['POST'])
def rekomendasi():
    # Ambil input pencarian dan filter harga dari form HTML
    kata_kunci = request.form['nama_tempat'].strip().lower()
    harga_dipilih = request.form.get('harga', 'Semua')
    
    # -- LAPIS 1: Cek apakah input adalah bagian dari NAMA TEMPAT --
    kandidat_judul = df[df['title'].str.lower().str.contains(kata_kunci, na=False, regex=False)]
    
    if not kandidat_judul.empty:
        # Jika ketemu nama tempatnya
        idx = kandidat_judul.index[0]
        nama_ditemukan = df.iloc[idx]['title']
        
        sim_scores = list(enumerate(cosine_sim[idx]))
        # Ambil 50 teratas sebagai stok sebelum difilter
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:51]
        hasil_indices = [i[0] for i in sim_scores]
        judul_tampilan = f"Tempat Serupa dengan: {nama_ditemukan}"
        
    else:
        # -- LAPIS 2: Jadikan input sebagai KATA KUNCI (Kategori/Deskripsi) --
        query_vec = tf.transform([kata_kunci])
        sim_scores_query = cosine_similarity(query_vec, tfidf_matrix).flatten()
        
        if sim_scores_query.max() == 0:
            return render_template('index.html', error=f"Maaf, tidak ditemukan kuliner dengan kata '{kata_kunci}'.")
        
        # Ambil 50 teratas yang cocok dengan kata kunci
        hasil_indices = sim_scores_query.argsort()[::-1][:50]
        judul_tampilan = f"Hasil Pencarian Kategori: '{kata_kunci.title()}'"
    
    # Buat tabel sementara dari 50 kandidat tersebut
    kandidat_df = df.iloc[hasil_indices].copy()
    
    # -- FITUR FILTER HARGA --
    if harga_dipilih != 'Semua':
        # Saring tempat yang harganya mengandung simbol/teks yang dipilih
        kandidat_df = kandidat_df[kandidat_df['price'].str.contains(harga_dipilih, case=False, na=False, regex=False)]
        
        if kandidat_df.empty:
            return render_template('index.html', error=f"Rekomendasi '{kata_kunci}' dengan rentang harga {harga_dipilih} tidak ditemukan.")
    
    # -- FITUR HYBRID (FILTER ULASAN & URUTKAN RATING) --
    # Hanya rekomendasikan tempat yang sudah direview minimal 5 kali
    kandidat_df = kandidat_df[kandidat_df['reviewsCount'] > 5]
    
    if kandidat_df.empty:
        return render_template('index.html', error=f"Ada tempat untuk '{kata_kunci}', namun ulasannya masih terlalu sedikit/belum terpercaya.")
        
    # Urutkan berdasarkan Rating Tertinggi dan ambil 5 teratas
    kandidat_df = kandidat_df.sort_values(by='totalScore', ascending=False)
    hasil_akhir = kandidat_df.head(5)
    
    # Ubah data menjadi format list dictionary agar mudah dikirim ke HTML
    rekomendasi_list = hasil_akhir.to_dict('records')
    
    return render_template('index.html', nama_tempat=judul_tampilan, rekomendasi=rekomendasi_list)

if __name__ == '__main__':
    app.run(debug=True)