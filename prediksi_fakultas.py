import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT NOT NULL,
            biologi integer NOT NULL,
            fiska integer NOT NULL,
            inggris integer NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

def prediksi_fakultas(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Dapat Ditentukan"

def submit_nilai():
    class entry_nama:
        ...

    nama = entry_nama.get().strip()

    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())

    except ValueError:
        messagebox.showerror(
            "Error", "Nilai harus berupa angka!"
        )
        return

    if nama == "":
        messagebox.showerror(
            "Error", "Nama siswa harus diisi!"
        )
        return

    if any(nilai < 0 or nilai > 100 for nilai in [bio, fis, ing]):
        messagebox.showerror(
            "Error", "Nilai harus antara 0 sampai 100!"
        )
        return

    hasil = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO nilai_siswa
        (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil))

    conn.commit()
    conn.close()

    messagebox.showinfo(
        "Hasil Prediksi",
        f"Nama: {nama}\nPrediksi Fakultas: {hasil}"
    )
