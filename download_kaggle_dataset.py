import os
import sys
import json
import zipfile
import argparse
import urllib.request
import urllib.error

# ponytail: stdlib urllib over requests/kaggle CLI to avoid extra dependencies

def get_token() -> str:
    # 1. Check local kaggle.json
    local_cfg = os.path.join(os.path.dirname(__file__), "kaggle.json")
    if os.path.exists(local_cfg):
        try:
            with open(local_cfg, "r") as f:
                data = json.load(f)
                token = data.get("token") or data.get("key")
                if token:
                    return token.strip()
        except Exception:
            pass

    # 2. Check environment variable
    env_token = os.environ.get("KAGGLE_API_TOKEN")
    if env_token:
        return env_token.strip()

    # 3. Check ~/.kaggle/access_token
    user_token_file = os.path.expanduser("~/.kaggle/access_token")
    if os.path.exists(user_token_file):
        try:
            with open(user_token_file, "r") as f:
                token = f.read().strip()
                if token:
                    return token
        except Exception:
            pass

    raise RuntimeError("Kaggle API token tidak ditemukan di kaggle.json atau ~/.kaggle/access_token")


def check_connection(token: str) -> bool:
    url = "https://www.kaggle.com/api/v1/datasets/list?pageSize=1"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        with urllib.request.urlopen(req) as resp:
            if resp.status == 200:
                print("[✓] Koneksi ke Kaggle API berhasil! Token aktif.")
                return True
    except urllib.error.HTTPError as e:
        print(f"[!] Gagal terhubung ke Kaggle: HTTP {e.code} ({e.reason})")
    except Exception as e:
        print(f"[!] Gagal terhubung ke Kaggle: {e}")
    return False


def download_dataset(dataset_slug: str, output_dir: str = "dataset") -> None:
    token = get_token()
    dataset_slug = dataset_slug.strip().strip("/")
    url = f"https://www.kaggle.com/api/v1/datasets/download/{dataset_slug}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})

    os.makedirs(output_dir, exist_ok=True)
    zip_path = os.path.join(output_dir, "temp_dataset.zip")

    print(f"[*] Mengunduh dataset: {dataset_slug}")
    print(f"[*] Target folder: {output_dir}")

    try:
        with urllib.request.urlopen(req) as resp:
            total = int(resp.headers.get("Content-Length", 0))
            downloaded = 0
            chunk_size = 1024 * 1024  # 1MB chunks

            with open(zip_path, "wb") as f:
                while True:
                    chunk = resp.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        pct = (downloaded / total) * 100
                        mb_done = downloaded / (1024 * 1024)
                        mb_total = total / (1024 * 1024)
                        sys.stdout.write(f"\r    Progress: {pct:5.1f}% ({mb_done:.1f}/{mb_total:.1f} MB)")
                        sys.stdout.flush()

        print("\n[*] Ekstraksi file...")
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(output_dir)

        if os.path.exists(zip_path):
            os.remove(zip_path)

        print(f"[✓] Berhasil! Dataset siap digunakan di '{output_dir}'.")

    except urllib.error.HTTPError as e:
        if os.path.exists(zip_path):
            os.remove(zip_path)
        print(f"\n[!] Gagal mengunduh dataset: HTTP {e.code} ({e.reason})")
    except Exception as e:
        if os.path.exists(zip_path):
            os.remove(zip_path)
        print(f"\n[!] Terjadi kesalahan: {e}")


def main():
    parser = argparse.ArgumentParser(description="Kaggle Dataset Downloader (AI Image Detector)")
    parser.add_argument("dataset", nargs="?", help="Slug dataset Kaggle (contoh: cashbowman/ai-generated-images-vs-real-images)")
    parser.add_argument("-o", "--out", default="dataset", help="Folder tujuan penyimpanan dataset (default: dataset)")
    parser.add_argument("--check", action="store_true", help="Cek validitas token dan koneksi ke Kaggle API")

    args = parser.parse_args()

    try:
        token = get_token()
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

    if args.check or not args.dataset:
        ok = check_connection(token)
        if not args.dataset:
            print("\nCara penggunaan untuk mengunduh dataset nanti:")
            print("  python download_kaggle_dataset.py <owner>/<dataset-name>")
            print("Contoh:")
            print("  python download_kaggle_dataset.py cashbowman/ai-generated-images-vs-real-images")
        sys.exit(0 if ok else 1)

    download_dataset(args.dataset, args.out)


if __name__ == "__main__":
    main()
