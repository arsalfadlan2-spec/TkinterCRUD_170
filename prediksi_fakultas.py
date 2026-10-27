import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_database():
    conn = sqlite3.connect('fakultas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fakultas (
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

def tampilkan_data():
    for item in tabel.get_children():
        tabel.delete(item)

    conn = sqlite3.connect("fakultas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fakultas")