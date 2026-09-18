# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan - Jaya Jaya Institut

## Business Understanding
Jaya Jaya Institut merupakan salah satu institusi pendidikan perguruan tinggi yang telah berdiri sejak tahun 2000 dan telah mencetak banyak lulusan berprestasi. Meski demikian, institusi saat ini menghadapi tantangan serius terkait tingginya rasio mahasiswa yang tidak menyelesaikan studi atau putus kuliah (*dropout*). Tingginya angka *dropout* ini berpotensi merusak reputasi institusi, menurunkan pendapatan operasional, serta menghambat efisiensi perencanaan akademik kampus. Untuk menyelesaikan masalah ini, Jaya Jaya Institut membutuhkan sistem berbasis data dan *machine learning* yang dapat mendeteksi mahasiswa berisiko *dropout* sedini mungkin (*early warning system*) agar pihak kampus dan dosen wali dapat memberikan bimbingan khusus serta intervensi yang tepat waktu.

### Permasalahan Bisnis
1. Tingginya angka *dropout* mahasiswa yang mengancam reputasi akademik dan stabilitas finansial institusi pendidikan.
2. Evaluasi akademik masih bersifat reaktif di akhir semester sehingga kampus terlambat melakukan penanganan terhadap mahasiswa yang berisiko.
3. Belum tersedianya instrumen monitoring terpusat untuk memetakan hubungan antara kondisi finansial, profil demografi mahasiswa, dan capaian evaluasi studi akademik.
4. Belum adanya model prediktif yang siap pakai untuk mengestimasi risiko *dropout* secara objektif dan melakukan simulasi intervensi perbaikan.

### Cakupan Proyek
1. Melakukan pembersihan data (*data cleaning*), audit konsistensi data, dan analisis data eksploratif (EDA) terhadap performa dan profil mahasiswa.
2. Membangun model *machine learning* klasifikasi multi-kelas (*Dropout*, *Enrolled*, *Graduate*) menggunakan Random Forest Classifier.
3. Merancang dashboard analitik interaktif berbasis Metabase untuk memonitor KPI retensi, faktor keberhasilan studi, serta analisis demografi (*Gender* & *Marital Status*).
4. Mengembangkan antarmuka web prototype menggunakan Streamlit yang menyediakan fitur prediksi risiko dan simulasi skenario intervensi (*What-If Analysis*).
5. Menyusun kesimpulan analitik serta rekomendasi aksi strategis (*Action Items*) bagi manajemen institusi.

---

## Persiapan

### Sumber Data
Dataset yang digunakan dalam proyek ini adalah *Students' Performance Dataset* yang disediakan oleh Dicoding:
* **Tautan Dataset**: [Students Performance Data (data.csv)](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/students_performance/data.csv)

### Setup Environment
Proyek ini dikembangkan menggunakan Python versi 3.10.

1. Membuat dan mengaktifkan *virtual environment*:
   * **Windows (Command Prompt / PowerShell):**
     ```powershell
     python -m venv env
     .\env\Scripts\activate
     ```
   * **Linux / macOS:**
     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

2. Menginstal seluruh dependensi pustaka:
   ```bash
   pip install -r requirements.txt
   ```

### Struktur Direktori
```text
submission/
├── model/
│   ├── model_random_forest.joblib
│   ├── scaler.joblib
│   └── label_encoder.joblib
├── notebook.ipynb
├── clean_students_performance.csv
├── student_performance.db
├── app.py
├── requirements.txt
├── README.md
├── lxng_vr-dashboard.png
├── lxng_vr-video.mp4
└── metabase.db.mv.db
```

---

## Business Dashboard
Business Dashboard dibangun menggunakan Metabase untuk membantu manajemen kampus Jaya Jaya Institut memonitor performa akademik, administratif, dan karakteristik demografi mahasiswa secara terukur:
- **Kartu Metrik KPI Utama**: Menampilkan ringkasan total mahasiswa (4.424), total mahasiswa berstatus Dropout (1.421), mahasiswa menunggak SPP (528), serta total penerima beasiswa (1.099).
- **Distribusi Status Mahasiswa (Aktual)**: Visualisasi proporsi kelulusan aktual (*Graduate*, *Dropout*, dan *Enrolled*).
- **Analisis Finansial vs Retensi**: Visualisasi korelasi antara kelancaran pembayaran SPP (*Tuition fees up to date*) dan kelulusan mahasiswa.
- **Analisis Capaian Akademik**: Grafik perbandingan rata-rata SKS lulus Semester 2 (*Curricular units approved*) terhadap status retensi mahasiswa.
- **Distribusi Bantuan Finansial**: Komparasi keberhasilan studi antara mahasiswa penerima beasiswa (*Scholarship holder*) dengan non-beasiswa.
- **Distribusi Status Mahasiswa Berdasarkan Gender**: Visualisasi rasio kelulusan dan *dropout* perbandingan antara mahasiswa Laki-laki dan Perempuan (*100% Stacked Bar*).
- **Distribusi Status Mahasiswa Berdasarkan Status Pernikahan (Marital Status)**: Analisis hubungan status perkawinan (*Single*, *Married*, *Divorced*, dll.) terhadap ketahanan studi mahasiswa.

### Informasi Akses Dashboard Metabase:
* **URL Dashboard**: http://localhost:3000
* **Email / Username**: `galangdavaa@gmail.com`
* **Password**: `serend4vitz13`
* **Berkas Basis Data**: Konfigurasi dashboard telah diekspor ke dalam berkas `metabase.db.mv.db` pada direktori proyek.
* **Tangkapan Layar**: Tersedia pada berkas `lxng_vr-dashboard.png`.

