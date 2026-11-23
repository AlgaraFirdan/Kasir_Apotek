# ==============================
# FUNGSI BANTU UNTUK SELURUH APP
# ==============================

from datetime import datetime
import os

# Lokasi folder ini mengikuti lokasi file utils.py.
# Jadi folder data dan struk tetap ditemukan meskipun app dijalankan dari folder lain.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
RECEIPT_DIR = os.path.join(BASE_DIR, "struk")

# Menyiapkan folder penyimpanan data dan struk.
def pastikan_folder():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(RECEIPT_DIR, exist_ok=True)

# Meminta input angka dan terus mengulang sampai nilainya valid.
# try menangkap kesalahan jika input tidak dapat diubah menjadi integer.
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

# Meminta tanggal dalam format YYYY-MM-DD, misalnya 2027-12-31.
# strptime hanya menerima tanggal yang sesuai dengan pola YYYY-MM-DD.
def input_tanggal(pesan):
    while True:
        nilai = input(pesan).strip()
        try:
            datetime.strptime(nilai, "%Y-%m-%d")
            return nilai
        except ValueError:
            print("Format tanggal harus YYYY-MM-DD.")

# Mengubah teks tanggal menjadi objek tanggal.
# None digunakan sebagai tanda bahwa nilai bukan tanggal yang dapat dipakai.
def tanggal_valid(nilai):
    try:
        return datetime.strptime(nilai, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None

# Mengubah angka menjadi tampilan mata uang Indonesia.
# :,.0f menambah pemisah ribuan, lalu koma diganti titik agar menjadi format Indonesia.
def format_rupiah(nilai):
    return f"Rp{nilai:,.0f}".replace(",", ".")

# Membuat garis untuk mempercantik dan memisahkan tampilan terminal.
def garis(panjang=78, karakter="-"):
    return karakter * panjang

# Memberi jeda sampai pengguna menekan Enter.
def tunggu():
    input("\nTekan Enter untuk melanjutkan...")