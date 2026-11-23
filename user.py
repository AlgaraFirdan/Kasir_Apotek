# ==============================
# PENGELOLAAN AKUN DAN LOGIN
# ==============================

import os

from utils import DATA_DIR

# Lokasi file tempat semua data user disimpan.
PATH_USER = os.path.join(DATA_DIR, "user.txt")

# Membaca file user.txt dan mengubah setiap baris menjadi dictionary.
def muat_user():
    # os.makedirs memastikan folder data ada. exist_ok=True berarti tidak error jika sudah ada.
    os.makedirs(DATA_DIR, exist_ok=True)

    # Buat file kosong jika file user belum pernah dibuat.
    if not os.path.exists(PATH_USER):
        open(PATH_USER, "a", encoding="utf-8").close()

    data = []
    with open(PATH_USER, "r", encoding="utf-8") as file:
        for baris in file:
            # Contoh baris: admin|admin123|admin|Administrator
            # Tanda | dipakai sebagai pemisah antara tiap informasi.
            # strip() menghapus spasi tersisa, sedangkan split("|") memotong kolom berdasarkan pemisah |
            bagian = [item.strip() for item in baris.strip().split("|")]

            # Baris valid harus berisi tepat 4 bagian.
            # Dictionary memudahkan penggunaan data, misalnya user["username"] atau user["role"].
            if len(bagian) == 4:
                data.append({
                    "username": bagian[0],
                    "password": bagian[1],
                    "role": bagian[2],
                    "nama_lengkap": bagian[3]
                })
    return data

# Menyimpan kembali seluruh daftar user ke file user.txt.
def simpan_user(data):
    # Mode "w" membuka file untuk ditulis ulang, sehingga data lama diganti dengan isi data terbaru.
    with open(PATH_USER, "w", encoding="utf-8") as file:
        for user in data:
            file.write(f"{user['username']}|{user['password']}|{user['role']}|{user['nama_lengkap']}\n")

# Mengecek username dan password hingga tiga kali percobaan.
def login(data):
    # range(3) menghasilkan tiga percobaan: indeks 0, 1, dan 2.
    for percobaan in range(3):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Cari user yang memiliki username dan password yang cocok.
        # AND berarti kedua syarat harus benar: username cocok dan password juga cocok.
        for user in data:
            if user["username"] == username and user["password"] == password:
                print(f"Selamat datang, {user['nama_lengkap']}.")
                return user

        print(f"Username atau password salah. Sisa percobaan: {2 - percobaan}")
    return None

# Menambah user baru ke daftar dan menyimpannya ke file.
def tambah_user(data):
    username = input("Username baru: ").strip()

    # Username tidak boleh kosong atau sama dengan user yang sudah ada.
    # any() bernilai True jika terdapat sedikitnya satu user yang username-nya sama.
    if not username or any(user["username"] == username for user in data):
        print("Username kosong atau sudah digunakan.")
        return

    password = input("Password: ").strip()
    role = input("Role (admin/kasir): ").strip().lower()
    if role not in ("admin", "kasir"):
        print("Role tidak valid.")
        return

    nama = input("Nama lengkap: ").strip()
    data.append({"username": username, "password": password, "role": role, "nama_lengkap": nama})
    simpan_user(data)
    print("User berhasil ditambahkan.")

# Mengubah password milik salah satu user.
def ubah_password(data):
    username = input("Username: ").strip()
    for user in data:
        if user["username"] == username:
            # Mengubah nilai password pada dictionary yang ditemukan.
            user["password"] = input("Password baru: ").strip()
            simpan_user(data)
            print("Password berhasil diubah.")
            return
    print("User tidak ditemukan.")

# Menghapus user lain setelah meminta konfirmasi.
def hapus_user(data, username_login):
    username = input("Username yang dihapus: ").strip()

    # Mencegah admin menghapus akun yang sedang dipakai.
    if username == username_login:
        print("Admin tidak boleh menghapus dirinya sendiri.")
        return

    # enumerate memberikan posisi indeks sekaligus isi data agar user dapat dihapus dari list.
    for indeks, user in enumerate(data):
        if user["username"] == username:
            if input("Konfirmasi hapus? (y/n): ").strip().lower() == "y":
                data.pop(indeks)
                simpan_user(data)
                print("User berhasil dihapus.")
            return
    print("User tidak ditemukan.")