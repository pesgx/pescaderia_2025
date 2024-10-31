import tkinter as tk
from tkinter import ttk, messagebox
from conexion_db import get_db_connection

class CrudProducciones(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Producciones")
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
        cursor.execute("SELECT id_produccion, nombre_produccion, descr_produccion FROM tabla_producciones")
        rows = cursor.fetchall()

        # Insertar datos en el treeview
        for row in rows:
            self.tree.insert("", tk.END, values=(row['id_produccion'], row['nombre_produccion'], row['descr_produccion']))

        conn.close()

    def guardar(self):
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tabla_producciones (nombre_produccion, descr_produccion) VALUES (?, ?)", (nombre, descripcion))
        conn.commit()
        conn.close()

        self.limpiar_campos()
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Producción guardada correctamente")

    def actualizar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una producción para actualizar")
            return

        id_produccion = self.tree.item(selected_item)['values'][0]
        nombre = self.entry_nombre.get()
        descripcion = self.entry_descripcion.get()

        if not nombre:
            messagebox.showerror("Error", "El nombre es obligatorio")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tabla_producciones SET nombre_produccion = ?, descr_produccion = ? WHERE id_produccion = ?", (nombre, descripcion, id_produccion))
        conn.commit()
        conn.close()

        self.limpiar_campos()
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Producción actualizada correctamente")

    def eliminar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una producción para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta producción?"):
            id_produccion = self.tree.item(selected_item)['values'][0]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tabla_producciones WHERE id_produccion = ?", (id_produccion,))
            conn.commit()
            conn.close()

            self.limpiar_campos()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Producción eliminada correctamente")

    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, values[1])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, values[2])

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrudProducciones(root)
    root.mainloop()