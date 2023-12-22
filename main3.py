from tkinter import ttk
from tkinter import *

import sqlite3



class Product():
    def __init__(self, window):
        self.wind = window
        self.wind.title("Products")
        
        #crear frame
        frame = LabelFrame(self.wind, text="busca una persona")
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        
        #name imput
        Label(frame, text="Name").grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.grid(row=1, column=1)
        
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading("#0", text="ID", anchor=CENTER, )
        self.tree.heading("#1", text="NOMBRE", anchor=CENTER)  
        
        self.garments_tree = ttk.Treeview(frame, columns=("ID", "Description", "Price Real", "Price 40", "Price 50", "Cobrada", "Fecha"))
        self.garments_tree.grid(row=5, column=0, columnspan=2)
        
        self.garments_tree.heading("#0", text="Prendas")
        self.garments_tree.heading("ID", text="ID")
        self.garments_tree.heading("Description", text="Descripción")
        self.garments_tree.heading("Price Real", text="Precio Real")
        self.garments_tree.heading("Price 40", text="Precio 40")
        self.garments_tree.heading("Price 50", text="Precio 50")
        self.garments_tree.heading("Cobrada", text="Cobrada")
        self.garments_tree.heading("Fecha", text="Fecha")

        self.garments_tree.column("#0",stretch=0, width=0)
        self.garments_tree.column("ID",stretch=0, width=0)
        self.garments_tree.column("Description", width=int(window.winfo_screenwidth() * 0.2), anchor=CENTER)  # 60% of the screen width
        self.garments_tree.column("Price Real", minwidth=80, width=80, anchor=CENTER)
        self.garments_tree.column("Price 40", minwidth=80, width=80, anchor=CENTER)
        self.garments_tree.column("Price 50", minwidth=80, width=80, anchor=CENTER)
        self.garments_tree.column("Cobrada", minwidth=80, width=80, anchor=CENTER)
        self.garments_tree.column("Fecha", minwidth=100, width=100, anchor=CENTER)
          
        self.get_cliente()
    
    def run_query(self, query, parameters = ()):
        with sqlite3.connect("gestor_clientes.db") as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result 
        
    def get_cliente(self):
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        #quering data
        query = "SELECT * FROM clientes ORDER BY nombre DESC"
        db_rows = self.run_query(query)
        #fill data
        for row in db_rows:
            self.tree.insert('',0, text=row[0] ,values=(row[1]))
            
            
                
if __name__ == "__main__":
    window = Tk()
    application = Product(window)
    window.mainloop()