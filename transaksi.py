from datetime import datetime
import os

from obat import cari_kode, sudah_kedaluwarsa, simpan_obat
from utils import DATA_DIR, RECEIPT_DIR, format_rupiah, input_angka, garis, tanggal_valid

# ==============================
# TRANSAKSI PEMBELIAN OBAT
# ==============================

# Modul ini mengelola keranjang, pembayaran, stok, riwayat, dan struk.

PATH_TRANSAKSI = os.path.join(DATA_DIR, "transaksi.txt")
PATH_DETAIL = os.path.join(DATA_DIR, "detail_transaksi.txt")
BATAS_DISKON = 100000
PERSEN_DISKON = 5

# Menambahkan obat ke keranjang, atau menambah jumlah jika obat sudah ada.
def tambah_ke_keranjang(keranjang, obat, jumlah):
    for item in keranjang:
        if item["kode"] == obat["kode"]:
            item["jumlah"] += jumlah
            item["subtotal"] = item["jumlah"] * item["harga"]
            return
    keranjang.append({"kode": obat["kode"], "nama": obat["nama"], "jumlah": jumlah,
                      "harga": obat["harga"], "subtotal": jumlah * obat["harga"]})

def tampil_keranjang(keranjang):
    if not keranjang:
        print("Keranjang masih kosong.")
        return
    print(garis())
    for nomor, item in enumerate(keranjang, 1):
        print(f"{nomor}. {item['nama']} ({item['kode']}) - {item['jumlah']} x "
              f"{format_rupiah(item['harga'])} = {format_rupiah(item['subtotal'])}")
    print(garis())

def hapus_dari_keranjang(keranjang):
    tampil_keranjang(keranjang)
    if keranjang:
        nomor = input_angka("Nomor item yang dihapus: ", 1)
        if nomor <= len(keranjang):
            keranjang.pop(nomor - 1)
            print("Item dihapus.")
        else:
            print("Nomor item tidak valid.")

# Menghitung diskon berdasarkan subtotal keranjang.
def hitung_diskon(total):
    # // membuang angka desimal sehingga diskon tetap berupa rupiah bulat.
    return total * PERSEN_DISKON // 100 if total >= BATAS_DISKON else 0

def hitung_total(keranjang):
    subtotal = sum(item["subtotal"] for item in keranjang)
    diskon = hitung_diskon(subtotal)
    return subtotal, diskon, subtotal - diskon

# Meminta uang pembayaran dan mengulang sampai nilainya cukup.
def proses_bayar(total):
    while True:
        bayar = input_angka(f"Bayar ({format_rupiah(total)}): ", 0)
        if bayar >= total:
            return bayar, bayar - total
        print("Uang bayar kurang dari total.")

# Membuat nomor transaksi unik dari tanggal dan waktu saat ini.
def buat_id_transaksi():
    return "TRX" + datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]

def buat_struk(id_transaksi, waktu, nama_kasir, keranjang, total, diskon, bayar, kembalian):
    baris = ["=" * 40, "APOTEK SEHAT".center(40), "=" * 40,
             f"No    : {id_transaksi}", f"Tgl   : {waktu}", f"Kasir : {nama_kasir}", "-" * 40]
    for item in keranjang:
        baris.extend([item["nama"], f"  {item['jumlah']} x {format_rupiah(item['harga'])}"
                      f"{'':>12}{format_rupiah(item['subtotal']):>12}"])
    baris.extend(["-" * 40, f"SUBTOTAL{'':>24}{format_rupiah(total + diskon):>12}",
                  f"DISKON{'':>27}{format_rupiah(diskon):>12}",
                  f"TOTAL{'':>28}{format_rupiah(total):>12}",
                  f"BAYAR{'':>28}{format_rupiah(bayar):>12}",
                  f"KEMBALI{'':>26}{format_rupiah(kembalian):>12}", "=" * 40,
                  "Terima kasih, semoga lekas sembuh"])
    return "\n".join(baris)

# Menyimpan header transaksi dan setiap item barang yang dibeli.
def simpan_transaksi(id_transaksi, waktu, username, keranjang, total, diskon, bayar, kembalian):
    os.makedirs(DATA_DIR, exist_ok=True)
    # Mode "a" menambahkan data baru tanpa menghapus transaksi lama.
    with open(PATH_TRANSAKSI, "a", encoding="utf-8") as file:
        file.write(f"{id_transaksi}|{waktu}|{username}|{total}|{diskon}|{bayar}|{kembalian}\n")
    with open(PATH_DETAIL, "a", encoding="utf-8") as file:
        for item in keranjang:
            file.write(f"{id_transaksi}|{item['kode']}|{item['nama']}|{item['jumlah']}|{item['harga']}|{item['subtotal']}\n")

