import tkinter as tk
from tkinter import ttk, messagebox
from conexion_db import get_db_connection

class CrudZonas(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Zonas")
        self.geometry("800x400")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)
        
        # Frame para los campos de entrada
        self.frame_entrada = tk.Frame(self, bg="#f0f0f0")
        self.frame_entrada.pack(pady=20)

        # Campos de entrada
        tk.Label(self.frame_entrada, text="Nombre:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(self.frame_entrada, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_entrada, text="Descripción:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.entry_descripcion = tk.Entry(self.frame_entrada, width=50)
        self.entry_descripcion.grid(row=0, column=3, padx=5, pady=5)

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

        self.tree = ttk.Treeview(self.frame_treeview, columns=("ID", "Nombre", "Descripción"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Descripción", text="Descripción")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=200)
        self.tree.column("Descripción", width=400)

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
        cursor.execute("SELECT id_zona, nombre_zona, descr_zona FROM tabla_zonas")
        rows = cursor.fetchall()

        # Insertar datos en el treeview
        for row in rows:
            self.tree.insert("", tk.END, values=(row['id_zona'], row['nombre_zona'], row['descr_zona']))

        conn.close()

    def guardar(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tabla_zonas (nombre_zona, descr_zona) VALUES (?, ?)", (nombre, descripcion))
        conn.commit()
        conn.close()

        self.limpiar_campos()
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Zona guardada correctamente")

    def actualizar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una zona para actualizar")
            return

        id_zona = self.tree.item(selected_item)['values'][0]
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tabla_zonas SET nombre_zona = ?, descr_zona = ? WHERE id_zona = ?", (nombre, descripcion, id_zona))
        conn.commit()
        conn.close()

        self.limpiar_campos()
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Zona actualizada correctamente")

    def eliminar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una zona para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta zona?"):
            id_zona = self.tree.item(selected_item)['values'][0]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tabla_zonas WHERE id_zona = ?", (id_zona,))
            conn.commit()
            conn.close()

            self.limpiar_campos()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Zona eliminada correctamente")
    
    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)


    def item_selected(self, event):
        selected_item = self.tree