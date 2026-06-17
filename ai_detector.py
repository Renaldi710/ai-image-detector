import argparse
from transformers import pipeline
from PIL import Image
import warnings

# Mengabaikan warning agar output lebih bersih
warnings.filterwarnings("ignore")

def detect_ai_image(image_path, model_name="dima806/ai_vs_real_image_detection"):
    print(f"[*] Memuat gambar dari: {image_path}")
    try:
        image = Image.open(image_path).convert("RGB")
    except Exception as e:
        print(f"[!] Error saat memuat gambar: {e}")
        return

    print(f"[*] Memuat model pendeteksi AI ({model_name})...")
    print("    (Ini mungkin memakan waktu agak lama pada proses pertama karena harus mengunduh model)")
    try:
        # Inisialisasi pipeline klasifikasi gambar
        detector = pipeline("image-classification", model=model_name)
    except Exception as e:
        print(f"[!] Error saat memuat model: {e}")
        return

    print("[*] Menganalisis gambar...\n")
    try:
        results = detector(image)
    except Exception as e:
        print(f"[!] Error saat menganalisis gambar: {e}")
        return

    print("==============================")
    print("        HASIL ANALISIS        ")
    print("==============================")
    
    # Mengurutkan hasil berdasarkan probabilitas (score) tertinggi
    results.sort(key=lambda x: x['score'], reverse=True)
    
    for result in results:
        label = result['label'].upper()
        score = result['score'] * 100
        print(f"[{label}] Probabilitas: {score:.2f}%")
        
    print("==============================")
    
    # Memberikan kesimpulan singkat
    top_result = results[0]
    if top_result['label'].lower() == 'fake':
        print(f"\n=> Kesimpulan: Gambar ini KEMUNGKINAN BESAR HASIL GENERATE AI ({top_result['score']*100:.2f}%).")
    elif top_result['label'].lower() == 'real':
         print(f"\n=> Kesimpulan: Gambar ini KEMUNGKINAN BESAR ASLI / NYATA ({top_result['score']*100:.2f}%).")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pendeteksi Gambar AI (AI vs Real Image Detector)")
    parser.add_argument("image_path", help="Path ke file gambar yang ingin dianalisis (contoh: gambar.jpg)")
    parser.add_argument("--model", default="dima806/ai_vs_real_image_detection", 
                        help="Model HuggingFace yang akan digunakan (default: dima806/ai_vs_real_image_detection)")
    
    args = parser.parse_args()
    detect_ai_image(args.image_path, args.model)
