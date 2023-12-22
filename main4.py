import sqlite3
from tkinter import *
from tkinter import ttk

def obtener_datos_desde_db():
    # Conectar a la base de datos
    conn = sqlite3.connect('gestor_clientes.db')
    cursor = conn.cursor()

    # Ejecutar una consulta para obtener las fechas y prendas
    cursor.execute('SELECT fecha, descripcion FROM prendas WHERE cliente_id = 2')

    # Obtener todos los resultados
    datos = cursor.fetchall()

    # Cerrar la conexión a la base de datos
    conn.close()

    return datos

app = Tk()
app.title("Herencia Treeview")

ttk.Label(app, text="Herencia Treeview").pack()

treeview = ttk.Treeview(app)
treeview.pack()

# Obtener datos desde la base de datos
datos_desde_db = obtener_datos_desde_db()

# Diccionario para organizar las prendas por fecha
prendas_por_fecha = {}

# Organizar las prendas por fecha en el diccionario
for fecha, prenda in datos_desde_db:
    if fecha not in prendas_por_fecha:
        prendas_por_fecha[fecha] = []
    
    prendas_por_fecha[fecha].append(prenda)

# Insertar datos automáticamente en el Treeview
for fecha, prendas in prendas_por_fecha.items():
    treeview.insert('', "end", fecha, text=fecha)
    
    for idx, prenda in enumerate(prendas, start=1):
        treeview.insert(fecha, 'end', f'{fecha}_{idx}', text=prenda)

app.mainloop()
