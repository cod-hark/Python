
pip install psycopg2 
import psycopg2

# --- CONFIGURACIÓN DE LA BASE DE DATOS ---
DB_NAME = "restaurante"
DB_USER = "postgres"
DB_PASSWORD = "tu_password"
DB_HOST = "localhost"
DB_PORT = "5432"

def conectar_bd():
    """
    Conecta a la base de datos PostgreSQL.
    """
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def inicializar_bd():
    """
    Crea las tablas necesarias en la base de datos.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Crear tabla de ingredientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredientes (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        unidad_medida TEXT NOT NULL,
        precio_unitario REAL NOT NULL,
        stock_actual REAL NOT NULL
    );
    """)

    # Crear tabla de recetas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recetas (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        instrucciones TEXT
    );
    """)

    # Crear tabla de relación entre recetas e ingredientes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS relacion_receta_ingredientes (
        id SERIAL PRIMARY KEY,
        id_receta INTEGER REFERENCES recetas(id),
        id_ingrediente INTEGER REFERENCES ingredientes(id),
        cantidad REAL NOT NULL
    );
    """)

    # Crear tabla de gastos operativos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS gastos_operativos (
        id SERIAL PRIMARY KEY,
        nombre TEXT NOT NULL,
        monto REAL NOT NULL,
        frecuencia TEXT NOT NULL
    );
    """)

    conexion.commit()
    cursor.close()
    conexion.close()
    print("Base de datos inicializada correctamente.")

# --- DATOS DE PRUEBA ---
def insertar_datos_prueba():
    """
    Inserta ingredientes y recetas de ejemplo para realizar pruebas.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    # Ingredientes
    cursor.execute("""
    INSERT INTO ingredientes (nombre, unidad_medida, precio_unitario, stock_actual)
    VALUES
        ('Tomate', 'kg', 2.5, 10),
        ('Queso', 'kg', 5.0, 5),
        ('Harina', 'kg', 1.2, 20),
        ('Aceite', 'litro', 3.0, 8),
        ('Pollo', 'kg', 4.0, 10)
    ON CONFLICT DO NOTHING;
    """)

    # Recetas
    cursor.execute("""
    INSERT INTO recetas (nombre, instrucciones)
    VALUES
        ('Pizza Margarita', 'Preparar la base, añadir tomate y queso.'),
        ('Pollo Frito', 'Freír el pollo con harina y aceite.')
    ON CONFLICT DO NOTHING;
    """)

    # Relación entre recetas e ingredientes
    cursor.execute("""
    INSERT INTO relacion_receta_ingredientes (id_receta, id_ingrediente, cantidad)
    VALUES
        (1, 1, 0.5),  -- Pizza Margarita: 0.5 kg de tomate
        (1, 2, 0.3),  -- Pizza Margarita: 0.3 kg de queso
        (1, 3, 0.4),  -- Pizza Margarita: 0.4 kg de harina
        (2, 5, 1.0),  -- Pollo Frito: 1 kg de pollo
        (2, 3, 0.2),  -- Pollo Frito: 0.2 kg de harina
        (2, 4, 0.5)   -- Pollo Frito: 0.5 litros de aceite
    ON CONFLICT DO NOTHING;
    """)

    conexion.commit()
    cursor.close()
    conexion.close()
    print("Datos de prueba insertados correctamente.")

# --- FUNCIONES ---
def calcular_costo_receta(id_receta):
    """
    Calcula el costo total de una receta en base a sus ingredientes.
    """
    conexion = conectar_bd()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT i.nombre, i.precio_unitario, rri.cantidad
    FROM relacion_receta_ingredientes rri
    JOIN ingredientes i ON rri.id_ingrediente = i.id
    WHERE rri.id_receta = %s;
    """, (id_receta,))

    ingredientes = cursor.fetchall()
    costo_total = sum(precio * cantidad for _, precio, cantidad in ingredientes)

    cursor.close()
    conexion.close()
    return costo_total

def calcular_precio_final(id_receta, margen_ganancia=0.3):
    """
    Calcula el precio final de un plato.
    """
    costo_receta = calcular_costo_receta(id_receta)
    precio_final = costo_receta + (costo_receta * margen_ganancia)
    return round(precio_final, 2)

# --- EJECUCIÓN ---
if __name__ == "__main__":
    inicializar_bd()
    insertar_datos_prueba()

    # Cálculo de costos y precios
    print("Costo de Pizza Margarita:", calcular_costo_receta(1))
    print("Precio final de Pizza Margarita:", calcular_precio_final(1))

    print("Costo de Pollo Frito:", calcular_costo_receta(2))
    print("Precio final de Pollo Frito:", calcular_precio_final(2))
