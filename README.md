# 🕵️‍♂️ AI Image Detector

Proyek ini berisi kumpulan script Python untuk mendeteksi apakah sebuah gambar merupakan hasil *generate* dari kecerdasan buatan (seperti Midjourney, DALL-E, Stable Diffusion, dll) atau merupakan foto/gambar asli.

Terdapat dua versi script yang bisa Anda gunakan: **Versi Standar** dan **Versi Lanjutan (Advanced)**.

## 🚀 Fitur Utama

1. **ai_detector.py (Versi Standar)**
   - Menggunakan satu model Deep Learning HuggingFace (`dima806/ai_vs_real_image_detection`).
   - Eksekusi cepat dan ramah memori (RAM/VRAM).
   - Sangat cocok untuk pengecekan cepat sehari-hari.

2. **ai_detector_advanced.py (Versi Advanced / Ensemble)**
   - **Multi-layered Detection:** Menggunakan pendekatan berlapis untuk akurasi maksimal.
   - **Layer 1 (Metadata EXIF):** Mengekstraksi informasi EXIF gambar untuk mencari jejak tersembunyi parameter AI (seperti nama *software* atau metadata *prompt* dari Stable Diffusion).
   - **Layer 2 & 3 (Ensemble 3 Model):** Jika metadata bersih, script akan meluncurkan tiga model AI berbeda secara bersamaan:
     1. Model ViT Umum (`dima806/ai_vs_real_image_detection`) - Bobot 40%
     2. Model ViT CIFAKE (`capcheck/ai-image-detection`) - Bobot 35%
     3. Model SigLIP (`Ateeqq/ai-vs-human-image-detector`) - Bobot 25%
   - **Sistem Voting:** Menganalisis probabilitas dari ketiga model dan mengkalkulasi vonis akhir berdasarkan sistem *weighted voting* untuk meminimalkan salah deteksi (False Positive/Negative).

## 🛠️ Instalasi & Persiapan

1. Pastikan Anda sudah menginstal **Python 3.8+** di sistem Anda.
2. Buka terminal di folder proyek ini dan jalankan perintah berikut untuk menginstal seluruh pustaka (*library*) yang dibutuhkan:

```bash
pip install -r requirements.txt
```

Pustaka utama yang digunakan meliputi:
- `transformers`: Ekosistem HuggingFace untuk memuat model *machine learning*.
- `torch`: Mesin utama (*backend*) pengolahan tensor (PyTorch).
- `pillow` (PIL): Untuk manipulasi dan pembacaan file gambar.
- `piexif`: Ekstraksi data EXIF/Metadata secara mendalam.

## 💻 Cara Penggunaan

### Menggunakan Versi Standar:
```bash
python ai_detector.py "path/ke/gambar/anda.jpg"
```
*(Opsional)* Anda juga bisa mengganti model yang digunakan:
```bash
python ai_detector.py "gambar.jpg" --model "Ateeqq/ai-vs-human-image-detector"
```

### Menggunakan Versi Advanced (Sangat Akurat):
```bash
python ai_detector_advanced.py "path/ke/gambar/anda.jpg"
```
> **Catatan Penting:** Saat pertama kali dijalankan, script akan mengunduh model Deep Learning dari server HuggingFace (sekitar 1-2 GB). Pastikan koneksi internet Anda stabil. Pada penggunaan versi Advanced, direkomendasikan memiliki memori (RAM) yang cukup besar.

## 📊 Memahami Hasil (Output)

Setiap probabilitas yang dihasilkan adalah keyakinan sistem bahwa gambar masuk ke dalam kategori tertentu.
- **FAKE (Sintetis/AI):** Gambar dicurigai kuat dibuat atau diedit berat oleh AI.
- **REAL (Asli):** Gambar dicurigai kuat merupakan foto asli tangkapan kamera atau ilustrasi buatan tangan manusia seutuhnya tanpa intervensi AI generatif.

Pada versi **Advanced**, sistem akan menampilkan rangkuman vonis yang sangat jelas dengan skala yang dikategorikan berdasarkan persentase hasil *voting*.

---
*Dibuat untuk analisis gambar tingkat lanjut oleh AI Engineer.*
