
import tkinter as tk
from tkinter import messagebox
import sqlite3

# Membuat database SQLite
koneksi = sqlite3.connect("prediksi_siswa.db")
cursor = koneksi.cursor()

# Membuat tabel nilai_siswa
cursor.execute("""
CREATE TABLE IF NOT EXISTS nilai_siswa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_siswa TEXT NOT NULL,
    biologi INTEGER NOT NULL,
    fisika INTEGER NOT NULL,
    inggris INTEGER NOT NULL,
    prediksi_fakultas TEXT NOT NULL
)
""")

koneksi.commit()


# Fungsi untuk memproses nilai siswa
def submit_nilai():
    nama = entry_nama.get().strip()

    try:
        biologi = int(entry_biologi.get())
        fisika = int(entry_fisika.get())
        inggris = int(entry_inggris.get())
    except ValueError:
        messagebox.showerror(
            "Error", "Nilai harus diisi dengan angka!"
        )
        return

    if nama == "":
        messagebox.showerror("Error", "Nama siswa harus diisi!")
        return

    if any(nilai < 0 or nilai > 100
           for nilai in [biologi, fisika, inggris]):
        messagebox.showerror(
            "Error", "Nilai harus berada antara 0 sampai 100!"
        )
        return

    nilai_tertinggi = max(biologi, fisika, inggris)

    # Menentukan prediksi berdasarkan nilai tertinggi
    mata_pelajaran_tertinggi = [
        mapel for mapel, nilai in [
            ("Biologi", biologi),
            ("Fisika", fisika),
            ("Inggris", inggris)
        ]
        if nilai == nilai_tertinggi
    ]

    if len(mata_pelajaran_tertinggi) > 1:
        messagebox.showwarning(
            "Peringatan",
            "Nilai tertinggi sama. Masukkan nilai yang berbeda."
        )
        return

    if biologi == nilai_tertinggi:
        prediksi = "Kedokteran"
    elif fisika == nilai_tertinggi:
        prediksi = "Teknik"
    else:
        prediksi = "Bahasa"

    # Menyimpan data ke database
    cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))

    koneksi.commit()

    # Menampilkan hasil prediksi
    messagebox.showinfo(
        "Hasil Prediksi",
        f"Nama Siswa: {nama}\n"
        f"Biologi: {biologi}\n"
        f"Fisika: {fisika}\n"
        f"Inggris: {inggris}\n\n"
        f"Prediksi Fakultas: {prediksi}\n\n"
        "Data berhasil disimpan!"
    )

    # Mengosongkan input setelah berhasil
    entry_nama.delete(0, tk.END)
    entry_biologi.delete(0, tk.END)
    entry_fisika.delete(0, tk.END)
    entry_inggris.delete(0, tk.END)


# Membuat tampilan Tkinter
root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("400x430")
root.configure(bg="#29205c")

judul = tk.Label(
    root,
    text="PREDIKSI FAKULTAS",
    font=("Arial", 18, "bold"),
    bg="#29205c",
    fg="white"
)
judul.pack(pady=20)


def buat_input(label):
    tk.Label(
        root,
        text=label,
        font=("Arial", 11),
        bg="#29205c",
        fg="white"
    ).pack()

    entry = tk.Entry(root, font=("Arial", 11), width=30)
    entry.pack(pady=5)
    return entry


entry_nama = buat_input("Nama Siswa")
entry_biologi = buat_input("Nilai Biologi")
entry_fisika = buat_input("Nilai Fisika")
entry_inggris = buat_input("Nilai Inggris")

tombol_submit = tk.Button(
    root,
    text="Submit Nilai",
    font=("Arial", 12, "bold"),
    bg="#00d9ff",
    fg="#29205c",
    command=submit_nilai
)
tombol_submit.pack(pady=20)

root.mainloop()

# Menutup koneksi ketika program selesai
koneksi.close()
