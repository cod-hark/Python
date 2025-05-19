import os
import json

# --- CONFIGURACIÓN DE ARCHIVOS ---
BASE_DIR = "datos_restaurante"
INGREDIENTES_FILE = os.path.join(BASE_DIR, "ingredientes.txt")
RECETAS_FILE = os.path.join(BASE_DIR, "recetas.txt")
RELACIONES_FILE = os.path.join(BASE_DIR, "relaciones.txt")
GASTOS_FILE = os.path.join(BASE_DIR, "gastos.txt")

def inicializar_archivos():
    """
    Crea los archivos necesarios para almacenar los datos si no existen.
    """
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)

    for archivo in [INGREDIENTES_FILE, RECETAS_FILE, RELACIONES_FILE, GASTOS_FILE]:
        if not os.path.exists(archivo):
            with open(archivo, "w") as f:
                json.dump([], f)  # Crear archivos vacíos en formato JSON

# --- FUNCIONES DE INGREDIENTES ---
def agregar_ingrediente():
    """
    Solicita al usuario los datos de un ingrediente y lo almacena.
    """
    while True:
        nombre = input("Ingrese el nombre del ingrediente: ")
        unidad_medida = input("Ingrese la unidad de medida (kg, litro, etc.): ")
        precio_unitario = float(input("Ingrese el precio por unidad: "))
        stock_actual = float(input("Ingrese el stock actual: "))

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

        print(f"Ingrediente '{nombre}' agregado correctamente.")

        continuar = input("Desea agregar otro ingrediente? (s/n): ").lower()
        if continuar != 's':
            break

def listar_ingredientes():
    """
    Lista todos los ingredientes almacenados.
    """
    with open(INGREDIENTES_FILE, "r") as f:
        ingredientes = json.load(f)

    if not ingredientes:
        print("No hay ingredientes registrados.")
        return

    print("\n--- Ingredientes ---")
    for i, ing in enumerate(ingredientes, start=1):
        print(f"{i}. {ing['nombre']} - {ing['stock_actual']} {ing['unidad_medida']} - ${ing['precio_unitario']}/unidad")

# --- FUNCIONES DE RECETAS ---
def agregar_receta():
    """
    Solicita al usuario los datos de una receta y la almacena.
    """
    while True:
        nombre = input("Ingrese el nombre de la receta: ")
        instrucciones = input("Ingrese las instrucciones de la receta: ")

        with open(RECETAS_FILE, "r") as f:
            recetas = json.load(f)

        recetas.append({
            "nombre": nombre,
            "instrucciones": instrucciones
        })

        with open(RECETAS_FILE, "w") as f:
            json.dump(recetas, f, indent=4)

        print(f"Receta '{nombre}' agregada correctamente.")

        continuar = input("Desea agregar otra receta? (s/n): ").lower()
        if continuar != 's':
            break

def listar_recetas():
    """
    Lista todas las recetas almacenadas.
    """
    with open(RECETAS_FILE, "r") as f:
        recetas = json.load(f)

    if not recetas:
        print("No hay recetas registradas.")
        return

    print("\n--- Recetas ---")
    for i, rec in enumerate(recetas, start=1):
        print(f"{i}. {rec['nombre']}: {rec['instrucciones']}")

# --- FUNCIONES DE RELACIONES ---
def agregar_relacion_receta_ingrediente():
    """
    Relaciona una receta con un ingrediente solicitando los datos al usuario.
    """
    while True:
        listar_recetas()
        receta = input("Ingrese el nombre de la receta a relacionar: ")

        listar_ingredientes()
        ingrediente = input("Ingrese el nombre del ingrediente: ")
        cantidad = float(input("Ingrese la cantidad necesaria del ingrediente: "))

        with open(RELACIONES_FILE, "r") as f:
            relaciones = json.load(f)

        relaciones.append({
            "receta": receta,
            "ingrediente": ingrediente,
            "cantidad": cantidad
        })

        with open(RELACIONES_FILE, "w") as f:
            json.dump(relaciones, f, indent=4)

        print(f"Relación entre receta '{receta}' e ingrediente '{ingrediente}' agregada correctamente.")

        continuar = input("Desea agregar otra relación? (s/n): ").lower()
        if continuar != 's':
            break

# --- FUNCIONES DE GASTOS ---
def agregar_gastos():
    """
    Permite agregar gastos semanales o mensuales.
    """
    while True:
        tipo = input("Desea registrar gastos semanales o mensuales? (semanales/mensuales): ").lower()
        monto = float(input(f"Ingrese el monto de los gastos {tipo}: "))

        with open(GASTOS_FILE, "r") as f:
            gastos = json.load(f)

        gastos.append({
            "tipo": tipo,
            "monto": monto
        })

        with open(GASTOS_FILE, "w") as f:
            json.dump(gastos, f, indent=4)

        print(f"Gastos {tipo} registrados correctamente.")

        continuar = input("Desea agregar más gastos? (s/n): ").lower()
        if continuar != 's':
            break

def calcular_gastos_totales():
    """
    Calcula el total de los gastos semanales y mensuales.
    """
    with open(GASTOS_FILE, "r") as f:
        gastos = json.load(f)

    total = sum(gasto["monto"] for gasto in gastos)
    return total

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

def calcular_precio_final(nombre_receta, margen_ganancia=0.3):
    """
    Calcula el precio final de un plato con un margen de ganancia y considerando gastos.
    """
    costo_receta = calcular_costo_receta(nombre_receta)
    gastos = calcular_gastos_totales()
    precio_final = costo_receta + (costo_receta * margen_ganancia) + (gastos / 10)  # Proporcionar gastos
    return round(precio_final, 2)

# --- INTERACCIÓN CON EL USUARIO ---
def menu():
    """
    Muestra un menú interactivo para el usuario.
    """
    while True:
        print("\n--- Menú Principal ---")
        print("1. Agregar ingrediente")
        print("2. Listar ingredientes")
        print("3. Agregar receta")
        print("4. Listar recetas")
        print("5. Relacionar receta con ingrediente")
        print("6. Agregar gastos semanales o mensuales")
        print("7. Calcular costo y precio final de una receta")
        print("8. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_ingrediente()
        elif opcion == "2":
            listar_ingredientes()
        elif opcion == "3":
            agregar_receta()
        elif opcion == "4":
            listar_recetas()
        elif opcion == "5":
            agregar_relacion_receta_ingrediente()
        elif opcion == "6":
            agregar_gastos()
        elif opcion == "7":
            listar_recetas()
            receta = input("Ingrese el nombre de la receta a calcular: ")
            costo = calcular_costo_receta(receta)
            gastos = calcular_gastos_totales()
            precio = calcular_precio_final(receta, gastos=gastos)
            print(f"Costo de {receta}: ${costo}")
            print(f"Gastos incluidos: ${gastos}")
            print(f"Precio final de {receta} (30% margen + gastos): ${precio}")
        elif opcion == "8":
            print("Saliendo del programa. ¡Adiós!")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# --- EJECUCIÓN PRINCIPAL ---
if __name__ == "__main__":
    inicializar_archivos()
    menu()
