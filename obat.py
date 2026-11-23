from datetime import date
import os

from utils import DATA_DIR, format_rupiah, input_angka, input_tanggal, tanggal_valid

# ==============================
# PENGELOLAAN DATA OBAT
# ==============================

# Modul ini menyimpan semua data obat dalam data/obat.txt.

PATH_OBAT = os.path.join(DATA_DIR, "obat.txt")
GOLONGAN = ("bebas", "bebas terbatas", "keras")

# Membaca data obat dari file dan menjadikannya daftar dictionary.
def muat_obat():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PATH_OBAT):
        open(PATH_OBAT, "a", encoding="utf-8").close()
    data = []
    with open(PATH_OBAT, "r", encoding="utf-8") as file:
        for nomor, baris in enumerate(file, 1):
            if not baris.strip():
                continue
            bagian = [item.strip() for item in baris.strip().split("|")]
            if len(bagian) != 7:
                print(f"Peringatan: baris obat ke-{nomor} dilewati.")
                continue
            try:
                harga, stok = int(bagian[4]), int(bagian[5])
                if harga < 0 or stok < 0 or tanggal_valid(bagian[6]) is None:
                    raise ValueError
            except ValueError:
                print(f"Peringatan: data obat ke-{nomor} rusak dan dilewati.")
                continue
            data.append({"kode": bagian[0].upper(), "nama": bagian[1], "golongan": bagian[2].lower(),
                         "satuan": bagian[3], "harga": harga, "stok": stok, "kedaluwarsa": bagian[6]})
    return data

# Menulis ulang seluruh data obat ke obat.txt.
def simpan_obat(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(PATH_OBAT, "w", encoding="utf-8") as file:
        for obat in data:
            file.write("|".join([obat["kode"], obat["nama"], obat["golongan"], obat["satuan"],
                                 str(obat["harga"]), str(obat["stok"]), obat["kedaluwarsa"]]) + "\n")

# Mengurutkan obat berdasarkan nama, harga, stok, atau kedaluwarsa.
def urutkan(data, kunci, naik=True):
    hasil = data.copy()
    if kunci in ("harga", "stok"):
        for batas in range(len(hasil) - 1, 0, -1):
            for indeks in range(batas):
                if (hasil[indeks][kunci] > hasil[indeks + 1][kunci]) == naik:
                    hasil[indeks], hasil[indeks + 1] = hasil[indeks + 1], hasil[indeks]
    else:
        for indeks in range(len(hasil)):
            pilihan = indeks
            for pembanding in range(indeks + 1, len(hasil)):
                if (hasil[pembanding][kunci] < hasil[pilihan][kunci]) == naik:
                    pilihan = pembanding
            hasil[indeks], hasil[pilihan] = hasil[pilihan], hasil[indeks]
    return hasil

# Mencari obat berdasarkan kode menggunakan pencarian biner.
def cari_kode(data, kode):
    terurut = urutkan(data, "kode")
    kiri, kanan = 0, len(terurut) - 1
    kode = kode.upper()
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        if terurut[tengah]["kode"] == kode:
            for indeks, obat in enumerate(data):
                if obat["kode"] == kode:
                    return indeks
            return -1
        if terurut[tengah]["kode"] < kode:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1

# Mencari nama obat yang mengandung kata pencarian.
def cari_nama(data, kata):
    kata = kata.lower()
    return [obat for obat in data if kata in obat["nama"].lower()]

# Mengecek apakah tanggal kedaluwarsa sudah lewat.
def sudah_kedaluwarsa(tanggal):
    nilai = tanggal_valid(tanggal) if isinstance(tanggal, str) else tanggal
    return nilai is not None and nilai < date.today()

# Mengambil semua obat yang stoknya kurang dari batas yang ditentukan.
def cek_stok_menipis(data, batas=10):
    return [obat for obat in data if obat["stok"] < batas]

# Menampilkan daftar obat dalam bentuk tabel.
def tampil_obat(data):
    if not data:
        print("Belum ada data obat.")
        return
    print(f"{'Kode':<8} {'Nama':<26} {'Golongan':<16} {'Harga':>12} {'Stok':>6} {'Exp':<12}")
    print("-" * 84)
    for obat in data:
        print(f"{obat['kode']:<8} {obat['nama'][:25]:<26} {obat['golongan']:<16} "
              f"{format_rupiah(obat['harga']):>12} {obat['stok']:>6} {obat['kedaluwarsa']:<12}")

# Meminta data obat baru, memvalidasi, lalu menyimpannya.
def tambah_obat(data):
    kode = input("Kode obat (OBxxx): ").strip().upper()
    if not kode.startswith("OB") or not kode[2:].isalnum() or any(o["kode"] == kode for o in data):
        print("Kode tidak valid atau sudah digunakan.")
        return
    nama = input("Nama obat: ").strip()
    golongan = input(f"Golongan {GOLONGAN}: ").strip().lower()
    if golongan not in GOLONGAN:
        print("Golongan tidak valid.")
        return
    satuan = input("Satuan: ").strip()
    harga = input_angka("Harga: ", 0)
    stok = input_angka("Stok: ", 0)
    kedaluwarsa = input_tanggal("Kedaluwarsa (YYYY-MM-DD): ")
    data.append({"kode": kode, "nama": nama, "golongan": golongan, "satuan": satuan,
                 "harga": harga, "stok": stok, "kedaluwarsa": kedaluwarsa})
    simpan_obat(data)
    print("Obat berhasil ditambahkan.")

# Mengubah bagian data obat yang diisi pengguna.
def ubah_obat(data):
    kode = input("Kode obat yang diubah: ").strip().upper()
    indeks = cari_kode(data, kode)
    if indeks == -1:
        print("Obat tidak ditemukan.")
        return
    obat = data[indeks]
    print("Kosongkan input jika tidak ingin mengubah nilai.")
    nama = input(f"Nama [{obat['nama']}]: ").strip()
    harga = input(f"Harga [{obat['harga']}]: ").strip()
    stok = input(f"Stok [{obat['stok']}]: ").strip()
    kedaluwarsa = input(f"Kedaluwarsa [{obat['kedaluwarsa']}]: ").strip()
    if nama:
        obat["nama"] = nama
    if harga:
        try:
            obat["harga"] = int(harga)
            if obat["harga"] < 0: raise ValueError
        except ValueError:
            print("Harga tidak valid.")
            return
    if stok:
        try:
            obat["stok"] = int(stok)
            if obat["stok"] < 0: raise ValueError
        except ValueError:
            print("Stok tidak valid.")
            return
    if kedaluwarsa:
        if tanggal_valid(kedaluwarsa) is None:
            print("Tanggal tidak valid.")
            return
        obat["kedaluwarsa"] = kedaluwarsa
    simpan_obat(data)
    print("Obat berhasil diubah.")

# Menghapus obat setelah kode ditemukan dan pengguna mengonfirmasi.
def hapus_obat(data):
    kode = input("Kode obat yang dihapus: ").strip().upper()
    indeks = cari_kode(data, kode)
    if indeks == -1:
        print("Obat tidak ditemukan.")
        return
    if input(f"Hapus {data[indeks]['nama']}? (y/n): ").strip().lower() == "y":
        data.pop(indeks)
        simpan_obat(data)
        print("Obat berhasil dihapus.")