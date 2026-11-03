import os

from utils import DATA_DIR

PATH_USER = os.path.join(DATA_DIR, "user.txt")

def muat_user():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(PATH_USER):
        open(PATH_USER, "a", encoding="utf-8").close()
    data = []
    with open(PATH_USER, "r", encoding="utf-8") as file:
        for baris in file:
            bagian = [item.strip() for item in baris.strip().split("|")]
            if len(bagian) == 4:
                data.append({"username": bagian[0], "password": bagian[1], "role": bagian[2], "nama_lengkap": bagian[3]})
    return data

def simpan_user(data):
    with open(PATH_USER, "w", encoding="utf-8") as file:
        for user in data:
            file.write(f"{user['username']}|{user['password']}|{user['role']}|{user['nama_lengkap']}\n")

def login(data):
    for percobaan in range(3):
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        for user in data:
            if user["username"] == username and user["password"] == password:
                print(f"Selamat datang, {user['nama_lengkap']}.")
                return user
        print(f"Username atau password salah. Sisa percobaan: {2 - percobaan}")
    return None

def tambah_user(data):
    username = input("Username baru: ").strip()
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

def ubah_password(data):
    username = input("Username: ").strip()
    for user in data:
        if user["username"] == username:
            user["password"] = input("Password baru: ").strip()
            simpan_user(data)
            print("Password berhasil diubah.")
            return
    print("User tidak ditemukan.")

def hapus_user(data, username_login):
    username = input("Username yang dihapus: ").strip()
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