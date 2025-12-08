# 🧠 BrainTumor-Scan

**Dokumentasi Proyek Analisis Citra Tumor Otak Berbasis Machine Learning**

---

## 📋 Deskripsi Proyek

Brain-Scan adalah aplikasi web berbasis Machine Learning yang dirancang untuk menganalisis citra scan otak dan menampilkan hasil klasifikasinya secara visual dan interaktif. Proyek ini mengintegrasikan teknologi AI dengan antarmuka pengguna modern untuk memberikan solusi analisis neuro-data yang efisien.

**Kegunaan:**
- Pendeteksi kondisi otak (tumor, kelainan, aktivitas abnormal)
- Dashboard analisis data neuro-science
- Demonstrasi AI untuk aplikasi kesehatan
- Platform eksperimen riset computer vision & neuroscience

---

## ✨ Fitur Utama

### 🖼️ Upload Brain Scan
Pengguna dapat mengunggah gambar scan otak (MRI, CT scan) untuk dianalisis oleh sistem

### 🤖 Klasifikasi AI
Model Machine Learning melakukan analisis dan klasifikasi kondisi otak berdasarkan input gambar

### 📊 Visualisasi Interaktif
Antarmuka pengguna modern dengan tema warna oranye yang menampilkan hasil analisis secara intuitif

### 🔗 Integrasi API
Arsitektur client-server yang memisahkan frontend dan backend untuk skalabilitas dan performa optimal

---

## 🛠️ Teknologi yang Digunakan

### Frontend
- **Next.js** - Framework React untuk aplikasi web
- **React** - Library JavaScript untuk membangun UI
- **TailwindCSS** - Framework CSS untuk styling (tema oranye)
- **TypeScript** - Superset JavaScript dengan type safety

### Backend & Machine Learning
- **Python** - Bahasa pemrograman utama untuk ML
- **TensorFlow / PyTorch** - Framework deep learning
- **OpenCV** - Library untuk preprocessing gambar
- **NumPy** - Komputasi numerik
- **Pandas** - Manipulasi dan analisis data
- **Flask / FastAPI** - Framework REST API (kemungkinan)

### Development Tools
- **GitHub** - Version control dan kolaborasi
- **npm** - Package manager untuk JavaScript
- **pip** - Package manager untuk Python

---

## 🏗️ Arsitektur Sistem

```
┌──────────────┐     HTTP Request      ┌─────────────┐     Model Inference    ┌────────────────┐
│  Frontend UI │  ──────────────────>  │  API Layer  │  ─────────────────>   │ ML Classifier  │
│   Next.js    │                       │  REST API   │                        │   Python/AI    │
│  localhost   │  <──────────────────  │  Flask/     │  <─────────────────   │   TensorFlow   │
│   :3000      │     JSON Response     │  FastAPI    │     Classification     │                │
└──────────────┘                       └─────────────┘                        └────────────────┘
                                              │
                                              ▼
                                       ┌─────────────┐
                                       │ Visualization│
                                       │ Result Panel │
                                       └─────────────┘
```

---

## 📂 Struktur Folder

```
brain-scan/
├── ML/                      # Model Machine Learning & training scripts
│   ├── model.py            # Definisi model AI
│   ├── train.py            # Script untuk training model
│   └── requirements.txt    # Dependencies Python
│
├── app/                     # Aplikasi Next.js frontend
│   ├── components/         # Komponen React
│   ├── pages/              # Halaman aplikasi
│   └── styles/             # File CSS/styling
│
├── public/                  # Asset statis (gambar, icon)
│
├── .gitignore              # File yang diabaikan git
├── package.json            # Dependencies Node.js
├── next.config.ts          # Konfigurasi Next.js
├── tsconfig.json           # Konfigurasi TypeScript
└── README.md               # Dokumentasi proyek
```

---

## 🚀 Cara Instalasi & Menjalankan

### Prasyarat
- Node.js (versi 16 atau lebih tinggi)
- Python (versi 3.8 atau lebih tinggi)
- npm atau yarn
- pip (Python package installer)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/emanuellzoe/brain-scan.git
cd brain-scan
```

### 2️⃣ Setup Backend (Python ML Model)

```bash
# Masuk ke folder ML
cd ML