### Cara Menjalankan Dashboard Metabase Secara Lokal:

* **Menggunakan Docker:**
  ```bash
  docker run -d -p 3000:3000 -v $(pwd)/metabase.db:/metabase.db -e "MB_DB_FILE=/metabase.db" --name metabase metabase/metabase:v0.46.4
  ```

* **Menggunakan File JAR:**
  ```bash
  set MB_DB_FILE=./metabase.db && java -jar metabase.jar
  ```

---

## Menjalankan Sistem Machine Learning
Sistem prediksi dibangun menggunakan antarmuka web interaktif berbasis Streamlit dengan fitur:
- Formulir input data mahasiswa: Mencakup data demografi, administrasi finansial, serta nilai dan SKS semester 1 dan semester 2.
- Deteksi Tingkat Risiko: Menampilkan label status (*Dropout*, *Enrolled*, *Graduate*) disertai skor probabilitas (*Risk Score Gauge*).
- Fitur *What-If Analysis*: Simulasi intervensi dinamis untuk menguji perubahan risiko *dropout* apabila mahasiswa diberikan bantuan pembayaran SPP atau perbaikan SKS kelulusan semester berikutnya.

### Tautan Prototype (Streamlit Community Cloud):
- **URL Deployment**: [https://jaya-jaya-institut-retention.streamlit.app/](https://jaya-jaya-institut-retention.streamlit.app/)

### Cara Menjalankan Prototipe Secara Lokal:
Jalankan perintah berikut pada terminal:
```bash
streamlit run app.py
```

Aplikasi akan terbuka otomatis di peramban web pada alamat:
`http://localhost:8501`

---

## Conclusion
Berdasarkan hasil eksplorasi data, visualisasi dashboard, dan pemodelan *machine learning* yang telah dilakukan:
1. **Faktor Finansial sebagai Indikator Kritis**: Mahasiswa yang memiliki tunggakan SPP (*Tuition fees not up to date*) memiliki proporsi *dropout* yang sangat tinggi. Sebaliknya, penerima beasiswa menunjukkan persentase kelulusan (*Graduation rate*) yang signifikan lebih tinggi.
2. **Performa Semester Pertama dan Kedua Menentukan**: Jumlah SKS yang berhasil diluluskan pada Semester 1 dan Semester 2 (*Curricular units approved*) merupakan fitur pembeda paling dominan antara mahasiswa yang berhasil lulus dengan yang putus studi.
3. **Pengaruh Karakteristik Demografi**:
   - **Gender**: Mahasiswa laki-laki memiliki kecenderungan rasio *dropout* yang lebih tinggi dibandingkan mahasiswa perempuan.
   - **Status Pernikahan**: Mayoritas mahasiswa berstatus lajang (*Single*) mendominasi populasi dengan rasio kelulusan yang stabil, sementara mahasiswa dengan status telah menikah atau berpisah memiliki tantangan komitmen ganda yang membutuhkan perhatian khusus.
4. **Kinerja Model Machine Learning**: Algoritma Random Forest Classifier berhasil memberikan performa yang sangat optimal setelah memfokuskan pemodelan pada klasifikasi biner (*Graduate* vs *Dropout*) dengan hasil evaluasi pada data uji (*test set*):
   - **Akurasi Model**: 91,87%
   - **Weighted Average F1-Score**: 92% (Macro Avg F1-Score: 91%)
   - **F1-Score per Kelas**: 0,89 untuk kelas *Dropout* dan 0,93 untuk kelas *Graduate*
   - **Fitur Dominan**: Curricular units 2nd sem (approved), Tuition fees up to date, Curricular units 1st sem (approved), dan Admission grade.
*Catatan Pemilihan Model*: Berdasarkan komparasi beberapa algoritma di notebook (Logistic Regression dan Random Forest), Logistic Regression memang menghasilkan skor data uji yang kompetitif. Namun, **Random Forest Classifier dipilih untuk implementasi sistem produksi** karena merupakan model *ensemble* berbasis pohon keputusan yang memiliki generalisasi lebih tangguh (*robust*), mampu menangkap relasi data non-linear secara optimal, serta lebih stabil menghadapi variasi data baru di lingkungan implementasi nyata.

---

## Rekomendasi Action Items
- **Sistem Notifikasi Finansial Fleksibel**: Mengintegrasikan sistem pembayaran kampus dengan peringatan dini; mahasiswa yang menunggak SPP segera diarahkan ke program restrukturisasi cicilan, skema beasiswa darurat, atau program kerja paruh waktu kampus sebelum dikenakan sanksi akademik.
- **Program Pendampingan Akademik Terpadu**: Mewajibkan sesi tutorial/asistensi belajar tambahan khusus mahasiswa yang meluluskan SKS semester pertama di bawah ambang batas minimal (< 50% SKS terdaftar).
- **Intervensi Konseling Berbasis Demografi**: Memberikan ruang konseling dan pendampingan personal bagi mahasiswa yang memiliki peran ganda (sudah menikah/berkeluarga) serta kelompok mahasiswa dengan rasio risiko *dropout* tinggi.
- **Revitalisasi Peran Dosen Pembimbing Akademik (DPA)**: Menggunakan aplikasi *Early Warning System* Streamlit ini sebagai instrumen kerja DPA dalam memantau profil risiko anak bimbingan secara berkala di tiap awal semester.
- **Optimalisasi Kuota Beasiswa Berkelanjutan**: Mengalokasikan proporsi beasiswa retensi berbasis kebutuhan ekonomi bagi mahasiswa aktif berprestasi yang terancam putus studi di pertengahan semester.

