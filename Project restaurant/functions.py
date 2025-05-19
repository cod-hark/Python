#Registro de Ingredientes



#Una función para agregar ingredientes, actualizar precios y gestionar stock.

def agregar_ingrediente(nombre, unidad_medida, precio_unitario, stock_actual):
    # Conexión a la base de datos
    # Insertar ingrediente en la tabla
    pass

# Función actualizar precio ingredientes

def actualizar_precio_ingrediente(id_ingrediente, nuevo_precio):
    # Actualizar el precio en la base de datos
    pass

#Cálculo del costo del plato
#Cada receta utiliza varios ingredientes. El costo total del plato es la suma del costo de los ingredientes por las cantidades especificadas.

def calcular_costo_receta(id_receta):
    ingredientes = obtener_ingredientes_receta(id_receta)  # Consulta SQL
    costo_total = sum([ingrediente['precio_unitario'] * ingrediente['cantidad'] for ingrediente in ingredientes])
    return costo_total

"""Cálculo del precio final
El precio final de un plato puede incluir:

Márgenes de ganancia: Por ejemplo, un 30%.
Prorrateo de costos operativos: Distribuir costos mensuales entre los platos vendidos."""

def calcular_precio_final(costo_receta, margen_ganancia=0.3, costo_operativo=0):
    precio_final = costo_receta + (costo_receta * margen_ganancia) + costo_operativo
    return round(precio_final, 2)


#Gestión de inventario
#Reducir las cantidades de los ingredientes cada vez que se venda un plato:

def actualizar_stock(id_receta, cantidad_vendida):
    ingredientes = obtener_ingredientes_receta(id_receta)  # Consulta SQL
    for ingrediente in ingredientes:
        reducir_stock(ingrediente['id'], ingrediente['cantidad'] * cantidad_vendida)
        
        

