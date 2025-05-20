import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
import sqlite3

# === CONFIGURACIÓN DE LA APP ===
class PeluqueriaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lana Estilismo Canino")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.theme = "flatly"  # por defecto: claro
        self.style = Style(theme=self.theme)

        self.conn = sqlite3.connect("peluqueria_canina.db")
        self.cursor = self.conn.cursor()

        self._build_gui()

    def _build_gui(self):
        # Frame lateral (navegación)
        self.menu_frame = ttk.Frame(self, padding=10)
        self.menu_frame.pack(side="left", fill="y")

        ttk.Label(self.menu_frame, text="Menú", font=("Segoe UI", 14, "bold")).pack(pady=10)

        self.btn_cliente = ttk.Button(self.menu_frame, text="📋 Ver Clientes", command=self.ver_clientes)
        self.btn_cliente.pack(fill="x", pady=5)

        self.btn_nuevo = ttk.Button(self.menu_frame, text="➕ Añadir Cliente", command=self.anadir_cliente)
        self.btn_nuevo.pack(fill="x", pady=5)

        self.btn_visitas = ttk.Button(self.menu_frame, text="📅 Historial Visitas", command=self.historial_visitas)
        self.btn_visitas.pack(fill="x", pady=5)

        self.btn_config = ttk.Button(self.menu_frame, text="⚙️ Configuración", command=self.configuracion)
        self.btn_config.pack(fill="x", pady=5)

        # Frame principal (contenido dinámico)
        self.content_frame = ttk.Frame(self, padding=20)
        self.content_frame.pack(side="right", expand=True, fill="both")
        self.actualizar_contenido("Bienvenido a Lana Estilismo Canino")

    def actualizar_contenido(self, texto):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        label = ttk.Label(self.content_frame, text=texto, font=("Segoe UI", 16))
        label.pack(pady=20)

    def ver_clientes(self):
        self.actualizar_contenido("Aquí iría la tabla de clientes...")

    def anadir_cliente(self):
        self.actualizar_contenido("Formulario para añadir cliente...")

    def historial_visitas(self):
        self.actualizar_contenido("Historial de servicios/visitas...")

    def configuracion(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ttk.Label(self.content_frame, text="Configuración", font=("Segoe UI", 16)).pack(pady=10)
        ttk.Label(self.content_frame, text="Seleccionar tema:").pack(pady=5)

        temas = ["flatly", "superhero", "darkly", "morph", "solar", "journal"]

        combo = ttk.Combobox(self.content_frame, values=temas)
        combo.set(self.theme)
        combo.pack(pady=10)

        def cambiar_tema():
            nuevo_tema = combo.get()
            self.theme = nuevo_tema
            self.style.theme_use(nuevo_tema)

        ttk.Button(self.content_frame, text="Aplicar Tema", command=cambiar_tema).pack(pady=10)

if __name__ == "__main__":
    app = PeluqueriaApp()
    app.mainloop()
