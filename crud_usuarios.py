import tkinter as tk
from tkinter import ttk, messagebox
from conexion_db import get_db_connection

class CrudUsuarios(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Gestión de Usuarios")
        self.geometry("800x400")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)
        
        # Frame para los campos de entrada
        self.frame_entrada = tk.Frame(self, bg="#f0f0f0")
        self.frame_entrada.pack(pady=20)

        # Campos de entrada
        tk.Label(self.frame_entrada, text="Nombre de Usuario:", bg="#f0f0f0").grid(row=0, column=0, padx=5, pady=5)
        self.entry_nombre = tk.Entry(self.frame_entrada, width=30)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frame_entrada, text="Contraseña:", bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.entry_contrasena = tk.Entry(self.frame_entrada, width=30, show="*")
        self.entry_contrasena.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(self.frame_entrada, text="Rol:", bg="#f0f0f0").grid(row=1, column=0, padx=5, pady=5)
        self.entry_rol = tk.Entry(self.frame_entrada, width=30)
        self.entry_rol.grid(row=1, column=1, padx=5, pady=5)

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

        self.tree = ttk.Treeview(self.frame_treeview, columns=("ID", "Nombre", "Rol"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre de Usuario")
        self.tree.heading("Rol", text="Rol")
        
        self.tree.column("ID", width=50)
        self.tree.column("Nombre", width=200)
        self.tree.column("Rol", width=150)

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
        cursor.execute("SELECT id_usuario, nombre_usuario, rol_usuario FROM tabla_usuarios")
        rows = cursor.fetchall()

        # Insertar datos en el treeview
        for row in rows:
            self.tree.insert("", tk.END, values=tuple(row))

        conn.close()
########################
# def cargar_datos(self):
#     # Limpiar treeview
#     for item in self.tree.get_children():
#         self.tree.delete(item)
#     # Obtener datos de la base de datos
#     conn = get_db_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT id_usuario, nombre_usuario, rol_usuario FROM tabla_usuarios")
#     rows = cursor.fetchall()
#     # Insertar datos en el treeview
#     for row in rows:
#         self.tree.insert("", tk.END, values=tuple(row))
#     conn.close()


    def guardar(self):
        nombre = self.entry_nombre.get()
        contrasena = self.entry_contrasena.get()
        rol = self.entry_rol.get()

        if not nombre or not contrasena or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tabla_usuarios (nombre_usuario, clave_usuario, rol_usuario) VALUES (?, ?, ?)", 
                       (nombre, contrasena, rol))
        conn.commit()
        conn.close()

        self.limpiar_campos()
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Usuario guardado correctamente")

    def actualizar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un usuario para actualizar")
            return

        id_usuario = self.tree.item(selected_item)['values'][0]
        nombre = self.entry_nombre.get()
        contrasena = self.entry_contrasena.get()
        rol = self.entry_rol.get()

        if not nombre or not contrasena or not rol:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tabla_usuarios SET nombre_usuario = ?, clave_usuario = ?, rol_usuario = ? WHERE id_usuario = ?", 
                       (nombre, contrasena, rol, id_usuario))
        conn.commit()
        conn.close()

        self.limpiar_campos()
        self.cargar_datos()
        messagebox.showinfo("Éxito", "Usuario actualizado correctamente")

    def eliminar(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Por favor, seleccione un usuario para eliminar")
            return

        if messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este usuario?"):
            id_usuario = self.tree.item(selected_item)['values'][0]

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tabla_usuarios WHERE id_usuario = ?", (id_usuario,))
            conn.commit()
            conn.close()

            self.limpiar_campos()
            self.cargar_datos()
            messagebox.showinfo("Éxito", "Usuario eliminado correctamente")

    def item_selected(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item)['values']
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, values[1])
            self.entry_rol.delete(0, tk.END)
            self.entry_rol.insert(0, values[2])
            # No mostramos la contraseña por seguridad
            self.entry_contrasena.delete(0, tk.END)

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_contrasena.delete(0, tk.END)
        self.entry_rol.delete(0, tk.END)
