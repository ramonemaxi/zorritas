import tkinter as tk
from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
from tkcalendar import Calendar
from datetime import datetime
import time

#Init de tkinter
window = tk.Tk()
window.title("Libro de Prendas")
icono = tk.PhotoImage(file="fox_scarf_icon_159308.png")
window.iconphoto(True, icono)
color_fondo = "#77824A"
window.configure(bg=color_fondo)
# initialize_db()

#Main Frame
frame_clients = tk.Frame(window)
frame_clients.pack(expand=True, fill='both', padx=10,pady=10)

frame_clients.grid_columnconfigure(0, weight=1)
frame_clients.grid_rowconfigure(0, weight=1)

#Logo y Nombre
tk.Label(frame_clients, text="Zorritas VIntage").grid(row=0, column=1, sticky=tk.E, padx=200, pady=10)
ruta_logo = 'fox_scarf_icon_159308.png'
imagen = PhotoImage(file=ruta_logo)
label_logo = tk.Label(frame_clients, image=imagen)
label_logo.grid(row=1, column=1, padx=200, pady=10, sticky=tk.E)

#Buscar Clientes
entry_new_client = tk.Entry(frame_clients, width=50) 
entry_new_client.focus()
entry_new_client.grid(row=0, column=0, padx=10, pady=10, sticky=tk.EW)

# #Vista de datos de Clientes
# nomb_variable = tk.StringVar()
# label_cliente_nombre = tk.Label(frame_clients, text="Nombre del Cliente", width=150, textvariable=nomb_variable)
# label_cliente_nombre.grid(row=3, column=1, sticky=tk.EW)
# tel_variable = tk.StringVar()
# label_cliente_telefono = tk.Label(frame_clients, text="Telefono del Cliente", width=150, textvariable=tel_variable)
# label_cliente_telefono.grid(row=4, column=1, sticky=tk.EW)
# ig_variable = tk.StringVar()
# label_cliente_ig = tk.Label(frame_clients, text="ig del Cliente", width=150, textvariable=ig_variable)
# label_cliente_ig.grid(row=5, column=1, sticky=tk.EW)



# #Check Button No Cobradas
# solo_no_cobradas = tk.BooleanVar()
# checkbutton = tk.Checkbutton(frame_clients, text="Mostrar solo no cobradas", variable=solo_no_cobradas, command=on_checkbutton_changed)
# checkbutton.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)

#Lista de Clientes
list_clients = ttk.Treeview(frame_clients, columns=("ID", "Name"), height=5)

list_clients.heading("#0", text="ID")
list_clients.heading("ID", text="ID")
list_clients.heading("Name", text="Nombre")
list_clients.column("#0", stretch=tk.NO, width=0)
list_clients.column("ID", stretch=tk.NO ,width=0)
list_clients.column("Name", stretch=tk.YES, width=150)

list_clients.grid(row=2, column=0, padx=10, pady=10, sticky=tk.NSEW)

# entry_new_client.bind('<KeyRelease>', update_list)


#Lista de Prendas
garments_tree = ttk.Treeview(frame_clients, columns=("ID", "Description", "Price Real", "Price 40", "Price 50", "Cobrada", "Fecha", "Fecha_cob"))

garments_tree.heading("#0", text="Prendas")
garments_tree.heading("ID", text="ID")
garments_tree.heading("Description", text="Descripción")
garments_tree.heading("Price Real", text="Precio Real")
garments_tree.heading("Price 40", text="Precio 40")
garments_tree.heading("Price 50", text="Precio 50")
garments_tree.heading("Cobrada", text="Cobrada")
garments_tree.heading("Fecha", text="Fecha")
garments_tree.heading("Fecha_cob", text="Fecha_cob")

garments_tree.column("#0", stretch=tk.NO, width=0)
garments_tree.column("ID", stretch=tk.NO, width=0)
garments_tree.column("Description", stretch=tk.YES, width=int(window.winfo_screenwidth() * 0.2), anchor=CENTER)  # 60% of the screen width
garments_tree.column("Price Real", stretch=tk.YES, minwidth=10, width=30, anchor=CENTER)
garments_tree.column("Price 40", stretch=tk.YES, minwidth=10, width=50, anchor=CENTER)
garments_tree.column("Price 50", stretch=tk.YES, minwidth=10, width=50, anchor=CENTER)
garments_tree.column("Cobrada", stretch=tk.YES, minwidth=10, width=60, anchor=CENTER)
garments_tree.column("Fecha", stretch=tk.YES, minwidth=10, width=60, anchor=CENTER)
garments_tree.column("Fecha_cob", stretch=tk.YES, minwidth=10, width=60, anchor=CENTER)

garments_tree.grid(row=2, column=1, padx=10, pady=10, sticky=tk.NSEW)

#Acciones de clientes
btn_add_client = tk.Button(frame_clients, text="Agregar Cliente",  width=27)
btn_modif_cliente = tk.Button(frame_clients, text="Modificar Cliente",  width=27)
btn_eliminar_cliente = tk.Button(frame_clients, text="Eliminar Cliente", width=27)

btn_add_client.grid(row=3, column=0, padx=10, pady=10, sticky=tk.W)
btn_modif_cliente.grid(row=4, column=0, padx=10, pady=10, sticky=tk.W)
btn_eliminar_cliente.grid(row=5, column=0, pady=10,padx=10, sticky=tk.W)

# #Opciones de prendas
# btn_add_garment = tk.Button(frame_clients, text="Agregar Prenda", command=add_garment)
# btn_delete_garment = tk.Button(frame_clients, text="Eliminar Prenda", command=delete_garment)
# btn_ver_prendas = tk.Button(frame_clients, text="Ver Prendas", command=mostrar_prendas_fecha)
# btn_mark_as_paid = tk.Button(frame_clients, text="Cobrada", command=mark_as_paid)
# btn_mark_as_no_paid = tk.Button(frame_clients, text="No Cobrada", command=mark_as_no_paid)

# btn_add_garment.grid(row=3, column=1, pady=10, padx=10, sticky=tk.W)
# btn_delete_garment.grid(row=3, column=1, pady=5,padx=135, sticky=tk.W)
# btn_ver_prendas.grid(row=3, column=1, pady=5,padx=300, sticky=tk.W)
# btn_mark_as_paid.grid(row=3, column=1, sticky=tk.E, padx=10, pady=10)
# btn_mark_as_no_paid.grid(row=3, column=1, sticky=tk.E, pady=10, padx=100)

# list_clients.bind('<<TreeviewSelect>>', select_client)
# solo_no_cobradas.trace_add('write', on_checkbutton_changed)

# # Set weight to make the columns expand with window resizing
# frame_clients.columnconfigure(0, weight=1)
# frame_clients.rowconfigure(2, weight=1)

window.mainloop()