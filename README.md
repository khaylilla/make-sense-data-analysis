# Analisis Performa Akademik Siswa

## Latar Belakang
Dataset Students Performance in Exams merupakan data yang umum digunakan untuk mempelajari hubungan antara faktor demografis, dukungan pendidikan, dan keberhasilan akademik siswa. Data ini mencakup nilai matematika, membaca, dan menulis, serta karakteristik seperti jenis kelamin, etnis, tingkat pendidikan orang tua, jenis makan siang, dan status persiapan ujian.

## Tujuan
Tujuan dari proyek ini adalah:
- memahami struktur dan kualitas dataset,
- membersihkan dan memproses data dengan benar,
- membandingkan rata-rata nilai berdasarkan kategori tertentu,
- menganalisis hubungan antarskor ujian,
- menyajikan hasil dalam bentuk tabel dan visualisasi,
- menuliskan insight yang didasarkan pada angka yang muncul dari program.

## Dataset
Dataset yang digunakan adalah `StudentsPerformance.csv`.

Kolom utama yang dipakai dalam analisis:
- `gender`
- `race/ethnicity`
- `parental level of education`
- `lunch`
- `test preparation course`
- `math score`
- `reading score`
- `writing score`

## Metode
Proyek ini menggunakan pendekatan analisis data sederhana dengan:
1. membaca data CSV,
2. memeriksa data kosong dan duplikasi,
3. memastikan kolom dan tipe data sesuai,
4. menambahkan kolom `average_score`,
5. menghitung rata-rata berdasarkan kategori,
6. membuat visualisasi dengan Matplotlib dan Seaborn,
7. menulis ringkasan insight ke file `output/insight.txt`.

## Struktur Proyek
```text
make-sense-data-analysis/
├── StudentsPerformance.csv
├── analysis.py
├── requirements.txt
├── README.md
└── output/
    ├── preparation_course.png
    ├── parental_education.png
    ├── score_correlation.png
    ├── summary.csv
    └── insight.txt
```

## Instalasi
Pastikan Python sudah terinstal di komputer.

Buka terminal di folder project lalu jalankan:

```bash
pip install -r requirements.txt
```

## Cara Menjalankan Program
Pada terminal, jalankan perintah berikut:

```bash
python analysis.py
```

Program ini akan:
- memeriksa dataset yang tersedia,
- membersihkan data jika ada masalah,
- membuat kolom `average_score`,
- menghasilkan grafik di folder `output/`,
- menyimpan tabel summary dan insight ke folder `output/`.

## Hasil Analisis
Hasil analisis mencakup:
- rata-rata nilai berdasarkan `test preparation course`,
- rata-rata nilai berdasarkan `parental level of education`,
- korelasi antara skor matematika, membaca, dan menulis,
- interpretasi yang hati-hati dan tidak menganggap hubungan sebab-akibat.

## Catatan Penting
- Dataset asli tidak diubah.
- File output dibuat otomatis jika belum ada.
- Program memiliki penanganan error jika file CSV tidak ditemukan atau kolom yang diperlukan tidak tersedia.
- Semua kesimpulan didasarkan pada data yang benar-benar dihasilkan oleh program.
