import os
import urllib.request

urls = {
    # Gambar Asli (Real)
    "real_tiger.jpg": "https://huggingface.co/datasets/mishig/sample_images/resolve/main/tiger.jpg",
    "real_airport.jpg": "https://huggingface.co/datasets/mishig/sample_images/resolve/main/airport.jpg",
    "real_cat.jpg": "https://huggingface.co/datasets/mishig/sample_images/resolve/main/cat-2.jpg",
    
    # Gambar Buatan AI (Stable Diffusion dll)
    "ai_generated_art.png": "https://huggingface.co/datasets/mishig/sample_images/resolve/main/sd-v1-4.png",
    "ai_generated_fantasy.png": "https://huggingface.co/datasets/mishig/sample_images/resolve/main/cat-dog-music.png"
}

os.makedirs("test_images", exist_ok=True)

print("======================================")
print("  Mengunduh Gambar Uji Coba (Dataset) ")
print("======================================")

for name, url in urls.items():
    path = os.path.join("test_images", name)
    try:
         # Menambahkan header User-Agent sederhana agar tidak diblokir
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response, open(path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"[+] Berhasil: {name}")
    except Exception as e:
        print(f"[-] Gagal: {name} ({e})")
        
print("======================================")
print("Selesai! Gambar siap dites, cek folder 'test_images'.")
