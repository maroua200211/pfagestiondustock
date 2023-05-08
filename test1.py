import tkinter as tk
import sqlite3
from tkinter import messagebox
import sys
sys.path.append('C:\\Users\\Imane\\Downloads\\test1\\test1')

import chambre

database="database.db"
conn=sqlite3.connect(database)

cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Utilisateur (
                    IdUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
                    NomUtilisateur NVARCHAR(50) NOT NULL,
                    password NVARCHAR(50) NOT NULL)

                """)


def open_login_window():
    login_window = tk.Toplevel(root)
    login_window.title("Connexion")
    login_window.geometry("300x200")
    login_window.configure(bg="#F5DEB3")
    username_label = tk.Label(login_window, text="Nom d'utilisateur:", bg="#F5DEB3", font=("Arial", 12))
    username_label.pack(pady=10)
    username_entry = tk.Entry(login_window, width=30)
    username_entry.pack(pady=5)
    password_label = tk.Label(login_window, text="Mot de passe:", bg="#F5DEB3", font=("Arial", 12))
    password_label.pack()
    password_entry = tk.Entry(login_window, width=30, show="*")
    password_entry.pack(pady=5)
    login_button = tk.Button(login_window, text="Connexion", bg="#F5DEB3", font=("Arial", 12), width=10, command=lambda : login(username_entry, password_entry))
    login_button.pack(pady=10)


def open_register_window():
    register_window = tk.Toplevel(root)
    register_window.title("Inscription")
    register_window.geometry("300x200")
    register_window.configure(bg="#F5DEB3")
    username_label = tk.Label(register_window, text="Nom d'utilisateur:", bg="#F5DEB3", font=("Arial", 12))
    username_label.pack(pady=10)
    username_entry = tk.Entry(register_window, width=30)
    username_entry.pack(pady=5)
    password_label = tk.Label(register_window, text="Mot de passe:", bg="#F5DEB3", font=("Arial", 12))
    password_label.pack()
    password_entry = tk.Entry(register_window, width=30, show="*")
    password_entry.pack(pady=5)
    register_button = tk.Button(register_window, text="Inscription", bg="#F5DEB3", font=("Arial", 12), width=10 , command=lambda : register(username_entry, password_entry))
    register_button.pack(pady=10)


root = tk.Tk()
root.title("Ma super application")
root.geometry("400x300")
root.configure(bg="#F5DEB3")
title_label = tk.Label(root, text="Bienvenue !", bg="#F5DEB3", font=("Arial", 20, "italic"))
title_label.pack(pady=50)
button_frame = tk.Frame(root, bg="#F5DEB3")
button_frame.pack(pady=20)
login_button = tk.Button(button_frame, text="Connexion", bg="#FFFACD", font=("Arial", 14), width=10, command=open_login_window)
login_button.pack(side=tk.RIGHT, padx=10)
register_button = tk.Button(button_frame, text="Inscription", bg="#FFFACD", font=("Arial", 14), width=10, command=open_register_window)
register_button.pack(side=tk.LEFT, padx=10)

def register(username_entry, password_entry):
    cursor=conn.cursor()
    username=username_entry.get()
    password=password_entry.get()
    try:
        cursor.execute("INSERT INTO Utilisateur(nomutilisateur, password) VALUES (? , ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Info", "utilisateur enregistré avec succes")
    except Exception as e:
        messagebox.showinfo("info", f"enregistrement utilisateur echoue {str(e)}")

def login(username_entry, password_entry):
    username=username_entry.get()
    password=password_entry.get()

    cursor=conn.cursor()
    cursor.execute("SELECT * FROM UTILISATEUR WHERE NOMUTILISATEUR=? and password = ?", (username, password))
    existe=cursor.fetchall()
    if not existe:
        messagebox.showinfo("info", "username et password errones")
    else:
        root.destroy()
        chambre.chambre_window()



root.mainloop()
