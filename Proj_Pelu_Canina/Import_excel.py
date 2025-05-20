import pandas as pd
import sqlite3
from datetime import datetime
import re

# === Configuración ===
excel_path = r"D:\nerea\Base de datos Lana Estilismo Canino.xlsx"

db_path = "peluqueria_canina.db"

# === Conectar a la base de datos SQLite ===
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# === Leer el Excel ===
df = pd.read_excel(excel_path, sheet_name="BASE DE DATOS")

# === Limpieza y normalización ===
df = df.dropna(subset=["Nombre del dueño", "Nombre perro"])
df["Teléfono"] = df["Teléfono"].astype(str).str.extract(r'(\d{6,})')  # extrae solo el primer número válido
df["Fecha última visita"] = pd.to_datetime(df["Fecha última visita"], errors='coerce')

# === Diccionario para rastrear IDs creados ===
cliente_id_map = {}

# === Funcíon para interpretar edad ===
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
            return max(1, numero // 12)  # convertir meses a años (redondeado abajo)
        else:
            return numero
    return None

for _, row in df.iterrows():
    nombre_cliente = row["Nombre del dueño"].strip()
    telefono = row["Teléfono"] if pd.notna(row["Teléfono"]) else None
    localidad = row["LOCALIDAD"] if pd.notna(row["LOCALIDAD"]) else None
    correo = row["Correo electrónico"] if pd.notna(row["Correo electrónico"]) else None

    clave_unica = (nombre_cliente, telefono)

    # === Insertar CLIENTE si no existe ===
    if clave_unica not in cliente_id_map:
        cursor.execute("""
            INSERT INTO clientes (nombre, telefono, email, localidad)
            VALUES (?, ?, ?, ?)
        """, (nombre_cliente, telefono, correo, localidad))
        cliente_id = cursor.lastrowid
        cliente_id_map[clave_unica] = cliente_id
    else:
        cliente_id = cliente_id_map[clave_unica]

    # === Insertar MASCOTA ===
    nombre_mascota = row["Nombre perro"].strip()
    raza = row["Raza perro"] if pd.notna(row["Raza perro"]) else None
    edad = interpretar_edad(row["Edad perro"])
    problemas = row["Problemas"] if pd.notna(row["Problemas"]) else None

    cursor.execute("""
        INSERT INTO mascotas (id_cliente, nombre, raza, edad, problemas)
        VALUES (?, ?, ?, ?, ?)
    """, (cliente_id, nombre_mascota, raza, edad, problemas))
    mascota_id = cursor.lastrowid

    # === Insertar SERVICIO (si hay fecha o tipo de servicio) ===
    fecha_visita = row["Fecha última visita"]
    tipo_servicio = row["Servicio realizado"] if pd.notna(row["Servicio realizado"]) else "Corte"
    observaciones = row["Observaciones"] if pd.notna(row["Observaciones"]) else None

    if not pd.isna(fecha_visita):
        cursor.execute("""
            INSERT INTO servicios (id_mascota, fecha, tipo_servicio, observaciones)
            VALUES (?, ?, ?, ?)
        """, (mascota_id, fecha_visita.strftime("%Y-%m-%d"), tipo_servicio, observaciones))

# === Guardar y cerrar ===
conn.commit()
conn.close()

print("Datos importados correctamente a la base de datos.")
