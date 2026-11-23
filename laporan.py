import os
from datetime import date, datetime, timedelta

from obat import cek_stok_menipis
from transaksi import PATH_DETAIL, PATH_TRANSAKSI
from utils import format_rupiah, input_tanggal

# ==============================
# LAPORAN PENJUALAN DAN STOK
# ==============================

# Data laporan diambil dari data/transaksi.txt dan data/detail_transaksi.txt.

# Membaca file teks menjadi daftar baris yang dipisahkan tanda |.
def baca_baris(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as file:
        return [baris.strip().split("|") for baris in file if baris.strip()]

# Menghitung jumlah dan pendapatan transaksi pada tanggal tertentu.
def laporan_harian():
    tanggal = input_tanggal("Tanggal laporan (YYYY-MM-DD): ")
    transaksi = [b for b in baca_baris(PATH_TRANSAKSI) if len(b) == 7 and b[1].startswith(tanggal)]
    total = sum(int(b[3]) for b in transaksi)
    print(f"Transaksi {tanggal}: {len(transaksi)} | Pendapatan: {format_rupiah(total)}")
    for b in transaksi:
        print(f"{b[0]} - {b[2]} - {format_rupiah(int(b[3]))}")

# Menghitung obat yang paling banyak dibeli dari detail transaksi.
def obat_terlaris():
    jumlah = {}
    nama = {}
    for bagian in baca_baris(PATH_DETAIL):
        if len(bagian) == 6:
            jumlah[bagian[1]] = jumlah.get(bagian[1], 0) + int(bagian[3])
            nama[bagian[1]] = bagian[2]
    hasil = list(jumlah.items())
    for indeks in range(len(hasil)):
        terbesar = indeks
        for pembanding in range(indeks + 1, len(hasil)):
            if hasil[pembanding][1] > hasil[terbesar][1]:
                terbesar = pembanding
        hasil[indeks], hasil[terbesar] = hasil[terbesar], hasil[indeks]
    print("5 obat terlaris:")
    for kode, banyak in hasil[:5]:
        print(f"{kode} - {nama[kode]}: {banyak} unit")

# Menampilkan obat dengan stok paling sedikit dan mengurutkannya.
def laporan_stok(data):
    hasil = cek_stok_menipis(data)
    for indeks in range(len(hasil)):
        pilihan = indeks
        for pembanding in range(indeks + 1, len(hasil)):
            if hasil[pembanding]["stok"] < hasil[pilihan]["stok"]:
                pilihan = pembanding
        hasil[indeks], hasil[pilihan] = hasil[pilihan], hasil[indeks]
    if not hasil:
        print("Tidak ada stok menipis.")
    for obat in hasil:
        print(f"{obat['kode']} - {obat['nama']}: {obat['stok']} {obat['satuan']}")

# Menampilkan obat kedaluwarsa atau hampir kedaluwarsa dalam 90 hari.
def laporan_kedaluwarsa(data):
    hari_ini = date.today()
    batas = hari_ini + timedelta(days=90)
    hasil = []
    for obat in data:
        tanggal = datetime.strptime(obat["kedaluwarsa"], "%Y-%m-%d").date()
        if tanggal <= batas:
            hasil.append((tanggal, obat))
    hasil.sort(key=lambda item: item[0])
    if not hasil:
        print("Tidak ada obat kedaluwarsa atau hampir kedaluwarsa.")
    for tanggal, obat in hasil:
        status = "SUDAH" if tanggal < hari_ini else "hampir"
        print(f"{obat['kode']} - {obat['nama']}: {tanggal} ({status})")

# Mengelompokkan pendapatan berdasarkan username kasir.
def total_pendapatan():
    hasil = {}
    for bagian in baca_baris(PATH_TRANSAKSI):
        if len(bagian) == 7:
            hasil[bagian[2]] = hasil.get(bagian[2], 0) + int(bagian[3])
    for kasir, total in hasil.items():
        print(f"{kasir}: {format_rupiah(total)}")