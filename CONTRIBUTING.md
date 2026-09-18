# 🤝 Panduan Kontribusi (Contributing Guide)

Halo! Terima kasih sudah tertarik untuk berkontribusi ke **AI Image Detector**! 🎉 Proyek open-source ini dibangun untuk membantu siapa saja membedakan gambar asli dan gambar sintetis buatan AI secara cepat dan akurat. 

Kontribusi dari komunitas—baik berupa perbaikan bug, penambahan model baru, pengujian, atau dokumentasi—sangat kami apresiasi!

---

## 📋 1. Prasyarat (Prerequisites)

Sebelum mulai mengutak-atik kode, pastikan lingkungan lokal Anda memenuhi persyaratan berikut:

- **Python 3.8+** terinstal di sistem Anda.
- Virtual environment (direkomendasikan):
  ```bash
  python -m venv venv
  # Linux/macOS:
  source venv/bin/activate
  # Windows:
  venv\Scripts\activate
  ```
- Instal seluruh dependencies yang dibutuhkan:
  ```bash
  pip install -r requirements.txt
  ```

> 💡 **Tips Hardware:** Karena model Deep Learning HuggingFace memerlukan resource komputasi dan memori (RAM/VRAM), pastikan Anda memiliki koneksi internet yang stabil saat pertama kali mendownload model (~1-2 GB).

---

## 🔄 2. Alur Kontribusi (Contribution Workflow)

Ikuti langkah-langkah standar berikut untuk mulai berkontribusi:

1. **Fork Repositori**  
   Klik tombol **Fork** di pojok kanan atas halaman repositori ini di GitHub.

2. **Clone ke Lokal**  
   ```bash
   git clone https://github.com/<username-kamu>/ai-image-detector.git
   cd ai-image-detector
   ```

3. **Buat Branch Baru**  
   Gunakan nama branch yang deskriptif:
   ```bash
   git checkout -b feat/tambah-model-baru
   # atau
   git checkout -b fix/penanganan-error-png
   ```

