import sqlite3
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap import Style
from tkinter import ttk
import tkinter as tk
from datetime import datetime
from tkcalendar import Calendar

# === Configuración ===
db_path = "peluqueria_canina.db"

# === Conectar a la base de datos ===
def obtener_estadisticas():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM clientes")
    total_clientes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM mascotas")
    total_mascotas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM servicios")
    total_servicios = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(DISTINCT id_mascota) FROM servicios")
    mascotas_atendidas = cursor.fetchone()[0]

    conn.close()
    return total_clientes, total_mascotas, total_servicios, mascotas_atendidas

# === Función para cambiar de contenido ===
def mostrar_contenido(frame):
    for widget in contenido_frame.winfo_children():
        widget.destroy()
    frame()

# === Función calendario separado ===
def abrir_calendario():
    top = tk.Toplevel(app)
    top.title("Calendario de Citas")
    cal = Calendar(top, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    cal.pack(padx=10, pady=10)

# === Vistas ===
def vista_dashboard():
    total_clientes, total_mascotas, total_servicios, mascotas_atendidas = obtener_estadisticas()

    ttk.Label(contenido_frame, text="Panel de Control", font=("Segoe UI", 18, "bold")).pack(pady=10)

    stats_frame = ttk.Frame(contenido_frame)
    stats_frame.pack(pady=10)

    tb.Label(stats_frame, text=f"Clientes registrados: {total_clientes}", font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=5)
    tb.Label(stats_frame, text=f"Mascotas registradas: {total_mascotas}", font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=5)
    tb.Label(stats_frame, text=f"Visitas totales: {total_servicios}", font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=5)
    tb.Label(stats_frame, text=f"Mascotas atendidas: {mascotas_atendidas}", font=("Segoe UI", 12)).pack(anchor="w", padx=10, pady=5)

    tb.Button(contenido_frame, text="Abrir Calendario", command=abrir_calendario, bootstyle=PRIMARY).pack(pady=10)


def vista_clientes():
    ttk.Label(contenido_frame, text="Gestión de Clientes", font=("Segoe UI", 18, "bold")).pack(pady=10)

    def cargar_clientes():
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id_cliente, nombre, telefono FROM clientes")
        for cliente in cursor.fetchall():
            tree.insert("", "end", values=cliente)
        conn.close()

    busqueda = tk.StringVar()
    tk.Entry(contenido_frame, textvariable=busqueda).pack(pady=5)

    tree = ttk.Treeview(contenido_frame, columns=("ID Cliente", "Nombre", "Teléfono"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)

    def buscar():
        texto = busqueda.get().lower()
        for row in tree.get_children():
            valores = tree.item(row, "values")
            if texto in str(valores).lower():
                tree.selection_set(row)
                tree.see(row)

    tb.Button(contenido_frame, text="Buscar", command=buscar, bootstyle=INFO).pack(pady=5)

    cargar_clientes()


def vista_mascotas():
    ttk.Label(contenido_frame, text="Gestión de Mascotas", font=("Segoe UI", 18, "bold")).pack(pady=10)

    def cargar_mascotas():
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id_mascota, nombre, especie, raza, id_cliente FROM mascotas")
        for mascota in cursor.fetchall():
            tree.insert("", "end", values=mascota)
        conn.close()

    tree = ttk.Treeview(contenido_frame, columns=("ID Mascota", "Nombre", "Especie", "Raza", "ID Cliente"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    cargar_mascotas()


def vista_servicios():
    ttk.Label(contenido_frame, text="Historial de Servicios", font=("Segoe UI", 18, "bold")).pack(pady=10)

    def cargar_servicios():
        for row in tree.get_children():
            tree.delete(row)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id_servicio, id_mascota, fecha, descripcion FROM servicios")
        for servicio in cursor.fetchall():
            tree.insert("", "end", values=servicio)
        conn.close()

    tree = ttk.Treeview(contenido_frame, columns=("ID Servicio", "ID Mascota", "Fecha", "Descripción"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
    tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
    cargar_servicios()


def vista_configuracion():
    ttk.Label(contenido_frame, text="Configuración", font=("Segoe UI", 18, "bold")).pack(pady=10)

    temas = ["flatly", "darkly", "cyborg", "superhero", "morph"]
    tema_var = tk.StringVar(value=app.style.theme.name)

    def aplicar_tema():
        app.style.theme_use(tema_var.get())

    tb.Label(contenido_frame, text="Selecciona un tema:", font=("Segoe UI", 12)).pack(pady=5)
    tema_combo = ttk.Combobox(contenido_frame, values=temas, textvariable=tema_var, state="readonly")
    tema_combo.pack(pady=5)
    tb.Button(contenido_frame, text="Aplicar Tema", command=aplicar_tema, bootstyle=SUCCESS).pack(pady=10)

# === Interfaz principal ===
app = tb.Window(themename="flatly")
app.title("Lana Estilismo Canino")
app.geometry("1000x600")

# Layout general
frame_lateral = tb.Frame(app, padding=10)
frame_lateral.pack(side=LEFT, fill=Y)

contenido_frame = tb.Frame(app, padding=20)
contenido_frame.pack(side=RIGHT, expand=YES, fill=BOTH)

# Menú lateral
botones = [
    ("Inicio", vista_dashboard),
    ("Clientes", vista_clientes),
    ("Mascotas", vista_mascotas),
    ("Servicios", vista_servicios),
    ("Configuración", vista_configuracion),
]

for texto, comando in botones:
    tb.Button(frame_lateral, text=texto, width=20, command=lambda c=comando: mostrar_contenido(c), bootstyle=SECONDARY).pack(pady=5)

# Cargar dashboard al inicio
vista_dashboard()

app.mainloop()
