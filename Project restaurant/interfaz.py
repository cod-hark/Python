import tkinter as tk
from tkinter import messagebox

def registrar_ingrediente():
    nombre = entry_nombre.get()
    precio = float(entry_precio.get())
    # Llamar a la función agregar_ingrediente()
    messagebox.showinfo("Registro", f"Ingrediente '{nombre}' registrado correctamente.")

root = tk.Tk()
root.title("Gestión de Ingredientes")

tk.Label(root, text="Nombre:").grid(row=0, column=0)
entry_nombre = tk.Entry(root)
entry_nombre.grid(row=0, column=1)

tk.Label(root, text="Precio unitario:").grid(row=1, column=0)
entry_precio = tk.Entry(root)
entry_precio.grid(row=1, column=1)

tk.Button(root, text="Registrar", command=registrar_ingrediente).grid(row=2, columnspan=2)

root.mainloop()