4. **Commit Perubahan**  
   Tulis commit message yang jelas dan informatif. Kami sangat menyarankan mengikuti format [Conventional Commits](https://www.conventionalcommits.org/):
   - `feat: ...` untuk fitur baru (contoh: `feat: add support for PNG metadata parsing`)
   - `fix: ...` untuk perbaikan bug (contoh: `fix: handle corrupted EXIF data gracefully`)
   - `docs: ...` untuk perubahan dokumentasi (contoh: `docs: update troubleshooting guide in README`)
   - `refactor: ...` untuk restrukturisasi kode tanpa mengubah fungsionalitas
   - `test: ...` untuk penambahan atau perbaikan unit test
   - `chore: ...` untuk update dependency, konfigurasi git, dll.

5. **Push ke Fork Kamu**  
   ```bash
   git push origin feat/tambah-model-baru
   ```

6. **Buka Pull Request (PR)**  
   Buka GitHub repo Anda, lalu klik **Compare & pull request**. Jelaskan apa yang diubah, motivasi perubahannya, serta cara mengujinya.

---

## 🧪 3. Pengujian Manual Sebelum Commit

Saat ini repositori masih mengandalkan pengujian manual. Sebelum melakukan commit dan submit PR, pastikan skrip berjalan tanpa error dengan gambar uji yang ada di folder `test_images/` (atau gambar lokal Anda):

```bash
# Uji versi standar
python ai_detector.py "test_images/real_cat.jpg"
python ai_detector.py "test_images/ai_cute_dragon.jpg"

# Atau dengan contoh umum:
python ai_detector.py "test_images/contoh.jpg"

# Uji versi advanced (ensemble + EXIF)
python ai_detector_advanced.py "test_images/real_cat.jpg"
python ai_detector_advanced.py "test_images/ai_cute_dragon.jpg"

# Atau dengan contoh umum:
python ai_detector_advanced.py "test_images/contoh.jpg"
```

Pastikan:
- Script tidak crash ketika menerima format gambar berbeda (`.jpg`, `.jpeg`, `.png`, `.webp`).
- Output prediksi, probabilitas, dan ringkasan vonis tampil dengan rapi di terminal.

---

## 🐛 4. Lapor Bug & Request Fitur (GitHub Issues)

Jika menemukan kendala atau punya ide fitur baru, silakan buat issue baru di tab **Issues**.

### Melaporkan Bug (Bug Report)
Harap sertakan informasi selengkap mungkin:
- **Deskripsi:** Penjelasan singkat mengenai masalah yang terjadi.
- **Langkah Reproduksi (Steps to Reproduce):** Perintah atau alur yang dijalankan hingga error muncul.
- **Error Log / Traceback:** Salin pesan error lengkap yang muncul di terminal.
- **Informasi Lingkungan:**
  - Versi Python (`python --version`)
  - Sistem Operasi (Windows / Linux / macOS & versinya)
  - Versi library utama (Torch, Transformers, Pillow)
- **Sampel Gambar (Opsional):** Lampirkan gambar yang memicu error jika memungkinkan.

### Request Fitur (Feature Request)
- Jelaskan masalah atau kebutuhan yang ingin diselesaikan.
- Berikan usulan solusi atau alur implementasi yang diharapkan.

---

## 🎯 5. Area yang Terbuka untuk Kontribusi

Proyek ini masih berkembang dan sangat terbuka untuk kolaborasi di area-area berikut:

1. **Model Deteksi Baru (Ensemble Layer):**
   - Menambahkan model SOTA HuggingFace baru ke dalam list ensemble di `ai_detector_advanced.py`.
   - Kalibrasi bobot (*weight tuning*) pada sistem voting agar akurasi semakin seimbang.
2. **Metadata & Format Gambar Baru:**
   - Menambah parser metadata non-EXIF (misalnya parsing teks *parameters* pada format PNG/WebP chunk dari Stable Diffusion, ComfyUI, atau Fooocus).
   - Dukungan format gambar tambahan (HEIC, TIFF, BMP).
3. **Unit Test & Test Suite:**
   - Menulis unit tests (menggunakan `pytest` atau `unittest`) untuk modularisasi fungsi, parsing metadata, dan validasi input.
   - Setup GitHub Actions / CI workflow dasar.
4. **Optimasi Performa & Resource:**
   - Implementasi lazy-loading model, caching hasil analisis, atau optimasi pemakaian VRAM/RAM (opsi CPU vs CUDA, batch processing).
5. **CLI & Fitur Ekstra:**
   - Dukungan scan batch untuk satu folder sekaligus.
   - Opsi export output hasil deteksi ke format JSON atau CSV.
   - Refaktor kode agar fungsi inti bisa diimpor sebagai package/modul Python.

---

## 📐 6. Standar Kode & Etika Git

Agar kode tetap bersih dan mudah dipelihara:

- **Gaya Kode:** Ikuti pedoman umum **PEP 8** (penamaan variabel snake_case, indentasi 4 spasi, dan komentar yang mudah dipahami).
- **Konsistensi:** Sesuaikan gaya kode dan penanganan error dengan kode yang sudah ada.
- **Kebersihan Repositori:**
  - **JANGAN** pernah commit cache Python (`__pycache__/`, `*.pyc`).
  - **JANGAN** commit file model besar (weights seperti `.bin`, `.safetensors`, `.pt`, `.onnx`). Model harus selalu di-load dari HuggingFace Hub secara dinamis.
  - Jangan commit file environment virtual (`venv/`, `.env`) atau file arsip hasil download pribadi.

---

## ✅ 7. PR Checklist

Sebelum klik **Submit Pull Request**, pastikan Anda mencentang daftar periksa berikut:

- [ ] Sudah melakukan branch dari branch utama (`main`) terbaru.
- [ ] Kode sudah diuji secara manual menggunakan skrip `ai_detector.py` dan/atau `ai_detector_advanced.py`.
- [ ] Kode mengikuti konvensi PEP 8 dan bebas dari sintaks error.
- [ ] Tidak ada file `__pycache__`, file model besar, atau file temporer yang tidak sengaja ter-commit.
- [ ] Pesan commit jelas dan deskriptif (disarankan Conventional Commits).
- [ ] Dokumentasi (seperti `README.md`) telah diperbarui jika ada parameter CLI baru atau perubahan alur penggunaan.
- [ ] Deskripsi PR menjelaskan perubahan yang dibuat dan alasan di baliknya.

---

Terima kasih atas kontribusi Anda dalam membuat deteksi gambar AI semakin akurat dan bermanfaat bagi banyak orang! 🚀
