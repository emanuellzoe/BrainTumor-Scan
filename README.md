🧠 Brain-Scan

Brain-Scan adalah proyek berbasis Machine Learning + Web UI (Next.js) yang bertujuan untuk
menganalisis citra brain scan dan menampilkan hasil klasifikasinya secara visual dan interaktif.

Proyek ini dapat digunakan sebagai fondasi sistem:

✔️ pendeteksi kondisi otak,
✔️ dashboard analisis neuro-data,
✔️ demonstrasi AI untuk kesehatan,
✔️ eksperimen riset computer vision & neuroscience.

📌 Fitur Utama

✨ Upload brain scan / image input
Pengguna dapat memasukkan data scan otak untuk dianalisis.

🤖 Model AI / Machine Learning Classification
Backend melakukan klasifikasi kondisi otak berdasarkan data input.

📊 Visualisasi UI
Frontend menampilkan hasil analisis dalam desain warna oranye yang intuitif dan modern.

🔗 Integrasi API
Frontend terhubung ke backend ML multi-service untuk inferensi dan pengiriman hasil analisis.

🏗️ Arsitektur Sistem
+--------------+       +-------------+       +----------------+
|  Frontend UI |  -->  |  API Layer  |  -->  |  ML Classifier |
|   Next.js    |       |  REST API   |       |   Python/AI    |
+--------------+       +-------------+       +----------------+
       |
       v
+---------------+
|  Visualization |
|  Result Panel  |
+---------------+

🛠️ Teknologi yang Digunakan
🔹 Frontend

Next.js

React

TailwindCSS (tema oranye UI)

🔹 Backend / Machine Learning

Python

TensorFlow / PyTorch (contoh model ML)

OpenCV (preprocessing gambar)

NumPy / Pandas (data handling)

🔹 DevTools / Infrastruktur

GitHub

REST API

Model inference runner

Catatan: Tools dapat berbeda sesuai implementasi di repositori kamu — README ini dapat disesuaikan jika struktur final berbeda.

📂 Struktur Folder (Direkomendasikan)
/brain-scan
 ├─ frontend/          # Next.js UI
 ├─ backend/           # Python ML model + API service
 ├─ dataset/           # Sample brain scan images (optional)
 ├─ docs/              # Documentation / presentation
 └─ README.md

🚀 Cara Instalasi & Menjalankan
1️⃣ Clone repository
git clone https://github.com/emanuellzoe/brain-scan.git
cd brain-scan

2️⃣ Menjalankan Backend (Python)
cd backend
pip install -r requirements.txt
python app.py


Backend akan berjalan pada:

http://localhost:5000

3️⃣ Menjalankan Frontend (Next.js)
cd frontend
npm install
npm run dev


UI dapat diakses melalui:

http://localhost:3000

📌 Cara Menggunakan

Jalankan backend inference model.

Buka UI (Next.js).

Upload gambar scan otak atau pilih sampel.

Sistem akan memproses gambar dan menampilkan output klasifikasi serta confidence.

🧩 Output Sistem

UI akan menampilkan:

✔ Status klasifikasi (misalnya: Normal, Tumor, Abnormal Activity)
✔ Confidence level model
✔ Highlighting visual / warna tematik

Tema tampilan menggunakan sentuhan warna oranye untuk menjaga UI lebih informatif dan menarik.

📌 Pengembangan Selanjutnya

Integrasi 3D MRI viewer

Explainable AI panel (XAI heatmap)

Dashboard monitoring (historical scan & patient management)

🤝 Kontribusi

Pull request sangat diterima!
Silakan buat issue atau diskusi untuk fitur baru.

🛡️ License

📄 MIT License — bebas digunakan untuk riset, akademik, atau pengembangan lanjutan.

Jika ingin kolaborasi, silakan kontak melalui GitHub repo ini.

✨ Terima kasih telah menggunakan Brain-Scan!
