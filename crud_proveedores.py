import tkinter as tk
from tkinter import ttk, messagebox
from conexion_db import get_db_connection
import sqlite3  # Añadimos esta importación

class CrudProveedores(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Proveedores")
        self.geometry("1000x500")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)
        
        # Frame para los campos de entrada
        self.frame_entrada = tk.Frame(self, bg="#f0f0f0")
        self.frame_entrada.pack(pady=20)

        # Campos de entrada
        tk.Label(self.frame_entrada, text="Código:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.entry_codigo = tk.Entry(self.frame_entrada, width=10)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_entrada, text="Nombre:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.entry_nombre = tk.Entry(self.frame_entrada, width=30)
        self.entry_nombre.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.frame_entrada, text="NIF:", bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5)
        self.entry_nif = tk.Entry(self.frame_entrada, width=20)
        self.entry_nif.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(self.frame_entrada, text="NRS:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.entry_nrs = tk.Entry(self.frame_entrada, width=20)
        self.entry_nrs.grid(row=1, column=1, padx=5, pady=5)

        # Frame para los botones
        self.frame_botones = tk.Frame(self, bg="#f0f0f0")
        self.frame_botones.pack(pady=10)

        # Botones
        self.btn_guardar = tk.Button(self.frame_botones, text="Guardar", command=self.guardar)
        self.btn_guardar.grid(row=0, column=0, padx=5)

        self.btn_actualizar = tk.Button(self.frame_botones, text="Actualizar", command=self.actualizar)
        self.btn_actualizar.grid(row=0, column=1, padx=5)

        self.btn_eliminar = tk.Button(self.frame_botones, text="Eliminar", command=self.eliminar)
        self.btn_eliminar.grid(row=0, column=2, padx=5)

        self.btn_salir = tk.Button(self.frame_botones, text="Salir", command=self.destroy)
        self.btn_salir.grid(row=0, column=3, padx=5)

        # Treeview
        self.frame_treeview = tk.Frame(self, bg="#f0f0f0")
        self.frame_treeview.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(self.frame_treeview, columns=("ID", "Código", "Nombre", "NIF", "NRS"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("NIF", text="NIF")
        self.tree.heading("NRS", text="NRS")
        
        self.tree.column("ID", width=50)
        self.tree.column("Código", width=100)
        self.tree.column("Nombre", width=200)
        self.tree.column("NIF", width=100)
        self.tree.column("NRS", width=100)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.frame_treeview, orient=tk.VERTICAL, command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Bind the treeview selection event
        self.tree.bind("<<TreeviewSelect>>", self.item_selected)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        # Limpiar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener datos de la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id_proveedor, cod_proveedor, nombre_proveedor, nif_proveedor, nrs_proveedor FROM tabla_proveedores")
        rows = cursor.fetchall()

        # Insertar datos en el treeview
        for row in rows:
            # Convertir el objeto sqlite3.Row a una tupla de valores
            values = tuple(row[key] for key in row.keys())
            self.tree.insert("", tk.END, values=values)

        conn.close()

    def guardar(self):
        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        nif = self.entry_nif.get()
        nrs = self.entry_nrs.get()

        if not codigo or not nombre:
            messagebox.showerror("Error", "El código y el nombre son obligatorios")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO tabla_proveedores (cod_proveedor, nombre_proveedor, nif_proveedor, nrs_proveedor) VALUES (?, ?, ?, ?)", 
                           (codigo, nombre, nif, nrs))
            conn.commit()
            self.limpiar_campos()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Proveedor guardado correctamente")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El código de proveedor ya existe")
        finally:
            conn.close()

    def actualizar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un proveedor para actualizar")
            return

        id_proveedor = self.tree.item(selected_item)['values'][0]
        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        nif = self.entry_nif.get()
        nrs = self.entry_nrs.get()

        if not codigo or not nombre:
            messagebox.showerror("Error", "El código y el nombre son obligatorios")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE tabla_proveedores SET cod_proveedor = ?, nombre_proveedor = ?, nif_proveedor = ?, nrs_proveedor = ? WHERE id_proveedor = ?", 
                           (codigo, nombre, nif, nrs, id_proveedor))
            conn.commit()
            self.limpiar_campos()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Proveedor actualizado correctamente")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El código de proveedor ya existe")
        finally:
            conn.close()

    def eliminar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un proveedor para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este proveedor?"):
            id_proveedor = self.tree.item(selected_item)['values'][0]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tabla_proveedores WHERE id_proveedor = ?", (id_proveedor,))
            conn.commit()
            conn.close()

            self.limpiar_campos()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")

    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.insert(0, values[1])
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, values[2])
            self.entry_nif.delete(0, tk.END)
            self.entry_nif.insert(0, values[3])
            self.entry_nrs.delete(0, tk.END)
            self.entry_nrs.insert(0, values[4])

    def limpiar_campos(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_nif.delete(0, tk.END)
        self.entry_nrs.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrudProveedores(root)
    root.mainloop()