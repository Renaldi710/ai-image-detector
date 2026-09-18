import os
import sys
import json
import zipfile
import urllib.request
import shutil

# ponytail: stdlib urllib + zipfile only, extract only target 100 jpgs and discard zip

def get_token() -> str:
    local_cfg = os.path.join(os.path.dirname(__file__), "kaggle.json")
    with open(local_cfg, "r") as f:
        return json.load(f)["token"].strip()

def collect():
    token = get_token()
    dataset_slug = "cashbowman/ai-generated-images-vs-real-images"
    url = f"https://www.kaggle.com/api/v1/datasets/download/{dataset_slug}"

    zip_path = "temp_dataset.zip"
    out_ai_dir = os.path.join("dataset", "ai")
    out_real_dir = os.path.join("dataset", "real")
    os.makedirs(out_ai_dir, exist_ok=True)
    os.makedirs(out_real_dir, exist_ok=True)

    existing_bytes = os.path.getsize(zip_path) if os.path.exists(zip_path) else 0
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    if existing_bytes > 0:
        req.add_header("Range", f"bytes={existing_bytes}-")

    print(f"[*] Mengunduh dataset {dataset_slug} dari Kaggle (posisi: {existing_bytes // (1024*1024)} MB)...")
    try:
        resp = urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        if e.code == 416: # Range not satisfiable, file might be complete
            resp = None
        else:
            raise

    if resp:
        mode = "ab" if existing_bytes > 0 and resp.status == 206 else "wb"
        if mode == "wb":
            existing_bytes = 0

        content_len = int(resp.headers.get("Content-Length", 0))
        total = existing_bytes + content_len
        downloaded = existing_bytes
        chunk_size = 1024 * 1024
        last_logged = 0

        with open(zip_path, mode) as f:
            while True:
                chunk = resp.read(chunk_size)
                if not chunk:
                    break
                f.write(chunk)
                downloaded += len(chunk)
                if downloaded - last_logged >= 10 * 1024 * 1024 or downloaded == total:
                    last_logged = downloaded
                    pct = (downloaded / total * 100) if total else 0
                    print(f"    Progress: {pct:5.1f}% ({downloaded // (1024*1024)}/{total // (1024*1024)} MB)")
        print()

    print("[*] Memilih dan mengekstrak 50 gambar AI dan 50 gambar Real (.jpg)...")
    with zipfile.ZipFile(zip_path, "r") as zf:
        ai_candidates = []
        real_candidates = []

        keywords = ("landscape", "scenery", "nature", "mountain", "sea", "forest", "view", "tree")

        for item in zf.infolist():
            name_lower = item.filename.lower()
            if not (name_lower.endswith(".jpg") or name_lower.endswith(".jpeg")):
                continue
            if item.file_size < 10000:  # skip corrupted/tiny files
                continue

            if "aiartdata" in name_lower:
                ai_candidates.append(item)
            elif "realart" in name_lower:
                real_candidates.append(item)

        # Sort prioritizing landscape/scenery keywords
        ai_candidates.sort(key=lambda x: not any(k in x.filename.lower() for k in keywords))
        real_candidates.sort(key=lambda x: not any(k in x.filename.lower() for k in keywords))

        selected_ai = ai_candidates[:50]
        selected_real = real_candidates[:50]

        for idx, item in enumerate(selected_ai, 1):
            target = os.path.join(out_ai_dir, f"ai_{idx:03d}.jpg")
            with zf.open(item) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)

        for idx, item in enumerate(selected_real, 1):
            target = os.path.join(out_real_dir, f"real_{idx:03d}.jpg")
            with zf.open(item) as src, open(target, "wb") as dst:
                shutil.copyfileobj(src, dst)

    if os.path.exists(zip_path):
        os.remove(zip_path)

    ai_count = len(os.listdir(out_ai_dir))
    real_count = len(os.listdir(out_real_dir))
    print(f"[✓] Berhasil mengumpulkan {ai_count} gambar AI di '{out_ai_dir}' dan {real_count} gambar Real di '{out_real_dir}'.")

if __name__ == "__main__":
    collect()
