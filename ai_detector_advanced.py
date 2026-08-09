import argparse
import warnings
import piexif
from PIL import Image
from transformers import pipeline

# Abaikan warnings huggingface/torch agar console bersih
warnings.filterwarnings("ignore")

# Definisi konstanta generator AI umum untuk pencarian Metadata
KNOWN_AI_SOFTWARE_TAGS = ['midjourney', 'dall-e', 'stable diffusion', 'novelai', 'comfyui', 'fooocus', 'automatic1111']

# Definisi Arsitektur Ensemble (VERSI OP / OVERPOWERED)
MODELS = [
    {
        "name": "Model 1 (SigLIP Deepfake SOTA)",
        "id": "Ateeqq/ai-vs-human-image-detector",
        "weight": 0.60 # Arsitektur SigLIP yang sangat tangguh terhadap manipulasi nyata vs sintetis
    },
    {
        "name": "Model 2 (SMOGY Advanced)",
        "id": "Smogy/SMOGY-Ai-images-detector",
        "weight": 0.40 # Model SOTA terbaru untuk generator modern (Midjourney v6, DALL-E 3, Flux)
    }
]

# // Fungsi untuk mengecek metadata EXIF dan tanda tangan AI pada gambar
def check_metadata(image_path):
    print("[*] Tahap 1: Analisis Metadata (EXIF/Tanda Tangan AI)...")
    try:
        exif_dict = piexif.load(image_path)
        software = ""
        
        # Mengecek TAG 'Software' pada metadata EXIF
        if piexif.ImageIFD.Software in exif_dict["0th"]:
            software = exif_dict["0th"][piexif.ImageIFD.Software].decode("utf-8", errors="ignore").lower()
            print(f"    [!] Ditemukan metadata Software: {software}")
            
        for tag in KNOWN_AI_SOFTWARE_TAGS:
            if tag in software:
                return True, f"Terdeteksi jejak software AI ({tag}) pada atribut Software EXIF."
                
        # Mengecek TAG 'UserComment' pada metadata EXIF (sering dipakai Stable Diffusion)
        if piexif.ExifIFD.UserComment in exif_dict["Exif"]:
            comment = exif_dict["Exif"][piexif.ExifIFD.UserComment].decode("utf-8", errors="ignore").lower()
            if comment:
                print(f"    [!] Ditemukan metadata UserComment panjang (umumnya Prompt AI)")
                for tag in KNOWN_AI_SOFTWARE_TAGS + ['steps:', 'sampler:', 'cfg scale:']:
                    if tag in comment:
                        return True, f"Terdeteksi parameter AI Generator pada UserComment EXIF."
    except Exception as e:
        print("    [-] Gambar tidak memiliki EXIF (atau format seperti PNG/WebP tidak didukung EXIF standar). Lanjut ke Deep Learning.")
        return False, ""
        
    print("    [+] Metadata EXIF bersih. Melanjutkan ke lapisan Deep Learning.")
    return False, ""

# // Fungsi untuk memuat model-model AI (Ensemble) yang dibutuhkan
def load_models():
    print("\n[*] Tahap 2: Memuat Ensemble Model AI")
    print("    (Peringatan: Membutuhkan RAM cukup besar. Loading mungkin agak lama...)")
    pipelines = []
    for m in MODELS:
        print(f"    -> Mengunduh/Memuat {m['name']} ({m['id']})...")
        try:
            pipe = pipeline("image-classification", model=m["id"])
            pipelines.append({"pipe": pipe, "weight": m["weight"], "name": m["name"]})
        except Exception as e:
            print(f"    [!] Gagal memuat {m['name']}: {e}")
            
    return pipelines

