import sqlite3
from datetime import datetime
from prettytable import PrettyTable
import os

# Función para crear la base de datos y las tablas si no existen
def inicializar_base_datos():
    with sqlite3.connect('gestor_clientes.db') as conn:
        cursor = conn.cursor()

        # Crear la tabla de clientes si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL
            )
        ''')

        # Crear la tabla de prendas si no existe
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS prendas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                descripcion TEXT NOT NULL,
                precio_real REAL NOT NULL,
                precio_40 REAL NOT NULL,
                precio_50 REAL NOT NULL,
                cobrada INTEGER NOT NULL,
                FOREIGN KEY (cliente_id) REFERENCES clientes (id)
            )
        ''')

# Función para limpiar la pantalla
def limpiar_pantalla():
    sistema_operativo = os.name
    if sistema_operativo == 'posix':
        os.system('clear')  # Limpiar pantalla en sistemas tipo Unix
    elif sistema_operativo == 'nt':
        os.system('cls')    # Limpiar pantalla en sistemas Windows

# Llamada a la función para inicializar la base de datos
inicializar_base_datos()
# Funciones relacionadas con la base de datos
def conectar_bd():
    return sqlite3.connect('gestor_clientes.db')

def buscar_clientes(nombre):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM clientes WHERE nombre LIKE ?', (f'%{nombre}%',))
        return cursor.fetchall()

def obtener_prendas(cliente_id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT p.id, c.nombre, p.fecha, p.descripcion, p.precio_real, p.precio_40, p.precio_50, p.cobrada FROM prendas p JOIN clientes c ON p.cliente_id = c.id WHERE p.cliente_id = ?', (cliente_id,))
        return cursor.fetchall()

def agregar_cliente(nombre):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO clientes (nombre) VALUES (?)', (nombre,))
        conn.commit()

def agregar_prenda(cliente_id, descripcion, precio_real):
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    precio_40 = precio_real * 0.4
    precio_50 = precio_real * 0.5

    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO prendas (cliente_id, fecha, descripcion, precio_real, precio_40, precio_50, cobrada) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (cliente_id, fecha_actual, descripcion, precio_real, precio_40, precio_50, 0))
        conn.commit()

def eliminar_prenda(prenda_id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM prendas WHERE id = ?', (prenda_id,))
        conn.commit()

def marcar_cobrada(prenda_id, cobrada):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('UPDATE prendas SET cobrada = ? WHERE id = ?', (cobrada, prenda_id))
        conn.commit()

# Funciones para la interfaz de consola
def mostrar_clientes_encontrados(clientes):
    table = PrettyTable()
    table.field_names = ["ID", "Nombre del Cliente"]

    for cliente in clientes:
        table.add_row([cliente[0], cliente[1]])

    print(table)

def mostrar_prendas_cliente(prendas):
    table = PrettyTable()
    table.field_names = ["ID", "Cobrada", "Descripción", "Precio Real", "Precio 40%", "Precio 50%", "Fecha"]

    for prenda in prendas:
        table.add_row([prenda[0], 'Sí' if prenda[7] else 'No', prenda[3], prenda[4], prenda[5], prenda[6], prenda[2]])
    
    print(table)

def buscar_cliente():
    nombre_cliente = input("Ingrese el nombre del cliente a buscar: ")
    clientes_encontrados = buscar_clientes(nombre_cliente)

    if clientes_encontrados:
        print("\nClientes Encontrados:")
        mostrar_clientes_encontrados(clientes_encontrados)
        cliente_id = elegir_cliente(clientes_encontrados)
        if cliente_id is not None:
            menu_prendas_cliente(cliente_id)
    else:
        print("No se encontraron clientes.")


def elegir_cliente(clientes):
    try:
        opcion = int(input("\nIngrese el número del cliente deseado (o 0 para cancelar): "))
        if 0 <= opcion <= len(clientes):
            if opcion == 0:
                print("Operación cancelada.")
                return None
            else:
                return clientes[opcion - 1][0]
        else:
            print("Número de cliente no válido. Intente de nuevo.")
            return elegir_cliente(clientes)
    except ValueError:
        print("Ingrese un número válido. Intente de nuevo.")
        return elegir_cliente(clientes)

def agregar_nuevo_cliente(nombre_cliente):
    try:
        agregar_cliente(nombre_cliente)
        print(f"Cliente '{nombre_cliente}' agregado exitosamente.")
    except Exception as e:
        print(f"Error al agregar el cliente: {e}")

def agregar_prenda_cliente(cliente_id):
    descripcion = input("Ingrese la descripción de la prenda: ")
    precio_real = float(input("Ingrese el precio real de la prenda: "))
    
    try:
        agregar_prenda(cliente_id, descripcion, precio_real)
        print(f"Prenda '{descripcion}' agregada al cliente {cliente_id}.")
    except Exception as e:
        print(f"Error al agregar la prenda: {e}")

def eliminar_prenda_cliente(cliente_id):
    prenda_id = int(input("Ingrese el ID de la prenda a eliminar: "))
    try:
        eliminar_prenda(prenda_id)
        print(f"Prenda eliminada del cliente {cliente_id}.")
    except Exception as e:
        print(f"Error al eliminar la prenda: {e}")

def marcar_cobrada_prenda_cliente(cliente_id):
    prenda_id = int(input("Ingrese el ID de la prenda a marcar/desmarcar como cobrada: "))
    cobrada = int(input("¿Cobrada? (1 para Sí, 0 para No): "))
    try:
        marcar_cobrada(prenda_id, cobrada)
        estado = "cobrada" if cobrada else "no cobrada"
        print(f"Prenda marcada como {estado} para el cliente {cliente_id}.")
    except Exception as e:
        print(f"Error al marcar la prenda: {e}")
def obtener_nombre_cliente(cliente_id):
    with conectar_bd() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT nombre FROM clientes WHERE id = ?', (cliente_id,))
        resultado = cursor.fetchone()
        if resultado:
            return resultado[0]
        else:
            return "Cliente no encontrado"
        
def menu_prendas_cliente(cliente_id):
    while True:
        limpiar_pantalla()
        prendas = obtener_prendas(cliente_id)
        nombre_cliente = obtener_nombre_cliente(cliente_id)
        print(f"\n---- Prendas de {nombre_cliente} ----")
        mostrar_prendas_cliente(prendas)

        print("\nOpciones:")
        print("1. Agregar Prenda", "  2. Eliminar Prenda", "  3. Marcar/Desmarcar Cobrada")
        print("0. Volver al Menú Principal")

        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == '1':
            agregar_prenda_cliente(cliente_id)
        elif opcion == '2':
            eliminar_prenda_cliente(cliente_id)
        elif opcion == '3':
            marcar_cobrada_prenda_cliente(cliente_id)
        elif opcion == '0':
            print("Volviendo al Menú Principal.")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

# Menú principal
while True:
    limpiar_pantalla()
    print("*-------------------*")
    print("|Gestor de Clientes |")
    print("*-------------------*")
    print("1. Buscar Cliente", "   2. Agregar Nuevo Cliente", "   0. Salir\n")
    

    opcion = input("Ingrese el número de la opción deseada: ")

    if opcion == '1':
        buscar_cliente()
    elif opcion == '2':
        nombre_cliente = input("Ingrese el nombre del nuevo cliente: ")
        agregar_nuevo_cliente(nombre_cliente)
    elif opcion == '0':
        print("¡Hasta luego!")
        break
    else:
        print("Opción no válida. Intente de nuevo.")
