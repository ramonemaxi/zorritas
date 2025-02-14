import pandas as pd
import mysql.connector

# 🔹 Conectar a la base de datos MySQL
conexion = mysql.connector.connect(
    host="localhost",
    user="maca",
    password="M4ca1977",
    database="zorritas"
)
cursor = conexion.cursor()

# 🔹 Cargar el archivo Excel con varias hojas
archivo_excel = "export.xlsx"  # Cambia por el nombre de tu archivo
xls = pd.ExcelFile(archivo_excel)

# 🔹 Leer cada hoja del archivo Excel
df_clientes = pd.read_excel(xls, "clientes")  # Pestaña 'clientes'
df_datos_clientes = pd.read_excel(xls, "datos_clientes")  # Pestaña 'datos_clientes'
df_prendas = pd.read_excel(xls, "prendas")  # Pestaña 'prendas'

df_clientes = df_clientes.where(pd.notna(df_clientes), None)
df_datos_clientes = df_datos_clientes.where(pd.notna(df_datos_clientes), None)
df_prendas = df_prendas.where(pd.notna(df_prendas), None)

# 🔹 Insertar datos en la tabla 'clientes'
for _, fila in df_clientes.iterrows():
    sql = "INSERT INTO clientes (id, nombre) VALUES (%s, %s)"
    valores = (fila["id"], fila["nombre"])
    cursor.execute(sql, valores)

# 🔹 Insertar datos en la tabla 'datos_clientes'
for _, fila in df_datos_clientes.iterrows():
    sql = "INSERT INTO datos_clientes (id, cliente_id, telefono, ig) VALUES (%s, %s, %s, %s)"
    valores = (fila["id"], fila["cliente_id"], fila["telefono"], fila["ig"])
    cursor.execute(sql, valores)

# 🔹 Insertar datos en la tabla 'prendas'
for _, fila in df_prendas.iterrows():
    sql = """INSERT INTO prendas (id, cliente_id, descripcion, precio_real, cobrada, fecha, fecha_venta, fecha_ingreso) 
             VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
    valores = (
        fila["id"], fila["cliente_id"], fila["descripcion"], fila["precio_real"], 
        fila["cobrada"], fila["fecha"], fila["fecha_venta"], "1999-01-01"
    )
    cursor.execute(sql, valores)

# 🔹 Guardar cambios y cerrar conexión
conexion.commit()
cursor.close()
conexion.close()

print("✅ Datos importados exitosamente a MySQL.")