# // Fungsi untuk menjalankan proses deteksi menggunakan model ensemble
def run_ensemble(image_path, pipelines):
    print("\n[*] Tahap 3: Menjalankan Analisis Visi Komputer & Pembobotan (Voting)...")
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"[!] Error saat membaca gambar: {e}")
        return

    total_fake_prob = 0.0
    total_real_prob = 0.0
    active_weight = 0.0
    
    for p in pipelines:
        print(f"    -> Menganalisis dengan {p['name']}...")
        try:
            results = p["pipe"](image)
            prob_fake = 0.0
            prob_real = 0.0
            
            # Memetakan label output ke Fake/Real, karena setiap model punya nama label beda
            for res in results:
                label = res['label'].lower()
                if 'fake' in label or 'ai' in label or 'synthetic' in label:
                    prob_fake = res['score']
                elif 'real' in label or 'human' in label or 'natural' in label:
                    prob_real = res['score']
                    
            # Jika model hanya mengeluarkan satu kelas probabilitas
            if prob_fake == 0.0 and prob_real > 0.0:
                prob_fake = 1.0 - prob_real
            elif prob_real == 0.0 and prob_fake > 0.0:
                prob_real = 1.0 - prob_fake

            print(f"       [Hasil] FAKE: {prob_fake*100:.2f}%, REAL: {prob_real*100:.2f}%")
            
            total_fake_prob += prob_fake * p["weight"]
            total_real_prob += prob_real * p["weight"]
            active_weight += p["weight"]
        except Exception as e:
            print(f"    [!] Error pada analisis {p['name']}: {e}")

    if active_weight == 0:
         print("[!] Semua model gagal melakukan analisis.")
         return
         
    # Normalisasi probabilitas berdasarkan bobot model yang berhasil dijalankan
    final_fake = (total_fake_prob / active_weight) * 100
    final_real = (total_real_prob / active_weight) * 100
    
    print("\n" + "="*60)
    print("      KESIMPULAN AKHIR (MULTILAYER ENSEMBLE DETECTION)      ")
    print("="*60)
    print(f"  [>] Probabilitas Gambar Buatan AI (FAKE) : {final_fake:.2f}%")
    print(f"  [>] Probabilitas Gambar Asli/Nyata (REAL): {final_real:.2f}%")
    
    print("\n  VONIS:")
    if final_fake > 85.0:
        print("  >> SANGAT MUNGKIN HASIL GENERATE AI (Sintetis) <<")
    elif final_fake > 60.0:
        print("  >> CENDERUNG HASIL GENERATE AI (Kemungkinan ada editan AI) <<")
    elif final_real > 85.0:
        print("  >> SANGAT MUNGKIN GAMBAR ASLI KUALITAS TINGGI <<")
    else:
        print("  >> CENDERUNG GAMBAR ASLI (Namun skor tidak begitu meyakinkan) <<")
    print("="*60)

# // Fungsi utama untuk menjalankan program analisis gambar
def main():
    parser = argparse.ArgumentParser(description="Pendeteksi Gambar AI Lanjutan (Ensemble 3 Model + EXIF)")
    parser.add_argument("image_path", help="Path ke gambar yang ingin dianalisis secara mendalam")
    args = parser.parse_args()
    
    print("="*60)
    print(f"--- MEMULAI ANALISIS ADVANCED UNTUK: {args.image_path} ---")
    print("="*60)
    
    # Layer 1: Metadata Check
    is_fake_meta, reason = check_metadata(args.image_path)
    if is_fake_meta:
        print("\n" + "="*60)
        print("                KESIMPULAN AKHIR (METADATA)                 ")
        print("="*60)
        print(f"  [!] {reason}")
        print("\n  VONIS: \n  >> 100% HASIL GENERATE AI (Terbukti dari Metadata) <<")
        print("="*60)
        return
        
    # Layer 2 & 3: Deep Learning Ensemble Check
    pipelines = load_models()
    if not pipelines:
        print("[!] Tidak ada model yang berhasil dimuat. Pastikan koneksi internet stabil.")
        return
        
    run_ensemble(args.image_path, pipelines)

if __name__ == "__main__":
    main()
