import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from datetime import datetime
import time
import mysql.connector


# Configuración de la conexión a MySQL
mydb = mysql.connector.connect(
  host="localhost",  # Reemplaza con tu host
  user="maca",  # Reemplaza con tu usuario
  password="M4ca1977",  # Reemplaza con tu contraseña
  database="zorritas"  # Reemplaza con el nombre de tu base de datos
)
mycursor = mydb.cursor()


def show_error(message):
    messagebox.showerror("Error", message)
        
def show_clients():
    try:
        mycursor.execute('SELECT * FROM clientes ORDER BY id DESC')
        return mycursor.fetchall()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error


def show_clients_in_list(filter=None):
    clients = show_clients()
    list_clients.delete(*list_clients.get_children())  # Clear existing items
    for client in clients:
        if filter is None or filter.lower() in client[1].lower():
            list_clients.insert('', tk.END, values=(client[0], client[1]))
    # Enfocar en el primer elemento si hay elementos en la lista
    if list_clients.get_children():
        list_clients.selection_set(list_clients.get_children()[0])
        list_clients.focus(list_clients.get_children()[0])

def show_client_garments(client_id):
    try:
        if control.get() == 1:
            mycursor.execute('SELECT * FROM prendas WHERE cliente_id = %s and cobrada = 0 ORDER BY fecha DESC', (client_id,))
        if control.get() == 2:
            mycursor.execute('SELECT * FROM prendas WHERE cliente_id = %s and cobrada = 1 ORDER BY fecha DESC', (client_id,))
        if control.get() == 3:
            mycursor.execute('SELECT * FROM prendas WHERE cliente_id = %s ORDER BY fecha DESC', (client_id,))
    
           
        garments = mycursor.fetchall()
        garments_tree.delete(*garments_tree.get_children())  # Clear existing items

        # Definir colores alternos
        color1 = '#ECECEC'  # Color para las filas pares
        color2 = '#D0D0D0'  # Color para las filas impares

        # Configurar etiquetas
        garments_tree.tag_configure('color1', background=color1)
        garments_tree.tag_configure('color2', background=color2)

        # Agregar filas con colores alternos
        for i, garment in enumerate(garments):
            
            if garment[4] == 1:
                cobrada = "SI"
            else:
                cobrada = "NO"
                
            
            if garment[6] is None or garment[6] == "":
                fecha_cobro = "NO"
            else:
                fecha_cobro = garment[6]

            if garment[3] <= 10000:
                efectivo = round(float(garment[3]) * 0.4, 2)
                credito = round(float(garment[3]) * 0.5, 2)
                
            elif 10500 <= garment[3] <= 20000:
                efectivo = round(float(garment[3]) * 0.5, 2)
                credito = round(float(garment[3]) * 0.5, 2)
                
            elif 20500 <= garment[3] <= 30000:
                efectivo = round(float(garment[3]) * 0.6, 2)
                credito = round(float(garment[3]) * 0.6, 2)
                
            else:  # precio >= 30000
                efectivo = round(float(garment[3]) * 0.7, 2)
                credito = round(float(garment[3]) * 0.7, 2)
        
            # Agregar filas con colores alternos y aplicar etiquetas inmediatamente
            if i % 2 == 0:
                garments_tree.insert('', tk.END, values=(garment[0], garment[2], garment[3], credito, efectivo, cobrada, garment[5], fecha_cobro), tags=('color1',))
            else:
                garments_tree.insert('', tk.END, values=(garment[0], garment[2], garment[3], credito, efectivo, cobrada, garment[5], fecha_cobro), tags=('color2',))
    
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error

        
def update_list(event):
    filter = entry_new_client.get()
    show_clients_in_list(filter)

