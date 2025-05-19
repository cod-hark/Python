import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# --- CONFIGURACIÓN DE ARCHIVOS ---
BASE_DIR = "datos_restaurante"
INGREDIENTES_FILE = os.path.join(BASE_DIR, "ingredientes.txt")
RECETAS_FILE = os.path.join(BASE_DIR, "recetas.txt")
RELACIONES_FILE = os.path.join(BASE_DIR, "relaciones.txt")
GASTOS_FILE = os.path.join(BASE_DIR, "gastos.txt")

# --- INICIALIZACIÓN ---
def inicializar_archivos():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    for archivo in [INGREDIENTES_FILE, RECETAS_FILE, RELACIONES_FILE, GASTOS_FILE]:
        if not os.path.exists(archivo):
            with open(archivo, "w") as f:
                json.dump([], f)

# --- FUNCIONES AUXILIARES ---
def cargar_datos(archivo):
    with open(archivo, "r") as f:
        return json.load(f)

def guardar_datos(archivo, datos):
    with open(archivo, "w") as f:
        json.dump(datos, f, indent=4)

# --- CLASE PRINCIPAL ---
class RestauranteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Restaurante")

        # MENÚ PRINCIPAL
        self.frame_menu = tk.Frame(self.root, padx=20, pady=20)
        self.frame_menu.pack()

        tk.Label(self.frame_menu, text="Menú Principal", font=("Arial", 18, "bold")).pack()

        tk.Button(self.frame_menu, text="Añadir Ingrediente", command=self.abrir_ventana_ingredientes, width=30).pack(pady=5)
        tk.Button(self.frame_menu, text="Añadir Receta", command=self.abrir_ventana_recetas, width=30).pack(pady=5)
        tk.Button(self.frame_menu, text="Añadir Gastos", command=self.abrir_ventana_gastos, width=30).pack(pady=5)
        tk.Button(self.frame_menu, text="Relacionar Receta e Ingrediente", command=self.abrir_ventana_relaciones, width=30).pack(pady=5)
        tk.Button(self.frame_menu, text="Calcular Precio Final", command=self.abrir_ventana_calculos, width=30).pack(pady=5)
        tk.Button(self.frame_menu, text="Salir", command=self.root.quit, width=30).pack(pady=5)

    # --- VENTANA INGREDIENTES ---
    def abrir_ventana_ingredientes(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Añadir Ingredientes")

        # Mostrar ingredientes existentes
        ingredientes = cargar_datos(INGREDIENTES_FILE)
        lista_ingredientes = ttk.Treeview(ventana, columns=("Nombre", "Unidad", "Precio", "Stock"), show="headings")
        lista_ingredientes.heading("Nombre", text="Nombre")
        lista_ingredientes.heading("Unidad", text="Unidad")
        lista_ingredientes.heading("Precio", text="Precio/Unidad")
        lista_ingredientes.heading("Stock", text="Stock")
        lista_ingredientes.pack()

        for ing in ingredientes:
            lista_ingredientes.insert("", "end", values=(ing["nombre"], ing["unidad_medida"], ing["precio_unitario"], ing["stock_actual"]))

        # Formulario para añadir ingredientes
        tk.Label(ventana, text="Nombre:").pack()
        nombre = tk.Entry(ventana)
        nombre.pack()

        tk.Label(ventana, text="Unidad de Medida (kg, litro, etc):").pack()
        unidad = tk.Entry(ventana)
        unidad.pack()

        tk.Label(ventana, text="Precio por Unidad:").pack()
        precio = tk.Entry(ventana)
        precio.pack()

        tk.Label(ventana, text="Stock Actual:").pack()
        stock = tk.Entry(ventana)
        stock.pack()

        def agregar_ingrediente():
            nuevo_ingrediente = {
                "nombre": nombre.get(),
                "unidad_medida": unidad.get(),
                "precio_unitario": float(precio.get()),
                "stock_actual": float(stock.get())
            }
            ingredientes.append(nuevo_ingrediente)
            guardar_datos(INGREDIENTES_FILE, ingredientes)
            lista_ingredientes.insert("", "end", values=(nombre.get(), unidad.get(), precio.get(), stock.get()))
            messagebox.showinfo("Éxito", f"Ingrediente '{nombre.get()}' añadido correctamente.")

        tk.Button(ventana, text="Añadir Ingrediente", command=agregar_ingrediente).pack(pady=10)

    # --- VENTANA RECETAS ---
    def abrir_ventana_recetas(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Añadir Recetas")

        # Mostrar recetas existentes
        recetas = cargar_datos(RECETAS_FILE)
        lista_recetas = ttk.Treeview(ventana, columns=("Nombre", "Instrucciones"), show="headings")
        lista_recetas.heading("Nombre", text="Nombre")
        lista_recetas.heading("Instrucciones", text="Instrucciones")
        lista_recetas.pack()

        for rec in recetas:
            lista_recetas.insert("", "end", values=(rec["nombre"], rec["instrucciones"]))

        # Formulario para añadir recetas
        tk.Label(ventana, text="Nombre de la Receta:").pack()
        nombre = tk.Entry(ventana)
        nombre.pack()

        tk.Label(ventana, text="Instrucciones:").pack()
        instrucciones = tk.Entry(ventana)
        instrucciones.pack()

        def agregar_receta():
            nueva_receta = {
                "nombre": nombre.get(),
                "instrucciones": instrucciones.get()
            }
            recetas.append(nueva_receta)
            guardar_datos(RECETAS_FILE, recetas)
            lista_recetas.insert("", "end", values=(nombre.get(), instrucciones.get()))
            messagebox.showinfo("Éxito", f"Receta '{nombre.get()}' añadida correctamente.")

        tk.Button(ventana, text="Añadir Receta", command=agregar_receta).pack(pady=10)


    # --- VENTANA RELACIONES ---
    def abrir_ventana_relaciones(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Relacionar Receta con Ingrediente")

        # Mostrar relaciones existentes
        relaciones = cargar_datos(RELACIONES_FILE)
        lista_relaciones = ttk.Treeview(ventana, columns=("Receta", "Ingrediente", "Cantidad"), show="headings")
        lista_relaciones.heading("Receta", text="Receta")
        lista_relaciones.heading("Ingrediente", text="Ingrediente")
        lista_relaciones.heading("Cantidad", text="Cantidad")
        lista_relaciones.pack()

        for rel in relaciones:
            lista_relaciones.insert("", "end", values=(rel["receta"], rel["ingrediente"], rel["cantidad"]))

        # Cargar recetas e ingredientes existentes
        recetas = cargar_datos(RECETAS_FILE)
        ingredientes = cargar_datos(INGREDIENTES_FILE)

        tk.Label(ventana, text="Seleccione una Receta:").pack()
        combo_recetas = ttk.Combobox(ventana, values=[r["nombre"] for r in recetas])
        combo_recetas.pack()

        tk.Label(ventana, text="Seleccione un Ingrediente:").pack()
        combo_ingredientes = ttk.Combobox(ventana, values=[i["nombre"] for i in ingredientes])
        combo_ingredientes.pack()

        tk.Label(ventana, text="Cantidad del Ingrediente:").pack()
        cantidad = tk.Entry(ventana)
        cantidad.pack()

        # Función para guardar la relación
        def agregar_relacion():
            nueva_relacion = {
                "receta": combo_recetas.get(),
                "ingrediente": combo_ingredientes.get(),
                "cantidad": float(cantidad.get())
            }
            relaciones.append(nueva_relacion)
            guardar_datos(RELACIONES_FILE, relaciones)
            lista_relaciones.insert("", "end", values=(combo_recetas.get(), combo_ingredientes.get(), cantidad.get()))
            messagebox.showinfo("Éxito", "Relación añadida correctamente.")

        tk.Button(ventana, text="Añadir Relación", command=agregar_relacion).pack(pady=10)



    # --- VENTANA GASTOS ---
    def abrir_ventana_gastos(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Añadir Gastos")

        # Mostrar gastos existentes
        gastos = cargar_datos(GASTOS_FILE)
        lista_gastos = ttk.Treeview(ventana, columns=("Tipo", "Monto"), show="headings")
        lista_gastos.heading("Tipo", text="Tipo")
        lista_gastos.heading("Monto", text="Monto")
        lista_gastos.pack()

        for g in gastos:
            lista_gastos.insert("", "end", values=(g["tipo"], g["monto"]))

        # Formulario para añadir gastos
        tk.Label(ventana, text="Tipo de Gasto (Semanal/Mensual):").pack()
        tipo = tk.Entry(ventana)
        tipo.pack()

        tk.Label(ventana, text="Monto:").pack()
        monto = tk.Entry(ventana)
        monto.pack()

        def agregar_gasto():
            nuevo_gasto = {"tipo": tipo.get(), "monto": float(monto.get())}
            gastos.append(nuevo_gasto)
            guardar_datos(GASTOS_FILE, gastos)
            lista_gastos.insert("", "end", values=(tipo.get(), monto.get()))
            messagebox.showinfo("Éxito", f"Gasto '{tipo.get()}' añadido correctamente.")

        tk.Button(ventana, text="Añadir Gasto", command=agregar_gasto).pack(pady=10)


    # --- VENTANA CALCULAR PRECIO FINAL ---
    def abrir_ventana_calculos(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Calcular Precio Final de una Receta")

        # Mostrar recetas existentes
        recetas = cargar_datos(RECETAS_FILE)
        tk.Label(ventana, text="Seleccione una Receta:").pack()
        combo_recetas = ttk.Combobox(ventana, values=[r["nombre"] for r in recetas])
        combo_recetas.pack()

        # Mostrar gastos semanales y mensuales
        gastos = cargar_datos(GASTOS_FILE)
        gasto_semanal = sum(g["monto"] for g in gastos if g["tipo"] == "semanal")
        gasto_mensual = sum(g["monto"] for g in gastos if g["tipo"] == "mensual")

        tk.Label(ventana, text=f"Gastos Semanales: ${gasto_semanal}").pack()
        tk.Label(ventana, text=f"Gastos Mensuales: ${gasto_mensual}").pack()

        resultado_label = tk.Label(ventana, text="", fg="blue")
        resultado_label.pack()

        # Función para calcular el precio final
        def calcular_precio():
            receta = combo_recetas.get()
            costo_receta = calcular_costo_receta(receta)
            costo_total = costo_receta + (gasto_semanal / 4) + (gasto_mensual / 4)
            precio_final = costo_total + (costo_total * 0.3)  # 30% de ganancia
            resultado_label.config(
                text=f"Costo Base: ${costo_receta}\nCosto Total: ${costo_total:.2f}\nPrecio Final: ${precio_final:.2f}"
            )

        tk.Button(ventana, text="Calcular Precio Final", command=calcular_precio).pack(pady=10)

    # --- FUNCIONES PARA GASTOS ---
    def abrir_ventana_gastos(self):
        ventana = tk.Toplevel(self.root)
        ventana.title("Gestionar Gastos")

        gastos = cargar_datos(GASTOS_FILE)

        # Mostrar gastos existentes
        lista_gastos = ttk.Treeview(ventana, columns=("Tipo", "Descripción", "Monto"), show="headings")
        lista_gastos.heading("Tipo", text="Tipo")
        lista_gastos.heading("Descripción", text="Descripción")
        lista_gastos.heading("Monto", text="Monto")
        lista_gastos.pack()

        for gasto in gastos:
            lista_gastos.insert("", "end", values=(gasto["tipo"], gasto["descripcion"], gasto["monto"]))

        # Campos para agregar nuevos gastos
        tk.Label(ventana, text="Tipo de Gasto (semanal/mensual):").pack()
        tipo = ttk.Combobox(ventana, values=["semanal", "mensual"])
        tipo.pack()

        tk.Label(ventana, text="Descripción:").pack()
        descripcion = tk.Entry(ventana)
        descripcion.pack()

        tk.Label(ventana, text="Monto:").pack()
        monto = tk.Entry(ventana)
        monto.pack()

        # Función para guardar un gasto
        def agregar_gasto():
            nuevo_gasto = {
                "tipo": tipo.get(),
                "descripcion": descripcion.get(),
                "monto": float(monto.get())
            }
            gastos.append(nuevo_gasto)
            guardar_datos(GASTOS_FILE, gastos)
            lista_gastos.insert("", "end", values=(tipo.get(), descripcion.get(), monto.get()))
            messagebox.showinfo("Éxito", "Gasto añadido correctamente.")

        tk.Button(ventana, text="Agregar Gasto", command=agregar_gasto).pack(pady=10)


# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    inicializar_archivos()
    root = tk.Tk()
    app = RestauranteApp(root)
    root.mainloop()
