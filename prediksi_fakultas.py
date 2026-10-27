import sqlite3
import tkinter as tk
from tkinter import messagebox

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

    hasil_prediksi = prediksi_fakultas(bio, fis, ing)

    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, bio, fis, ing, hasil_prediksi))
    conn.commit()
    conn.close()

    messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")

    entry_nama.delete(0, tk.END)
    entry_bio.delete(0, tk.END)
    entry_fis.delete(0, tk.END)
    entry_ing.delete(0, tk.END)

def on_enter(e):
    btn_submit["bg"] = "#50fa7b"
    btn_submit["fg"] = "black"

def on_leave(e):
    btn_submit["bg"] = "#44475a"
    btn_submit["fg"] = "white"


root = tk.Tk()
root.title("Sistem Prediksi Fakultas")
root.geometry("400x450")
root.configure(bg="#282a36")


label_nama = tk.Label(root, text="Nama Siswa:", bg="#282a36", fg="white")
label_nama.pack(pady=(15, 2))
entry_nama = tk.Entry(root, width=35)
entry_nama.pack(pady=5)


label_bio = tk.Label(root, text="Nilai Biologi:", bg="#282a36", fg="white")
label_bio.pack(pady=(10, 2))
entry_bio = tk.Entry(root, width=35)
entry_bio.pack(pady=5)


label_fis = tk.Label(root, text="Nilai Fisika:", bg="#282a36", fg="white")
label_fis.pack(pady=(10, 2))
entry_fis = tk.Entry(root, width=35)
entry_fis.pack(pady=5)


label_ing = tk.Label(root, text="Nilai Bahasa Inggris:", bg="#282a36", fg="white")
label_ing.pack(pady=(10, 2))
entry_ing = tk.Entry(root, width=35)
entry_ing.pack(pady=5)

btn_submit = tk.Button(
    root, 
    text="Submit Nilai", 
    command=submit_nilai, 
    bg="#44475a", 
    fg="white", 
    font=("Arial", 10, "bold"),
    padx=10, 
    pady=5
)
btn_submit.pack(pady=20)

btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

root.mainloop()