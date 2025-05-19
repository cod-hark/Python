import sqlite3

# Crear y conectar a la base de datos (se creará un archivo .db en la misma carpeta)
conexion = sqlite3.connect("peluqueria_canina.db")
cursor = conexion.cursor()
# cursor permite ejecutar comandos sql

# Crear tabla CLIENTES
cursor.execute("""
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT,
    localidad TEXT
)
""")

# Crear tabla MASCOTAS
cursor.execute("""
CREATE TABLE IF NOT EXISTS mascotas (
    id_mascota INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER,
    nombre TEXT NOT NULL,
    raza TEXT,
    edad INTEGER,
    problemas TEXT,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
)
""")

# Crear tabla SERVICIOS
cursor.execute("""
CREATE TABLE IF NOT EXISTS servicios (
    id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
    id_mascota INTEGER,
    fecha TEXT,
    tipo_servicio TEXT,
    observaciones TEXT,
    FOREIGN KEY (id_mascota) REFERENCES mascotas(id_mascota)
)
""")

# Guardar cambios y cerrar
conexion.commit()
conexion.close()

print("Base de datos y tablas creadas correctamente.")