# Menulis teks struk ke folder struk dan mengembalikan lokasi filenya.
def simpan_struk(id_transaksi, teks):
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    path = os.path.join(RECEIPT_DIR, f"{id_transaksi}.txt")
    with open(path, "w", encoding="utf-8") as file:
        file.write(teks)
    return path

# Mengurangi stok setiap obat yang dibeli, lalu menyimpannya ke file obat.
def kurangi_stok(data, keranjang):
    # Pengurangan dilakukan setiap item dalam keranjang, bukan langsung untuk seluruh keranjang sekaligus.
    for item in keranjang:
        indeks = cari_kode(data, item["kode"])
        data[indeks]["stok"] -= item["jumlah"]
    simpan_obat(data)

# Menampilkan hanya transaksi milik kasir yang sedang login.
def riwayat_kasir(username):
    if not os.path.exists(PATH_TRANSAKSI):
        print("Belum ada transaksi.")
        return
    ditemukan = False
    with open(PATH_TRANSAKSI, "r", encoding="utf-8") as file:
        for baris in file:
            bagian = baris.strip().split("|")
            if len(bagian) == 7 and bagian[2] == username:
                ditemukan = True
                print(f"{bagian[0]} | {bagian[1]} | Total {format_rupiah(int(bagian[3]))}")
    if not ditemukan:
        print("Belum ada riwayat transaksi.")

# Alur lengkap satu transaksi: isi keranjang, bayar, kurangi stok, simpan, dan cetak struk.
def proses_transaksi(data, user):
    # Keranjang dimulai kosong. Setiap obat yang diterima ditambahkan sebagai dictionary.
    keranjang = []
    while True:
        tampil_keranjang(keranjang)
        kode = input("Kode obat (kosong untuk selesai input): ").strip().upper()
        # Jika kasir menekan Enter tanpa mengisi kode, pengisian keranjang dihentikan.
        if not kode:
            break
        # cari_kode() mengembalikan posisi obat pada list, atau -1 jika tidak ditemukan.
        indeks = cari_kode(data, kode)
        if indeks == -1:
            print("Obat tidak ditemukan.")
            continue
        obat = data[indeks]
        # Obat ditolak sebelum masuk keranjang jika tanggal kedaluwarsanya sudah lewat.
        if sudah_kedaluwarsa(obat["kedaluwarsa"]):
            print(f"Ditolak: obat kedaluwarsa pada {obat['kedaluwarsa']}.")
            continue
        # AND berarti konfirmasi resep hanya dibutuhkan ketika obat berstatus keras.
        if obat["golongan"] == "keras" and input("Konfirmasi resep dokter? (y/n): ").lower() != "y":
            print("Item dibatalkan karena resep tidak dikonfirmasi.")
            continue
        jumlah = input_angka("Jumlah: ", 1)
        # next() mencari jumlah obat ini di keranjang; default-nya 0 jika belum ada.
        sudah_ada = next((item["jumlah"] for item in keranjang if item["kode"] == kode), 0)
        # Jumlah baru ditambah jumlah lama tidak boleh melebihi stok yang tersedia.
        if jumlah + sudah_ada > obat["stok"]:
            print(f"Stok tidak cukup. Sisa stok: {obat['stok'] - sudah_ada}.")
            continue
        # Selisih negatif berarti sudah lewat; selisih kurang dari 90 berarti hampir kedaluwarsa.
        if (tanggal := tanggal_valid(obat["kedaluwarsa"])):
            if (tanggal - datetime.now().date()).days < 90:
                print("Peringatan: obat hampir kedaluwarsa.")
        tambah_ke_keranjang(keranjang, obat, jumlah)
    if not keranjang:
        print("Transaksi dibatalkan karena keranjang kosong.")
        return
    subtotal, diskon, total = hitung_total(keranjang)
    print(f"Subtotal: {format_rupiah(subtotal)} | Diskon: {format_rupiah(diskon)} | Total: {format_rupiah(total)}")
    bayar, kembalian = proses_bayar(total)
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id_transaksi = buat_id_transaksi()
    kurangi_stok(data, keranjang)
    simpan_transaksi(id_transaksi, waktu, user["username"], keranjang, total, diskon, bayar, kembalian)
    teks = buat_struk(id_transaksi, waktu, user["nama_lengkap"], keranjang, total, diskon, bayar, kembalian)
    path = simpan_struk(id_transaksi, teks)
    print(teks)
    print(f"Struk tersimpan di {path}")
    for item in keranjang:
        indeks = cari_kode(data, item["kode"])
        if data[indeks]["stok"] < 10:
            print(f"Peringatan: stok {data[indeks]['nama']} menipis ({data[indeks]['stok']}).")