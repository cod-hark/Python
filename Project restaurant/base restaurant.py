import os
import json

# --- CONFIGURACIÓN DE ARCHIVOS ---
BASE_DIR = "datos_restaurante"
INGREDIENTES_FILE = os.path.join(BASE_DIR, "ingredientes.txt")
RECETAS_FILE = os.path.join(BASE_DIR, "recetas.txt")
RELACIONES_FILE = os.path.join(BASE_DIR, "relaciones.txt")


def inicializar_archivos():
    """
    Crea los archivos necesarios para almacenar los datos si no existen.
    """
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    for archivo in [INGREDIENTES_FILE, RECETAS_FILE, RELACIONES_FILE]:
        if not os.path.exists(archivo):
            with open(archivo, "w") as f:
                json.dump([], f)  # Crear archivos vacíos en formato JSON


# --- FUNCIONES DE INGREDIENTES ---
def agregar_ingrediente(nombre, unidad_medida, precio_unitario, stock_actual):
    """
    Agrega un ingrediente al archivo de ingredientes.
    """
    with open(INGREDIENTES_FILE, "r") as f:
        ingredientes = json.load(f)

    ingredientes.append({
        "nombre": nombre,
        "unidad_medida": unidad_medida,
        "precio_unitario": precio_unitario,
        "stock_actual": stock_actual
    })

    with open(INGREDIENTES_FILE, "w") as f:
        json.dump(ingredientes, f, indent=4)


def listar_ingredientes():
    """
    Lista todos los ingredientes almacenados.
    """
    with open(INGREDIENTES_FILE, "r") as f:
        ingredientes = json.load(f)

    for i, ing in enumerate(ingredientes, start=1):
        print(f"{i}. {ing['nombre']} - {ing['stock_actual']} {ing['unidad_medida']} - ${ing['precio_unitario']}/unidad")


# --- FUNCIONES DE RECETAS ---
def agregar_receta(nombre, instrucciones):
    """
    Agrega una receta al archivo de recetas.
    """
    with open(RECETAS_FILE, "r") as f:
        recetas = json.load(f)

    recetas.append({
        "nombre": nombre,
        "instrucciones": instrucciones
    })

    with open(RECETAS_FILE, "w") as f:
        json.dump(recetas, f, indent=4)


def listar_recetas():
    """
    Lista todas las recetas almacenadas.
    """
    with open(RECETAS_FILE, "r") as f:
        recetas = json.load(f)

    for i, rec in enumerate(recetas, start=1):
        print(f"{i}. {rec['nombre']}: {rec['instrucciones']}")


# --- FUNCIONES DE RELACIONES ---
def agregar_relacion_receta_ingrediente(nombre_receta, nombre_ingrediente, cantidad):
    """
    Relaciona una receta con un ingrediente en el archivo de relaciones.
    """
    with open(RELACIONES_FILE, "r") as f:
        relaciones = json.load(f)

    relaciones.append({
        "receta": nombre_receta,
        "ingrediente": nombre_ingrediente,
        "cantidad": cantidad
    })

    with open(RELACIONES_FILE, "w") as f:
        json.dump(relaciones, f, indent=4)


def calcular_costo_receta(nombre_receta):
    """
    Calcula el costo total de una receta basada en los ingredientes y sus cantidades.
    """
    with open(RELACIONES_FILE, "r") as f:
        relaciones = json.load(f)

    with open(INGREDIENTES_FILE, "r") as f:
        ingredientes = json.load(f)

    costo_total = 0
    for relacion in relaciones:
        if relacion["receta"] == nombre_receta:
            ingrediente = next((i for i in ingredientes if i["nombre"] == relacion["ingrediente"]), None)
            if ingrediente:
                costo_total += ingrediente["precio_unitario"] * relacion["cantidad"]

    return round(costo_total, 2)


def calcular_precio_final(nombre_receta, margen_ganancia=0.4):
    """
    Calcula el precio final de un plato con un margen de ganancia.
    """
    costo_receta = calcular_costo_receta(nombre_receta)
    precio_final = costo_receta + (costo_receta * margen_ganancia)
    return round(precio_final, 2)


# --- DATOS DE PRUEBA ---
def insertar_datos_prueba():
    """
    Inserta datos de prueba en los archivos.
    """
    agregar_ingrediente("Tomate", "kg", 2.5, 10)
    agregar_ingrediente("Queso", "kg", 5.0, 5)
    agregar_ingrediente("Harina", "kg", 1.2, 20)
    agregar_ingrediente("Aceite", "litro", 3.0, 8)
    agregar_ingrediente("Pollo", "kg", 4.0, 10)

    agregar_receta("Pizza Margarita", "Preparar la base, añadir tomate y queso.")
    agregar_receta("Pollo Frito", "Freír el pollo con harina y aceite.")

    agregar_relacion_receta_ingrediente("Pizza Margarita", "Tomate", 0.5)
    agregar_relacion_receta_ingrediente("Pizza Margarita", "Queso", 0.3)
    agregar_relacion_receta_ingrediente("Pizza Margarita", "Harina", 0.4)

    agregar_relacion_receta_ingrediente("Pollo Frito", "Pollo", 1.0)
    agregar_relacion_receta_ingrediente("Pollo Frito", "Harina", 0.2)
    agregar_relacion_receta_ingrediente("Pollo Frito", "Aceite", 0.5)


# --- EJECUCIÓN ---
if __name__ == "__main__":
    inicializar_archivos()
    insertar_datos_prueba()

    print("\n--- Ingredientes ---")
    listar_ingredientes()

    print("\n--- Recetas ---")
    listar_recetas()

    print("\n--- Cálculo de Costos ---")
    receta = "Pizza Margarita"
    print(f"Costo de {receta}: ${calcular_costo_receta(receta)}")
    print(f"Precio final de {receta}: ${calcular_precio_final(receta)}")

    receta = "Pollo Frito"
    print(f"Costo de {receta}: ${calcular_costo_receta(receta)}")
    print(f"Precio final de {receta}: ${calcular_precio_final(receta)}")