# Install dependencies Python
pip install -r requirements.txt

# Jalankan server backend
python app.py
```

Backend akan berjalan pada **http://localhost:5000**

### 3️⃣ Setup Frontend (Next.js)

Buka terminal baru:

```bash
# Kembali ke root directory (jika masih di folder ML)
cd ..

# Install dependencies Node.js
npm install

# Jalankan development server
npm run dev
```

Frontend akan berjalan pada **http://localhost:3000**

---

## 📖 Cara Menggunakan

### Langkah 1: Jalankan Backend
Pastikan server Python backend sudah berjalan di port 5000

### Langkah 2: Akses Aplikasi Web
Buka browser dan akses **http://localhost:3000**

### Langkah 3: Upload Gambar Scan Otak
- Klik tombol upload atau drag-and-drop gambar scan otak
- Format yang didukung: JPG, PNG, DICOM (tergantung implementasi)

### Langkah 4: Proses Analisis
- Sistem akan mengirim gambar ke backend untuk diproses
- Model AI akan melakukan inferensi dan klasifikasi

### Langkah 5: Lihat Hasil
UI akan menampilkan:
- **Status Klasifikasi** - Kondisi otak terdeteksi (Normal, Tumor, Abnormal)
- **Confidence Score** - Tingkat kepercayaan model (dalam persentase)
- **Visualisasi** - Highlighting area yang terdeteksi (jika tersedia)
- **Rekomendasi** - Saran tindak lanjut berdasarkan hasil analisis

---

## 🎨 Tampilan Antarmuka

Aplikasi menggunakan tema warna **oranye** yang modern dan informatif dengan desain yang:
- Clean dan minimalis
- Responsif untuk berbagai ukuran layar
- Fokus pada pengalaman pengguna
- Visualisasi data yang jelas dan mudah dipahami

---

## 🧪 Contoh Output Sistem

### Hasil Klasifikasi
```
┌─────────────────────────────────┐
│  Hasil Analisis Brain Scan      │
├─────────────────────────────────┤
│  Status: Tumor Terdeteksi        │
│  Confidence: 92.5%               │
│  Lokasi: Lobus Frontal Kanan    │
│  Ukuran: ~2.3 cm                │
└─────────────────────────────────┘
```

---

## 🔧 Pengembangan Lanjutan

### Fitur Masa Depan
- 🎯 **Integrasi 3D MRI Viewer** - Visualisasi scan 3D interaktif
- 🔍 **Explainable AI (XAI)** - Heatmap untuk menjelaskan keputusan model
- 📊 **Dashboard Monitoring** - Tracking historical scan & manajemen pasien
- 🔐 **Sistem Autentikasi** - Login untuk dokter dan admin
- 📱 **Mobile Application** - Versi mobile native
- 🌐 **Multi-language Support** - Mendukung berbagai bahasa

### Peningkatan Model
- Training dengan dataset lebih besar
- Implementasi ensemble learning
- Fine-tuning hyperparameter
- Validasi silang yang lebih robust

---

## 🤝 Kontribusi

Kontribusi dari komunitas sangat diterima! Berikut cara berkontribusi:

1. Fork repository ini
2. Buat branch fitur baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

Untuk bug report atau feature request, silakan buat **Issue** di GitHub.

---

## 📄 Lisensi

Proyek ini dilisensikan di bawah **MIT License** - bebas digunakan untuk:
- Riset akademik
- Pengembangan komersial
- Proyek open source
- Pembelajaran dan eksperimen

---

## ⚠️ Disclaimer

Aplikasi ini dibuat untuk tujuan riset dan edukasi. Hasil analisis **TIDAK dapat** menggantikan diagnosis medis profesional. Selalu konsultasikan dengan dokter atau tenaga medis bersertifikat untuk interpretasi hasil scan otak.

---

## 🙏 Acknowledgments

- Dataset: [Sumber dataset brain scan yang digunakan]
- Model Architecture: Inspirasi dari penelitian terkini dalam medical imaging
- Community: Terima kasih kepada komunitas open source atas library dan framework yang digunakan

---

✨ **Terima kasih telah menggunakan Brain-Scan!**

Jika proyek ini bermanfaat, jangan lupa berikan ⭐ di GitHub!