def add_garment():
    fecha_actual = datetime.now().date()
    client_selection = list_clients.selection()
    
    if not client_selection:
        return
    client_item = list_clients.item(client_selection[0]) 
    client_id = client_item['values'][0]
        
    ventana_agregar_prenda = tk.Toplevel(frame_clients)
    ventana_agregar_prenda.title("Agregar Prenda")
    ventana_agregar_prenda.update_idletasks()  # Asegurarse de que la ventana tiene dimensiones antes de obtenerlas
    width = ventana_agregar_prenda.winfo_width()
    height = ventana_agregar_prenda.winfo_height()

    screen_width = ventana_agregar_prenda.winfo_screenwidth()
    screen_height = ventana_agregar_prenda.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    x = x -100
    y = y -50
    ventana_agregar_prenda.geometry(f"+{x}+{y}")

    # Etiquetas y campos de entrada en el formulario
    tk.Label(ventana_agregar_prenda, text="Descripcion:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_desc = tk.Entry(ventana_agregar_prenda, width=50)
    entry_desc.grid(row=0, column=1, padx=10, pady=5)
    entry_desc.focus()
    tk.Label(ventana_agregar_prenda, text="Precio:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_precio = tk.Entry(ventana_agregar_prenda, width=10)
    entry_precio.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_agregar_prenda, text="Fecha de Venta:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_fecha = Calendar(ventana_agregar_prenda, selectmode='day', year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)
    
    
    # Botón para guardar la prenda
    btn_guardar_prenda = tk.Button(ventana_agregar_prenda, text="Guardar Prenda", command=lambda: guardar_prenda(client_id, entry_desc.get(), entry_precio.get(),entry_fecha.get_date(), ventana_agregar_prenda))
    btn_guardar_prenda.grid(row=3, column=1, padx=10, pady=5)
    
    ventana_agregar_prenda.bind('<Return>', lambda event=None: btn_guardar_prenda.invoke())

def guardar_prenda(client_id, descripcion, precio, fecha_in, ventana_agregar_prenda):
    try:
        if not descripcion:
            show_error("Falta Descripción")
            return
        if not precio.isdigit():
            show_error("Precio no es numerico")
            return
        precio = int(precio)
        if precio <= 0:
            show_error("Precio tiene que ser mayor que 0")
            return
    except:
        return
    # Aquí puedes realizar las acciones necesarias para guardar la prenda
    # Por ejemplo, agregar el nombre de la prenda a una lista o base de datos
    cobrada = 0
    try:
        mycursor.execute('INSERT INTO prendas (cliente_id, descripcion, precio_real, cobrada, fecha) VALUES (%s, %s, %s, %s, %s)', (client_id, descripcion, precio, cobrada ,fecha_in))
        mydb.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error

        
    ventana_agregar_prenda.destroy()  # Cerrar la ventana después de guardar la prenda
    show_client_garments(client_id)
    no_cobradas_total(client_id)
        
def delete_garment():
    respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar esta prenda?")
    
    # La variable 'respuesta' será True si el usuario presiona 'Sí' y False si presiona 'No'
    if respuesta:
        # Código para eliminar el usuario
        garment_selection = garments_tree.selection()
        if garment_selection:
            garment_item = garments_tree.item(garment_selection[0])
            
            
            garment_name = garment_item['values'][0]
            

            try:
                mycursor.execute('DELETE FROM prendas WHERE ID = %s', (garment_name,))
                mydb.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                mydb.rollback()  # Revierte los cambios en caso de error
          
                
            client_selection = list_clients.selection()
            if client_selection:
                client_item = list_clients.item(client_selection[0])
                client_name = client_item['values'][0]
                show_client_garments(client_name)
                no_cobradas_total(client_name)

def mark_paid():
    fecha_actual = datetime.now().date()
    client_selection = list_clients.selection()
    
    if not client_selection:
        return
    client_item = list_clients.item(client_selection[0]) 
    client_id = client_item['values'][0]
        
    ventana_agregar_prenda = tk.Toplevel(frame_clients)
    ventana_agregar_prenda.title("Fecha de Cobro")
    ventana_agregar_prenda.update_idletasks()  # Asegurarse de que la ventana tiene dimensiones antes de obtenerlas
    width = ventana_agregar_prenda.winfo_width()
    height = ventana_agregar_prenda.winfo_height()

    screen_width = ventana_agregar_prenda.winfo_screenwidth()
    screen_height = ventana_agregar_prenda.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    x = x -100
    y = y -50
    ventana_agregar_prenda.geometry(f"+{x}+{y}")

    # Etiquetas y campos de entrada en el formulario

    entry_fecha = Calendar(ventana_agregar_prenda, selectmode='day', year=fecha_actual.year, month=fecha_actual.month, day=fecha_actual.day)
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)
    
    
    # Botón para guardar la prenda
    btn_guardar_prenda = tk.Button(ventana_agregar_prenda, text="Marcar como Cobrada", command=lambda: Cobrada(entry_fecha.get_date(), ventana_agregar_prenda))
    btn_guardar_prenda.grid(row=3, column=1, padx=10, pady=5)
    
    ventana_agregar_prenda.bind('<Return>', lambda event=None: btn_guardar_prenda.invoke())

def Cobrada(fecha, ventana):
    
    garment_selection = garments_tree.selection()
    if garment_selection:
        garment_item = garments_tree.item(garment_selection[0])
        garment_id = garment_item['values'][0]
        cobrada = 1

        try:
            mycursor.execute('UPDATE prendas SET cobrada = %s WHERE ID = %s', (cobrada, garment_id))
            mycursor.execute('UPDATE prendas SET fecha_venta = %s WHERE ID = %s', (fecha, garment_id))
            mydb.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            mydb.rollback()  # Revierte los cambios en caso de error
  
                
        client_selection = list_clients.selection()
        if client_selection:
            client_item = list_clients.item(client_selection[0])
            client_name = client_item['values'][0]
            show_client_garments(client_name)
            no_cobradas_total(client_name)
            ventana.destroy()

def mark_as_no_paid():
    garment_selection = garments_tree.selection()
    if garment_selection:
        garment_item = garments_tree.item(garment_selection[0])
        garment_id = garment_item['values'][0]
        cobrada = 0

        try:
            mycursor.execute('UPDATE prendas SET cobrada = %s, fecha_venta = NULL WHERE ID = %s', (cobrada, garment_id))
            mydb.commit()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            mydb.rollback()  # Revierte los cambios en caso de error

        client_selection = list_clients.selection()
        if client_selection:
            client_item = list_clients.item(client_selection[0])
            client_name = client_item['values'][0]
            show_client_garments(client_name)
            no_cobradas_total(client_name)

def select_client(event):
    selection = list_clients.selection()
    if selection:
        item = list_clients.item(selection[0])
        client_name = item['values'][0]
        mostra_datos_cliente()
        show_client_garments(client_name)
        no_cobradas_total(client_name)

def eliminar_cliente_seleccionado():
    # Muestra un cuadro de diálogo de confirmación
    respuesta = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar el cliente?")
    
    # La variable 'respuesta' será True si el usuario presiona 'Sí' y False si presiona 'No'
    if respuesta:
        # Código para eliminar el usuario
        selection = list_clients.selection()
        if selection:
            item = list_clients.item(selection[0])
            client_name = item['values'][0]
            garments_tree.delete(*garments_tree.get_children())
            
            try:
                mycursor.execute('DELETE FROM clientes WHERE ID = %s', (client_name,))
                mydb.commit()
            except mysql.connector.Error as err:
                print(f"Error: {err}")
                mydb.rollback()  # Revierte los cambios en caso de error

            
            # Actualiza el treeview después de eliminar el cliente (puedes omitir esto si no es necesario)
            list_clients.delete(selection)
        
def on_checkbutton_changed(*args):
    select_client(None)  

def agregar_cliente():
    # Función para abrir la nueva ventana y recopilar la información del cliente
    ventana_formulario = tk.Toplevel(window)
    ventana_formulario.title("Agregar Cliente")

    ventana_formulario.update_idletasks()  # Asegurarse de que la ventana tiene dimensiones antes de obtenerlas
    width = ventana_formulario.winfo_width()
    height = ventana_formulario.winfo_height()

    screen_width = ventana_formulario.winfo_screenwidth()
    screen_height = ventana_formulario.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    ventana_formulario.geometry(f"+{x}+{y}")
    # Etiquetas y campos de entrada en el formulario
    tk.Label(ventana_formulario, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(ventana_formulario)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)
    entry_nombre.focus()
    tk.Label(ventana_formulario, text="Telefono:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_telefono = tk.Entry(ventana_formulario)
    entry_telefono.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_formulario, text="IG:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_ig = tk.Entry(ventana_formulario)
    entry_ig.grid(row=2, column=1, padx=10, pady=5)
    
    btn_salvar = tk.Button(ventana_formulario, text="Guardar", command=lambda: add_client(entry_nombre.get(), entry_telefono.get(), entry_ig.get(), ventana_formulario))
    btn_salvar.grid(row=3, column=1, padx=10, pady=10)
    
    ventana_formulario.bind('<Return>', lambda event=None: btn_salvar.invoke())
    
def add_client(name, telefono, ig, ventana):
    if not name:
        tk.messagebox.showerror("Error", "Por favor, ingrese un nombre.")
        return
    try:
        mycursor.execute('INSERT INTO clientes (nombre) VALUES (%s)', (name,))
        mydb.commit()
        
        client_id = mycursor.lastrowid  # Obtenemos el ID del cliente recién insertado
        
        # Insertar los datos asociados en la segunda tabla utilizando el ID del cliente
        mycursor.execute('INSERT INTO datos_clientes (cliente_id, telefono, ig) VALUES (%s, %s, %s)', (client_id, telefono, ig))
        
        # Commit para aplicar los cambios en la base de datos
        mydb.commit()
        ventana.destroy()
        show_clients_in_list()  
        entry_new_client.focus()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error

        
def editar_cliente_form():
    selection = list_clients.selection()
    if not selection:
        return
    item = list_clients.item(selection[0])
    clien_id = item['values'][0]
    try:
        mycursor.execute('SELECT * FROM datos_clientes WHERE cliente_id = %s', (clien_id,))
        result = mycursor.fetchall()
        for row in result:
            nombre = item['values'][1]
            telefono = row[2]
            ig = row[3]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error

        
    # Función para abrir la nueva ventana y editar la información del cliente
    ventana_formulario = tk.Toplevel(window)
    ventana_formulario.title("Editar Cliente")
    
    ventana_formulario.update_idletasks()  # Asegurarse de que la ventana tiene dimensiones antes de obtenerlas
    width = ventana_formulario.winfo_width()
    height = ventana_formulario.winfo_height()

    screen_width = ventana_formulario.winfo_screenwidth()
    screen_height = ventana_formulario.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    ventana_formulario.geometry(f"+{x}+{y}")
    # Etiquetas y campos de entrada en el formulario
    tk.Label(ventana_formulario, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_nombre = tk.Entry(ventana_formulario)
    entry_nombre.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_formulario, text="Telefono:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_telefono = tk.Entry(ventana_formulario)
    entry_telefono.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(ventana_formulario, text="IG:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    entry_ig = tk.Entry(ventana_formulario)
    entry_ig.grid(row=2, column=1, padx=10, pady=5)
    
    btn_salvar = tk.Button(ventana_formulario, text="Guardar", command=lambda: modificar_cliente(clien_id, entry_nombre.get(), entry_telefono.get(), entry_ig.get(), ventana_formulario))
    btn_salvar.grid(row=3, column=1, padx=10, pady=10)
    ventana_formulario.bind('<Return>', lambda event=None: btn_salvar.invoke())
    # Rellenar los campos con los datos del cliente seleccionado
    entry_nombre.insert(0, nombre)
    entry_telefono.insert(0, telefono)
    entry_ig.insert(0, ig)
    
def modificar_cliente(id, name, telefono, ig, ventana):
    
    if not name:
        tk.messagebox.showerror("Error", "Por favor, ingrese un nombre.")
        return
    try:
        mycursor.execute('UPDATE clientes SET nombre = %s WHERE ID = %s', (name,id,))
        mydb.commit()
        
        client_id = mycursor.lastrowid  # Obtenemos el ID del cliente recién insertado
        
        # Insertar los datos asociados en la segunda tabla utilizando el ID del cliente
        mycursor.execute('UPDATE datos_clientes SET telefono = %s, ig = %s WHERE cliente_id = %s', (telefono, ig, id))
        
        # Commit para aplicar los cambios en la base de datos
        mydb.commit()
        mostra_datos_cliente()
        ventana.destroy()
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error

        
def mostra_datos_cliente():
    selection = list_clients.selection()
    if not selection:
        return
    item = list_clients.item(selection[0])
    clien_id = item['values'][0]
    try:
        mycursor.execute('SELECT * FROM datos_clientes WHERE cliente_id = %s', (clien_id,))
        result = mycursor.fetchall()
        for row in result:
            nombre = item['values'][1]
            telefono = row[2]
            ig = row[3]
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error

        
    nomb_variable.set("NOMBRE: " + nombre)
    tel_variable.set("TELEFONO: " + telefono if telefono is not None else "TELEFONO: ")
    ig_variable.set("IG: " + ig if ig is not None else "IG: ")    

def mostrar_prendas_fecha():
    ventana_prendas = tk.Toplevel(window)
    ventana_prendas.geometry("600x400")
    ventana_prendas.title("Fechas")
    selection = list_clients.selection()
    ventana_prendas.update_idletasks()  # Asegurarse de que la ventana tiene dimensiones antes de obtenerlas
    width = ventana_prendas.winfo_width()
    height = ventana_prendas.winfo_height()

    screen_width = ventana_prendas.winfo_screenwidth()
    screen_height = ventana_prendas.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    ventana_prendas.geometry(f"+{x}+{y}")
    if not selection:
        return
    item = list_clients.item(selection[0])
    clien_id = item['values'][0]
    
    def obtener_datos_desde_db():
        # Conectar a la base de datos
        mycursor = mydb.cursor()

        # Ejecutar una consulta para obtener las fechas y prendas
        mycursor.execute('SELECT fecha, descripcion FROM prendas WHERE cliente_id = %s', (clien_id,))

        # Obtener todos los resultados
        datos = mycursor.fetchall()

        # Cerrar la conexión a la base de datos
        mydb.close()

        return datos

   

    ttk.Label(ventana_prendas, text="Prendas X Fecha").pack()

    treeview = ttk.Treeview(ventana_prendas)
    treeview.pack(fill="both", expand=True)

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
            
def no_cobradas_total(client_id):
    
    try:   
        mycursor.execute('SELECT * FROM prendas WHERE cliente_id = %s and cobrada = 0', (client_id,))
        garments = mycursor.fetchall()
        totale_tree.delete(*totale_tree.get_children())
        total = 0
        for garment in enumerate(garments):
            
            total = total + garment[1][3]
        print(total)
        totale_tree.insert('', tk.END, values=("", round(float(total)) * 0.5, round(float(total)) * 0.4))
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error


def editar_prenda_form():
    
    garment_selection = garments_tree.selection()
    if garment_selection:
        garment_item = garments_tree.item(garment_selection[0])
        
        
        garment_name = garment_item['values'][0]
    try:
        mycursor.execute('SELECT * FROM prendas WHERE id = %s', (garment_name,))
        result = mycursor.fetchall()
        for row in result:
            
            descripcion = row[2]
            precio = row[3]
            fecha = row[5]
            fecha = datetime.strptime(fecha, "%d/%m/%y")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error
       
        
        
    # Función para abrir la nueva ventana y editar la información del cliente
    ventana_formulario = tk.Toplevel(window)
    ventana_formulario.title("Editar Prenda")
    
    ventana_formulario.update_idletasks()  # Asegurarse de que la ventana tiene dimensiones antes de obtenerlas
    width = ventana_formulario.winfo_width()
    height = ventana_formulario.winfo_height()

    screen_width = ventana_formulario.winfo_screenwidth()
    screen_height = ventana_formulario.winfo_screenheight()

    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    ventana_formulario.geometry(f"+{x}+{y}")
    # Etiquetas y campos de entrada en el formulario
    tk.Label(ventana_formulario, text="Descripcion:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    entry_desc = tk.Entry(ventana_formulario, width=50)
    entry_desc.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(ventana_formulario, text="Precio:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    entry_precio = tk.Entry(ventana_formulario)
    entry_precio.grid(row=1, column=1, padx=10, pady=5)

    entry_fecha = Calendar(ventana_formulario, selectmode='day', year=fecha.year, month=fecha.month, day=fecha.day)
    entry_fecha.grid(row=2, column=1, padx=10, pady=5)
    
    btn_salvar = tk.Button(ventana_formulario, text="Guardar", command=lambda: modificar_prenda(garment_name, entry_desc.get(), entry_precio.get(), entry_fecha.get_date(), ventana_formulario))
    btn_salvar.grid(row=3, column=1, padx=10, pady=10)
    ventana_formulario.bind('<Return>', lambda event=None: btn_salvar.invoke())
    # Rellenar los campos con los datos del cliente seleccionado
    entry_desc.insert(0, descripcion)
    entry_precio.insert(0, precio)
    
def modificar_prenda(id, descripcion, precio, fecha, ventana):
    print(fecha)
    try:
        if not descripcion:
            show_error("Falta Descripción")
            return
        if not precio.isdigit():
            show_error("Precio no es numerico")
            return
        precio = int(precio)
        if precio <= 0:
            show_error("Precio tiene que ser mayor que 0")
            return
    except:
        return
    try:
        mycursor.execute('UPDATE prendas SET descripcion = %s, precio_real = %s, fecha = %s WHERE id = %s', (descripcion, precio, fecha, id))
        print(id, descripcion, fecha, precio)
        mydb.commit()
        selection = list_clients.selection()
        if not selection:
            return
        item = list_clients.item(selection[0])
        clien_id = item['values'][0]
        show_client_garments(clien_id)
        no_cobradas_total(clien_id)
        ventana.destroy()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        mydb.rollback()  # Revierte los cambios en caso de error

#Init de tkinter
window = tk.Tk()
window.geometry('1280x700')
window.minsize(1200,700)
window.title("Libro de Ventas")
icono = tk.PhotoImage(file="fox_scarf_icon_159308.png")
window.iconphoto(True, icono)
color_fondo = "#77824A"
window.configure(bg=color_fondo)
# initialize_db()

#Main Frame
frame_clients = tk.Frame(window)

frame_clients.pack(expand=True, fill='both', padx=5,pady=5)

frame_clients.grid_columnconfigure(1, weight=1)
frame_clients.grid_rowconfigure(1, weight=1)

#Logo y Nombre
tk.Label(frame_clients, text="Zorritas Vintage").grid(row=0, column=1, sticky=tk.NSEW)
ruta_logo = 'fox_scarf_icon_159308.png'
imagen = PhotoImage(file=ruta_logo)
label_logo = tk.Label(frame_clients, image=imagen)
label_logo.grid(row=0, column=1, sticky=tk.E)

#Buscar Clientes
entry_new_client = tk.Entry(frame_clients, width=40) 
entry_new_client.focus()
entry_new_client.grid(row=0, column=0, padx=5, pady=10, sticky=tk.NSEW)

#Vista de datos de Clientes
nomb_variable = tk.StringVar()
label_cliente_nombre = tk.Label(frame_clients, text="Nombre del Cliente", width=150, textvariable=nomb_variable)
label_cliente_nombre.grid(row=6, column=1, sticky=tk.W)
tel_variable = tk.StringVar()
label_cliente_telefono = tk.Label(frame_clients, text="Telefono del Cliente", width=150, textvariable=tel_variable)
label_cliente_telefono.grid(row=7, column=1, sticky=tk.NS)
ig_variable = tk.StringVar()
label_cliente_ig = tk.Label(frame_clients, text="ig del Cliente", width=150, textvariable=ig_variable)
label_cliente_ig.grid(row=8, column=1, sticky=tk.E)





#Check Button No Cobradas
control = tk.IntVar()
control.set(3)
checkbutton = tk.Radiobutton(frame_clients, text="Mostrar solo no cobradas", variable=control, value=1)
checkbutton.grid(row=1, column=1, sticky=tk.SW, padx=0, pady=0)

# solo_cobradas = tk.IntVar()
checkbutton = tk.Radiobutton(frame_clients, text="Mostrar solo cobradas", variable=control, value=2)
checkbutton.grid(row=1, column=1, sticky=tk.SE, padx=0, pady=0)

checkbutton = tk.Radiobutton(frame_clients, text="Mostrar Todo", variable=control, value=3)
checkbutton.grid(row=1, column=1, sticky=tk.S, padx=0, pady=0)

#Lista de Clientes
list_clients = ttk.Treeview(frame_clients, columns=("ID", "Name"), height=10)

list_clients.heading("#0", text="ID")
list_clients.heading("ID", text="ID")
list_clients.heading("Name", text="Nombre")
list_clients.column("#0", stretch=tk.NO, width=0)
list_clients.column("ID", stretch=tk.NO ,width=0)
list_clients.column("Name", stretch=tk.YES, width=150)

list_clients.grid(row=4, column=0, padx=5, pady=0, sticky=tk.NSEW)

entry_new_client.bind('<KeyRelease>', update_list)


# #Lista de Prendas
garments_tree = ttk.Treeview(frame_clients, columns=("ID", "Description", "Price Real", "Credito", "Efectivo", "Cobrada", "Fecha", "Fecha_cob"), height=19)

garments_tree.heading("#0", text="Prendas")
garments_tree.heading("ID", text="ID")
garments_tree.heading("Description", text="Descripción")
garments_tree.heading("Price Real", text="Precio Venta")
garments_tree.heading("Credito", text="Credito")
garments_tree.heading("Efectivo", text="Efectivo")
garments_tree.heading("Cobrada", text="Cobrada")
garments_tree.heading("Fecha", text="Fecha Venta")
garments_tree.heading("Fecha_cob", text="Fecha_cob")

garments_tree.column("#0", stretch=tk.NO, width=0)
garments_tree.column("ID", stretch=tk.NO, width=0)
garments_tree.column("Description", stretch=tk.YES, anchor=CENTER)  # 60% of the screen width
garments_tree.column("Price Real", stretch=tk.NO, minwidth=10, width=100, anchor=CENTER)
garments_tree.column("Credito", stretch=tk.NO, minwidth=10, width=100, anchor=CENTER)
garments_tree.column("Efectivo", stretch=tk.NO, minwidth=10, width=100, anchor=CENTER)
garments_tree.column("Cobrada", stretch=tk.NO, minwidth=10, width=80, anchor=CENTER)
garments_tree.column("Fecha", stretch=tk.NO, minwidth=10, width=80, anchor=CENTER)
garments_tree.column("Fecha_cob", stretch=tk.NO, minwidth=10, width=100, anchor=CENTER)
garments_tree.grid(row=4, column=1, padx=5, pady=0, sticky=tk.EW)

#totales prendas
totale_tree = ttk.Treeview(frame_clients, columns=("ID","credito", "efectivo"), height=1)

totale_tree.heading("#0", text="Prendas")
totale_tree.heading("ID", text="ID")
totale_tree.heading("credito", text="Credito")
totale_tree.heading("efectivo", text="Efectivo")

totale_tree.column("#0", stretch=tk.NO, width=0)
totale_tree.column("ID", stretch=tk.NO, width=0)
totale_tree.column("credito", stretch=tk.NO, minwidth=10, width=100, anchor=CENTER)
totale_tree.column("efectivo", stretch=tk.NO, minwidth=10, width=100, anchor=CENTER)
totale_tree.grid(row=5, column=1, padx=10, pady=0, sticky=tk.E)

#Acciones de clientes
btn_add_client = tk.Button(frame_clients, text="Agregar Cliente", command=agregar_cliente, width=27)
btn_modif_cliente = tk.Button(frame_clients, text="Modificar Cliente", command=editar_cliente_form, width=27)
btn_eliminar_cliente = tk.Button(frame_clients, text="Eliminar Cliente", command=eliminar_cliente_seleccionado, width=27)

btn_add_client.grid(row=6, column=0, padx=10, pady=10, sticky=tk.W)
btn_modif_cliente.grid(row=7, column=0, padx=10, pady=10, sticky=tk.W)
btn_eliminar_cliente.grid(row=8, column=0, pady=10,padx=10, sticky=tk.W)

#Opciones de prendas
btn_add_garment = tk.Button(frame_clients, text="Agregar Prenda", command=add_garment, bg="green", width=20)
btn_mod_garment = tk.Button(frame_clients, text="Modificar Prenda", command=editar_prenda_form, bg="yellow", width=20)
btn_delete_garment = tk.Button(frame_clients, text="Eliminar Prenda", command=delete_garment, bg="red", width=20)
btn_ver_prendas = tk.Button(frame_clients, text="Ver Prendas", command=mostrar_prendas_fecha, bg="white")
btn_mark_as_paid = tk.Button(frame_clients, text="Cobrada", command=mark_paid)
btn_mark_as_no_paid = tk.Button(frame_clients, text="No Cobrada", command=mark_as_no_paid)

btn_add_garment.grid(row=5, column=1, pady=10, padx=10, sticky=tk.W)
btn_mod_garment.grid(row=6, column=1, pady=10, padx=10, sticky=tk.W)
btn_delete_garment.grid(row=7, column=1, pady=10,padx=10, sticky=tk.W)
btn_ver_prendas.grid(row=8, column=1, pady=10,padx=10, sticky=tk.W)
btn_mark_as_no_paid.grid(row=6, column=1, sticky=tk.E, padx=10, pady=10)
btn_mark_as_paid.grid(row=6, column=1, sticky=tk.E, pady=10, padx=130)

list_clients.bind('<<TreeviewSelect>>', select_client)
control.trace_add('write', on_checkbutton_changed)
# solo_cobradas.trace_add('write', on_checkbutton_changed)

# Set weight to make the columns expand with window resizing
frame_clients.columnconfigure(0, weight=1)
frame_clients.rowconfigure(2, weight=1)

window.mainloop()

if mydb.is_connected(): # Verifica si la conexión está activa.
    mycursor.close()
    mydb.close()
    print("Conexión cerrada.")