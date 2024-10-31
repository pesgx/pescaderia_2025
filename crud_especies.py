import tkinter as tk
from tkinter import ttk, messagebox
from conexion_db import get_db_connection

class CrudEspecies(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Especies")
        self.geometry("1200x500")
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

        tk.Label(self.frame_entrada, text="Nombre Científico:", bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5)
        self.entry_cientifico = tk.Entry(self.frame_entrada, width=30)
        self.entry_cientifico.grid(row=0, column=5, padx=5, pady=5)

        tk.Label(self.frame_entrada, text="Familia ID:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.entry_familia = tk.Entry(self.frame_entrada, width=10)
        self.entry_familia.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self.frame_entrada, text="Descripción:", bg="#f0f0f0").grid(row=1, column=2, padx=5, pady=5)
        self.entry_descripcion = tk.Entry(self.frame_entrada, width=50)
        self.entry_descripcion.grid(row=1, column=3, columnspan=3, padx=5, pady=5)

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

        self.tree = ttk.Treeview(self.frame_treeview, columns=("ID", "Código", "Nombre", "Científico", "Familia ID", "Descripción"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Código", text="Código")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Científico", text="Nombre Científico")
        self.tree.heading("Familia ID", text="Familia ID")
        self.tree.heading("Descripción", text="Descripción")
        
        self.tree.column("ID", width=50)
        self.tree.column("Código", width=70)
        self.tree.column("Nombre", width=200)
        self.tree.column("Científico", width=200)
        self.tree.column("Familia ID", width=70)
        self.tree.column("Descripción", width=300)

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
        cursor.execute("SELECT id_especie, cod_especie, nombre_especie, cientifico_especie, familia_id, descr_especie FROM tabla_especies")
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
        cientifico = self.entry_cientifico.get()
        familia = self.entry_familia.get()
        descripcion = self.entry_descripcion.get()

        if not codigo or not nombre:
            messagebox.showerror("Error", "El código y el nombre son obligatorios")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tabla_especies (cod_especie, nombre_especie, cientifico_especie, familia_id, descr_especie) VALUES (?, ?, ?, ?, ?)", 
                       (codigo, nombre, cientifico, familia, descripcion))
        conn.commit()
        conn.close()

        self.limpiar_campos()
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Especie guardada correctamente")

    def actualizar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una especie para actualizar")
            return

        id_especie = self.tree.item(selected_item)['values'][0]
        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        cientifico = self.entry_cientifico.get()
        familia = self.entry_familia.get()
        descripcion = self.entry_descripcion.get()

        if not codigo or not nombre:
            messagebox.showerror("Error", "El código y el nombre son obligatorios")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tabla_especies SET cod_especie = ?, nombre_especie = ?, cientifico_especie = ?, familia_id = ?, descr_especie = ? WHERE id_especie = ?", 
                       (codigo, nombre, cientifico, familia, descripcion, id_especie))
        conn.commit()
        conn.close()

        self.limpiar_campos()
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Especie actualizada correctamente")

    def eliminar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione una especie para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar esta especie?"):
            id_especie = self.tree.item(selected_item)['values'][0]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tabla_especies WHERE id_especie = ?", (id_especie,))
            conn.commit()
            conn.close()

            self.limpiar_campos()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Especie eliminada correctamente")

    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.entry_codigo.delete(0, tk.END)
            self.entry_codigo.insert(0, values[1])
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, values[2])
            self.entry_cientifico.delete(0, tk.END)
            self.entry_cientifico.insert(0, values[3])
            self.entry_familia.delete(0, tk.END)
            self.entry_familia.insert(0, values[4])
            self.entry_descripcion.delete(0, tk.END)
            self.entry_descripcion.insert(0, values[5])

    def limpiar_campos(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_cientifico.delete(0, tk.END)
        self.entry_familia.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CrudEspecies(root)
    root.mainloop()