from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RECEIPT_DIR = os.path.join(BASE_DIR, "struk")

def pastikan_folder():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RECEIPT_DIR, exist_ok=True)

def input_angka(pesan, minimum=0):
    while True:
        try:
            nilai = int(input(pesan).strip())
            if nilai < minimum:
                print(f"Nilai minimal adalah {minimum}.")
                continue
            return nilai
        except ValueError:
            print("Masukkan angka yang valid.")

def input_tanggal(pesan):
    while True:
        nilai = input(pesan).strip()
        try:
            datetime.strptime(nilai, "%Y-%m-%d")
            return nilai
        except ValueError:
            print("Format tanggal harus YYYY-MM-DD.")

def tanggal_valid(nilai):
    try:
        return datetime.strptime(nilai, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

def format_rupiah(nilai):
    return f"Rp{nilai:,.0f}".replace(",", ".")

def garis(panjang=78, karakter="-"):
    return karakter * panjang

def tunggu():
    input("\nTekan Enter untuk melanjutkan...")