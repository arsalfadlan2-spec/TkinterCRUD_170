import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

create_db()

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
    nama = entry_nama.get().strip()
    try:
        bio = int(entry_bio.get())
        fis = int(entry_fis.get())
        ing = int(entry_ing.get())
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka!")
        return

    prediksi = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, prediksi))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", f"Prediksi Fakultas: {prediksi}")
    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

def on_enter(e):
    btn_submit["bg"] = "#050fa7b"
    btn_submit["fg"] = "black"

def on_leave(e):
    btn_submit["bg"] = "#044475a"
    btn_submit["fg"] = "black"

    create_db()

root = tk.Tk()
root.title("Prediksi Fakultas Siswa")
root.geometry("400x400")

tk.Label(root, text="Nama Siswa:").pack(pady=5)
entry_nama = tk.Entry(root, width=30)
entry_nama.pack(pady=5)

tk.Label(root, text="Nilai Biologi:").pack(pady=5)
entry_bio = tk.Entry(root, width=30)
entry_bio.pack(pady=5)

tk.Label(root, text="Nilai Fisika:").pack(pady=5)
entry_fis = tk.Entry(root, width=30)
entry_fis.pack(pady=5)

tk.Label(root, text="Nilai Bahasa Inggris:").pack(pady=5)
entry_ing = tk.Entry(root, width=30)
entry_ing.pack(pady=5)

btn_submit = tk.Button(root, text="Submit Nilai", bg="#0000FF", fg="white", command=submit_nilai)
btn_submit.pack(pady=20)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

root.mainloop()