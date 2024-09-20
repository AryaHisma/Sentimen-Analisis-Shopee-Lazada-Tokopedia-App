# Sentiment Analysis Marketplace Online: Shopee, Lazada, dan Tokopedia

![images](https://github.com/AryaHisma/Sentimen-Analisis-Shopee-Lazada-Tokopedia-App/blob/main/assets/gambar/screenshoot.png)

Proyek ini berfokus pada **sentiment analysis** dari aplikasi e-commerce populer di Indonesia, yaitu **Shopee**, **Lazada**, dan **Tokopedia**. Dengan menggunakan **network analysis**, kami tidak hanya menilai sentimen secara umum tetapi juga mengeksplorasi hubungan antar kata dalam ulasan pengguna. Melalui analisis jaringan, kita dapat melihat kata-kata yang paling berpengaruh, hubungan yang paling penting, dan konektor terbaik dalam jaringan kata.


## Dataset
Dataset yang digunakan berasal dari **scraping ulasan pengguna** di **Google Play Store**. Dataset ini menampilkan ulasan dari pengguna aplikasi yang sudah melalui proses **preprocessing** (pra-pemrosesan), sehingga teks ulasan sudah siap untuk dianalisis. Beberapa tahapan preprocessing yang diterapkan meliputi:
- **Lower case**: Mengubah semua teks menjadi huruf kecil.
- **Remove emoji**: Menghapus karakter emoji dari teks.
- **Text cleaning**: Membersihkan teks dari karakter yang tidak diinginkan seperti tanda baca yang tidak relevan.
- **Slang transformation**: Mengubah kata-kata tidak baku atau slang ke bentuk baku.
- **Remove stopwords**: Menghapus kata-kata umum yang tidak signifikan seperti "dan", "yang", "di".


### Kolom dalam Dataset
Dataset ini terdiri dari beberapa kolom yang penting untuk analisis, antara lain:
- **content**: Berisi ulasan dari pelanggan yang sudah diproses.
- **at**: Tanggal dan waktu ketika ulasan diberikan oleh pelanggan.
- **year**: Tahun saat ulasan dipublikasikan.


## Exploratory data analysis
Sebelum dilakukan analisis jaringan kata, terlebih dahulu dilakukan **Exploratory Data Analysis (EDA)** yang memberikan gambaran umum tentang distribusi data, pola sentimen, dan karakteristik pengguna berdasarkan tahun atau waktu ulasan. Visualisasi ini membantu memahami dinamika ulasan pengguna secara lebih baik.


## Analisis Jaringan (Network Analysis)
Dalam analisis ini, kami menggunakan pendekatan **network analysis** untuk melihat hubungan antar kata yang sering muncul dalam ulasan pelanggan. Dengan cara ini, kita dapat melihat jaringan kata-kata yang membentuk sentimen positif atau negatif. Selain itu, kita juga menyoroti beberapa karakteristik penting dalam jaringan kata, seperti:
- **Most Influential Words**: Kata-kata yang paling sering muncul dan memengaruhi keseluruhan sentimen.
- **Most Important Connections**: Koneksi antar kata yang paling relevan dan memiliki dampak besar dalam jaringan.
- **Best Connectors**: Kata-kata yang berperan sebagai penghubung penting antar kata atau kelompok kata dalam ulasan.


## Library yang Digunakan
Berikut adalah beberapa library yang digunakan dalam proyek ini:
1. **Streamlit**: Digunakan untuk membangun aplikasi web yang interaktif, memungkinkan pengguna untuk melihat hasil analisis secara langsung.
2. **Pillow**: Untuk manipulasi gambar seperti resizing dan editing pada aplikasi web.
3. **Pandas & Numpy**: Library dasar untuk manipulasi data tabular dan komputasi numerik.
4. **NLTK (Natural Language Toolkit)**: Digunakan untuk pemrosesan teks, seperti tokenisasi, stemming, dan filtering stopwords.
5. **Matplotlib, Plotly, Seaborn & Wordcloud**: Library untuk visualisasi data, termasuk pembuatan grafik interaktif dan statis.
6. **NLP-ID & Sastrawi**: Digunakan khusus untuk pemrosesan teks berbahasa Indonesia, termasuk stemming dan tokenisasi.
7. **NetworkX**: Untuk membuat dan menganalisis grafik jaringan yang menghubungkan kata-kata penting dalam ulasan.

Dengan kombinasi berbagai teknik analisis ini, proyek ini tidak hanya menampilkan hasil sentiment analysis sederhana, tetapi juga menggali lebih dalam pola hubungan antar kata yang mendasari sentimen pengguna terhadap aplikasi e-commerce di Indonesia.

Penjelasan lebih terperinci tentang **preprocessing data** dan **exploratory data analysis** dapat dilihat di bagian masing-masing pada aplikasi.


## Alur preprocessing dan pengolahan data
![images](https://github.com/AryaHisma/Sentimen-Analisis-Shopee-Lazada-Tokopedia-App/blob/main/assets/gambar/alur.jpg)




