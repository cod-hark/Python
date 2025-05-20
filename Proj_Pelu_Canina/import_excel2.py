import pandas as pd
import sqlite3
from datetime import datetime
import re
import os

# === Configuración ===
excel_path = r"D:\nerea\Base de datos Lana Estilismo Canino.xlsx"
db_path = "peluqueria_canina2.db"

# Verificar que el archivo existe
if not os.path.exists(excel_path):
    raise FileNotFoundError(f"No se encontró el archivo en: {excel_path}")

# === Conectar a la base de datos SQLite ===
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# === Crear tablas si no existen ===
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT,
    localidad TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS mascotas (
    id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    nombre TEXT NOT NULL,
    raza TEXT,
    edad INTEGER,
    problemas TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS servicios (
    id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
    id_mascota INTEGER NOT NULL,
    fecha TEXT NOT NULL,
    tipo_servicio TEXT,
    observaciones TEXT,
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota)
)
""")

# === Leer el Excel ===
df = pd.read_excel(excel_path, sheet_name="BASE DE DATOS")
df.columns = df.columns.str.strip()  # limpiar nombres de columnas

# === Limpieza y normalización ===
df = df.dropna(subset=["Nombre del dueño", "Nombre perro"])
df["Teléfono"] = df["Teléfono"].astype(str).str.extract(r'(\d{6,})')
df["Fecha última visita"] = pd.to_datetime(df["Fecha última visita"], errors='coerce')

# === Función para interpretar edad ===
def interpretar_edad(valor):
    if pd.isna(valor):
        return None
    texto = str(valor).strip().lower()
    if texto.isdigit():
        return int(texto)
    match = re.search(r'(\d+)', texto)
    if match:
        numero = int(match.group(1))
        if "mes" in texto:
            return max(1, numero // 12)
        return numero
    return None

# === Inicializar contadores ===
clientes_insertados = 0
mascotas_insertadas = 0
servicios_insertados = 0
clientes_omitidos = []

# === Diccionario para rastrear IDs de clientes ===
cliente_id_map = {}

# === Insertar datos ===
for _, row in df.iterrows():
    try:
        nombre_cliente = str(row["Nombre del dueño"]).strip().lower()
        telefono = row["Teléfono"] if pd.notna(row["Teléfono"]) else None
        localidad = row["LOCALIDAD"] if pd.notna(row["LOCALIDAD"]) else None
        correo = row["Correo electrónico"] if pd.notna(row["Correo electrónico"]) else None

        clave_unica = (nombre_cliente, telefono)

        # Insertar CLIENTE si no existe
        if clave_unica not in cliente_id_map:
            cursor.execute("""
                INSERT INTO clientes (nombre, telefono, email, localidad)
                VALUES (?, ?, ?, ?)
            """, (nombre_cliente, telefono, correo, localidad))
            cliente_id = cursor.lastrowid
            cliente_id_map[clave_unica] = cliente_id
            clientes_insertados += 1
        else:
            cliente_id = cliente_id_map[clave_unica]

        # Manejar múltiples mascotas
        nombres_mascotas = str(row["Nombre perro"]).replace(" y ", "/").replace(",", "/").split("/")

        for nombre_mascota in nombres_mascotas:
            nombre_mascota = nombre_mascota.strip()
            if not nombre_mascota:
                continue

            raza = row["Raza perro"] if pd.notna(row["Raza perro"]) else None
            edad = interpretar_edad(row["Edad perro"])
            problemas = row["Problemas"] if pd.notna(row["Problemas"]) else None

            cursor.execute("""
                INSERT INTO mascotas (id_cliente, nombre, raza, edad, problemas)
                VALUES (?, ?, ?, ?, ?)
            """, (cliente_id, nombre_mascota, raza, edad, problemas))
            mascota_id = cursor.lastrowid
            mascotas_insertadas += 1

            # Insertar SERVICIO (si hay fecha)
            fecha_visita = row["Fecha última visita"]
            tipo_servicio = row["Servicio realizado"] if pd.notna(row["Servicio realizado"]) else "Corte"
            observaciones = row["Observaciones"] if pd.notna(row["Observaciones"]) else None

            if not pd.isna(fecha_visita):
                cursor.execute("""
                    INSERT INTO servicios (id_mascota, fecha, tipo_servicio, observaciones)
                    VALUES (?, ?, ?, ?)
                """, (mascota_id, fecha_visita.strftime("%Y-%m-%d"), tipo_servicio, observaciones))
                servicios_insertados += 1

    except Exception as e:
        clientes_omitidos.append(row.to_dict())
        print(f"ERROR en fila: {row.to_dict()}\n  -> {e}")

# === Guardar y cerrar ===
conn.commit()
conn.close()

# === Mostrar resumen ===
print("\n✔️ Importación completada")
print(f"Clientes insertados: {clientes_insertados}")
print(f"Mascotas insertadas: {mascotas_insertadas}")
print(f"Servicios insertados: {servicios_insertados}")
if clientes_omitidos:
    print(f"❗ Clientes con error: {len(clientes_omitidos)} (ver consola para detalles)")
