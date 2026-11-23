# ==============================
# PENGELOLAAN AKUN DAN LOGIN
# ==============================

import os

from utils import DATA_DIR

# Lokasi file tempat semua data user disimpan.
PATH_USER = os.path.join(DATA_DIR, "user.txt")

# Membaca file user.txt dan mengubah setiap baris menjadi dictionary.
def muat_user():
    os.makedirs(DATA_DIR, exist_ok=True)

    # Buat file kosong jika file user belum pernah dibuat.
    if not os.path.exists(PATH_USER):
        open(PATH_USER, "a", encoding="utf-8").close()

    data = []
    with open(PATH_USER, "r", encoding="utf-8") as file:
        for baris in file:
            # Contoh baris: admin|admin123|admin|Administrator
            # Tanda | dipakai sebagai pemisah antara tiap informasi.
            bagian = [item.strip() for item in baris.strip().split("|")]

            # Baris valid harus berisi tepat 4 bagian.
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
    with open(PATH_USER, "w", encoding="utf-8") as file:
        for user in data:
            file.write(f"{user['username']}|{user['password']}|{user['role']}|{user['nama_lengkap']}\n")

# Mengecek username dan password hingga tiga kali percobaan.
def login(data):
    for percobaan in range(3):
        username = input("Username: ").strip()
        password = input("Password: ").strip()

        # Cari user yang memiliki username dan password yang cocok.
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

    for indeks, user in enumerate(data):
        if user["username"] == username:
            if input("Konfirmasi hapus? (y/n): ").strip().lower() == "y":
                data.pop(indeks)
                simpan_user(data)
                print("User berhasil dihapus.")
            return
    print("User tidak ditemukan.")