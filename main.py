# =====================================
# FILE UTAMA: MENU DAN ALUR APLIKASI
# =====================================

from laporan import laporan_harian, laporan_kedaluwarsa, laporan_stok, obat_terlaris, total_pendapatan
from obat import cari_kode, cari_nama, hapus_obat, muat_obat, tambah_obat, tampil_obat, ubah_obat, urutkan
from transaksi import proses_transaksi, riwayat_kasir
from user import hapus_user, login, muat_user, tambah_user, ubah_password
from utils import garis, pastikan_folder, tunggu

# Menu pengelolaan data obat untuk admin.
def menu_obat(data):
    while True:
        print("\n" + garis())
        print("KELOLA OBAT")
        print("1. Tambah  2. Lihat  3. Cari  4. Ubah  5. Hapus  6. Urutkan  0. Kembali")
        pilihan = input("Pilih: ").strip()
        # Memanggil fungsi yang berbeda sesuai angka pilihan admin.
        if pilihan == "1": tambah_obat(data)
        elif pilihan == "2": tampil_obat(data)
        elif pilihan == "3":
            mode = input("Cari kode atau nama? ").strip().lower()
            if mode == "kode":
                indeks = cari_kode(data, input("Kode: ").strip())
                tampil_obat([data[indeks]] if indeks >= 0 else [])
            else: tampil_obat(cari_nama(data, input("Kata nama: ").strip()))
        elif pilihan == "4": ubah_obat(data)
        elif pilihan == "5": hapus_obat(data)
        elif pilihan == "6":
            kunci = input("Urut berdasarkan nama/harga/stok/kedaluwarsa: ").strip().lower()
            if kunci in ("nama", "harga", "stok", "kedaluwarsa"):
                tampil_obat(urutkan(data, kunci, input("Naik? (y/n): ").lower() == "y"))
            else: print("Kunci sorting tidak valid.")
        elif pilihan == "0": return
        else: print("Pilihan tidak valid.")
        if pilihan != "0": tunggu()

# Menu pengelolaan akun untuk admin.
def menu_user(data, user):
    while True:
        print("\nKELOLA USER\n1. Tambah\n2. Ubah password\n3. Hapus\n0. Kembali")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1": tambah_user(data)
        elif pilihan == "2": ubah_password(data)
        elif pilihan == "3": hapus_user(data, user["username"])
        elif pilihan == "0": return
        else: print("Pilihan tidak valid.")
        if pilihan != "0": tunggu()

# Menu pilihan laporan untuk admin.
def menu_laporan(data):
    while True:
        print("\nLAPORAN\n1. Penjualan harian\n2. Obat terlaris\n3. Stok menipis\n4. Kedaluwarsa\n5. Total pendapatan\n0. Kembali")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1": laporan_harian()
        elif pilihan == "2": obat_terlaris()
        elif pilihan == "3": laporan_stok(data)
        elif pilihan == "4": laporan_kedaluwarsa(data)
        elif pilihan == "5": total_pendapatan()
        elif pilihan == "0": return
        else: print("Pilihan tidak valid.")
        if pilihan != "0": tunggu()

# Menu utama admin. Akses ini hanya diberikan setelah login sebagai admin.
def menu_admin(user, users, data):
    while True:
        print("\n" + garis() + "\nMENU ADMIN\n1. Kelola Obat\n2. Kelola User\n3. Laporan\n4. Logout")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1": menu_obat(data)
        elif pilihan == "2": menu_user(users, user)
        elif pilihan == "3": menu_laporan(data)
        elif pilihan == "4": return
        else: print("Pilihan tidak valid.")

# Menu utama kasir. Kasir dapat bertransaksi dan melihat riwayat miliknya.
def menu_kasir(user, data):
    while True:
        print("\n" + garis() + "\nMENU KASIR\n1. Transaksi baru\n2. Cari obat\n3. Riwayat transaksi saya\n4. Logout")
        pilihan = input("Pilih: ").strip()
        if pilihan == "1": proses_transaksi(data, user)
        elif pilihan == "2": tampil_obat(cari_nama(data, input("Nama obat: ").strip()))
        elif pilihan == "3": riwayat_kasir(user["username"])
        elif pilihan == "4": return
        else: print("Pilihan tidak valid.")
        if pilihan != "4": tunggu()

# Titik awal program. Semua folder, user, dan obat dimuat dari sini.
def main():
    # pastikan_folder() menyiapkan lokasi penyimpanan sebelum file dibaca atau ditulis.
    pastikan_folder()

    # muat_user() dan muat_obat() mengubah isi file menjadi data Python yang siap dipakai.
    users, data = muat_user(), muat_obat()
    print("\nAPLIKASI KASIR APOTEK")
    while True:
        # login() mengembalikan None jika username/password salah sebanyak tiga kali.
        user = login(users)
        if user is None:
            print("Login gagal tiga kali. Program selesai.")
            return

        # Tampilkan menu berdasarkan peran user yang berhasil login.
        # Jika role admin buka menu admin, sedangkan role lain diperlakukan sebagai kasir.
        if user["role"] == "admin":
            menu_admin(user, users, data)
        else:
            menu_kasir(user, data)
        print("Anda telah logout.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram dihentikan dengan rapi.")
# while True membuat menu terus muncul sampai dipilih kembali atau logout.
        # strip() menghapus spasi awal/akhir agar input " 1 " tetap diterima sebagai pilihan 1.