import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk



database="database.db"
conn=sqlite3.connect("stock.db")

cursor = conn.cursor()


cursor.execute("""CREATE TABLE IF NOT EXISTS PRODUIT (IdProduit INTEGER  PRIMARY KEY AUTOINCREMENT,
    NomProduit NVARCHAR(50) ,
    DescriptionProduit NVARCHAR(100),
    PrixUnitaire DECIMAL(10,2) ,
    StockActuel INT,
    IdCategorie INT ,
    Sdalert int ,
    DDE date ,
    DDS date ,
    imgp BLOB
)""")
conn.commit()


def chambre_window():
    # création de la fenêtre principale
    root = tk.Tk()
    root.title("Gestion de stock")
    root.geometry("800x600")
    root.config(bg="#f5f5dc")

    # création des labels pour les attributs du produit
    name_label = ttk.Label(root, text="Nom:")
    name_label.grid(column=0, row=0, padx=10, pady=10, sticky="w")

    description_label = ttk.Label(root, text="Description:")
    description_label.grid(column=0, row=1, padx=10, pady=10, sticky="w")

    price_label = ttk.Label(root, text="Prix unitaire:")
    price_label.grid(column=0, row=2, padx=10, pady=10, sticky="w")

    quantity_label = ttk.Label(root, text="Quantité en stock:")
    quantity_label.grid(column=0, row=3, padx=10, pady=10, sticky="w")

    alert_label = ttk.Label(root, text="Seuil d'alerte de stock:")
    alert_label.grid(column=0, row=4, padx=10, pady=10, sticky="w")

    last_entry_label = ttk.Label(root, text="Date de dernière entrée en stock:")
    last_entry_label.grid(column=0, row=5, padx=10, pady=10, sticky="w")

    last_exit_label = ttk.Label(root, text="Date de dernière sortie de stock:")
    last_exit_label.grid(column=0, row=6, padx=10, pady=10, sticky="w")

    image_label = ttk.Label(root, text="Image du produit:")
    image_label.grid(column=0, row=7, padx=10, pady=10, sticky="w")

    # création des entrées pour les attributs du produit
    name_entry = ttk.Entry(root)
    name_entry.grid(column=1, row=0, padx=10, pady=10, sticky="w")
    description_entry = ttk.Entry(root)
    description_entry.grid(column=1, row=1, padx=10, pady=10, sticky="w")
    price_entry = ttk.Entry(root)
    price_entry.grid(column=1, row=2, padx=10, pady=10, sticky="w")
    quantity_entry = ttk.Entry(root)
    quantity_entry.grid(column=1, row=3, padx=10, pady=10, sticky="w")
    alert_entry = ttk.Entry(root)
    alert_entry.grid(column=1, row=4, padx=10, pady=10, sticky="w")
    last_entry_entry = ttk.Entry(root)
    last_entry_entry.grid(column=1, row=5, padx=10, pady=10, sticky="w")
    last_exit_entry = ttk.Entry(root)
    last_exit_entry.grid(column=1, row=6, padx=10, pady=10, sticky="w")
    image_entry = ttk.Entry(root)
    image_entry.grid(column=1, row=7, padx=10, pady=10, sticky="w")
    def browse_image():
        filename = filedialog.askopenfilename()
        image_entry.delete(0, "end")
        image_entry.insert(0, filename)

    browse_button = ttk.Button(root, text="Browse", command=browse_image)
    browse_button.grid(column=2, row=7, padx=10, pady=10)

    search_entry = ttk.Entry(root,width=20, font=("bold", 14))
    # création des boutons
    add_button = ttk.Button(root, text="Ajouter")
    add_button.grid(column=0, row=8, padx=10, pady=  10, sticky="w")
    modify_button = ttk.Button(root, text="Modifier")
    modify_button.grid(column=1, row=8, padx=10, pady=10, sticky="w")
    delete_button = ttk.Button(root, text="Supprimer")
    delete_button.grid(column=2, row=8, padx=10, pady=10, sticky="w")
    search_button = ttk.Button(root, text="Rechercher")
    search_button.grid(column=3, row=8, padx=1, pady=10)
    search_entry.grid(column=4, row=8, padx=0, pady=10)

    # création de la liste pour afficher les produits
    product_list = ttk.Treeview(root)
    product_list["columns"] = ("id", "name", "description", "price", "quantity", "alert", "last_entry", "last_exit", "image")
    product_list.column("#0", width=0, stretch=tk.NO)
    product_list.column("id", anchor=tk.CENTER, width=100)
    product_list.column("name", anchor=tk.CENTER, width=100)
    product_list.column("description", anchor=tk.CENTER, width=150)
    product_list.column("price", anchor=tk.CENTER, width=80)
    product_list.column("quantity", anchor=tk.CENTER, width=100)
    product_list.column("alert", anchor=tk.CENTER, width=100)
    product_list.column("last_entry", anchor=tk.CENTER, width=150)
    product_list.column("last_exit", anchor=tk.CENTER, width=150)
    product_list.column("image", anchor=tk.CENTER, width=150)
    product_list.heading("#0", text="", anchor=tk.CENTER)
    product_list.heading("id", text="Id", anchor=tk.CENTER)
    product_list.heading("name", text="Nom", anchor=tk.CENTER)
    product_list.heading("description", text="Description", anchor=tk.CENTER)
    product_list.heading("price", text="Prix unitaire", anchor=tk.CENTER)
    product_list.heading("quantity", text="Quantité en stock", anchor=tk.CENTER)
    product_list.heading("alert", text="Seuil d'alerte de stock", anchor=tk.CENTER)
    product_list.heading("last_entry", text="Date de dernière entrée en stock", anchor=tk.CENTER)
    product_list.heading("last_exit", text="Date de dernière sortie de stock", anchor=tk.CENTER)
    product_list.heading("image", text="Image du produit", anchor=tk.CENTER)
    product_list.grid(column=0, row=9, columnspan=4, padx=10, pady=10)

    cursor=conn.cursor()
    cursor.execute("SELECT * FROM PRODUIT")
    produits = cursor.fetchall()
    for produit in produits:
        product_list.insert("", "end", text="", values=(produit[0], produit[1],produit[2],produit[3],produit[4], produit[5], produit[6]))

    # fonction pour ajouter un produit à la liste
    def add_product():
        name = name_entry.get()
        description = description_entry.get()
        price = price_entry.get()
        quantity = quantity_entry.get()
        alert = alert_entry.get()
        last_entry = last_entry_entry.get()
        last_exit = last_exit_entry.get()
        image = image_entry.get()
        with open(image, "rb") as f:
            image_data = f.read()
        try:
            cursor=conn.cursor()
            cursor.execute("""INSERT INTO PRODUIT(NomProduit, DescriptionProduit, PrixUnitaire, StockActuel,Sdalert, DDE, DDS, imgp) VALUES(?,?,?,?,?,?,?,?)""",(name,description,price, quantity,alert,last_entry,last_exit,image_data))
            conn.commit()
            id = cursor.lastrowid
            item = (id,name, description, price, quantity, alert, last_entry, last_exit, image)
            product_list.insert("", "end", values=item)
            name_entry.delete(0, "end")
            description_entry.delete(0, "end")
            price_entry.delete(0, "end")
            quantity_entry.delete(0, "end")
            alert_entry.delete(0, "end")
            last_entry_entry.delete(0, "end")
            last_exit_entry.delete(0, "end")
            image_entry.delete(0, "end")
            messagebox.showinfo("Success", "Record added successfully.")

        except:
            messagebox.showinfo("Info", "Données saisies erronées ou non completes!")





    # fonction pour modifier un produit sélectionné dans la liste
    def modify_product():
        selected_item = product_list.selection()[0]
        id = int(product_list.item(selected_item, "values")[0])
        selected = product_list.focus()
        product_list.item(selected, values=(id, name_entry.get(), description_entry.get(), price_entry.get(), quantity_entry.get(), alert_entry.get(), last_entry_entry.get(), last_exit_entry.get(), image_entry.get()))
        with open(image_entry.get(), "rb") as f:
            image_data = f.read()
        cursor=conn.cursor()
        try:
            conn.execute("UPDATE produit SET NomProduit= ?, DescriptionProduit = ? , PrixUnitaire = ?, StockActuel = ? , Sdalert = ?, dde = ?, dds= ?, imgp = ? WHERE IdProduit=? ",(name_entry.get(), description_entry.get(), price_entry.get(), quantity_entry.get(), alert_entry.get(), last_entry_entry.get(), last_exit_entry.get(), image_data,id))
            conn.commit()
            messagebox.showinfo("Success", "Record modified successfully.")

        except:
            messagebox.showinfo("Info", "Données saisies erronées ou non completes!")

    # fonction pour supprimer un produit sélectionné dans la liste
    def delete_product():
        selected_item = product_list.selection()[0]
        id = int(product_list.item(selected_item, "values")[0])
        print(id)
        delete_query = "DELETE FROM produit WHERE IdProduit = ?"
        try:
            conn.execute(delete_query, ((id),))
            conn.commit()
            product_list.delete(selected_item)
            messagebox.showinfo("Success", "Record deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting record: {str(e)}")


    # fonction pour rechercher un produit dans la liste
    def search_product():
        keyword = search_entry.get()
        results = product_list.get_children()
        for result in results:
            values = product_list.item(result)["values"]
            if keyword.lower() in str(values).lower():
                product_list.selection_set(result)
                product_list.focus(result)
            else:
                product_list.selection_remove(result)


    # ajout des fonctions aux boutons
    add_button.config(command=add_product)
    modify_button.config(command=modify_product)
    delete_button.config(command=delete_product)
    search_button.config(command=search_product)

    root.mainloop()

