import sqlite3
from tkinter import messagebox

def cargar_proveedores(self):
    """
    Carga los datos de los proveedores desde la base de datos y los muestra en el combobox.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()
        # Obtener todos los proveedores
        cursor.execute("SELECT id_proveedor, nombre_proveedor FROM tabla_proveedores")
        self.proveedores = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Actualizar los valores del combobox
        self.actualizar_combobox_proveedores()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los proveedores: {str(e)}")

def actualizar_combobox_proveedores(self, filtro=""):
    """
    Actualiza los valores del combobox de proveedores, aplicando un filtro si se proporciona.
    """
    valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.proveedores 
                            if filtro.lower() in nombre.lower() or filtro in str(id_)]
    self.entry_proveedor_id['values'] = valores_filtrados

def buscar_proveedor(self, event):
    """
    Busca un proveedor por ID cuando se presiona Enter o Enter del teclado numérico.
    Si se encuentra, completa el combobox y pasa al siguiente campo.
    
    Args:
        event: El evento de teclado que activó esta función.
    """
    entrada = self.entry_proveedor_id.get()

    # Verificar si la entrada es un número
    if entrada.isdigit():
        id_proveedor = int(entrada)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Buscar el proveedor
            cursor.execute("SELECT id_proveedor, nombre_proveedor FROM tabla_proveedores WHERE id_proveedor = ?", (id_proveedor,))
            proveedor = cursor.fetchone()
            # Cerrar la conexión
            conn.close()
            if proveedor:
                # Si se encuentra, actualizar el combobox
                self.entry_proveedor_id.set(f"{proveedor[0]} - {proveedor[1]}")
                # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                self.entry_factura.focus_set()
            else:
                # Si no se encuentra, mostrar un mensaje de error
                messagebox.showerror("Error", f"No se encontró un proveedor con ID {id_proveedor}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo buscar el proveedor: {str(e)}")
    else:
        # Si la entrada no es un número, no hacer nada
        pass
def filtrar_proveedores(self, event):
    """
    Filtra los proveedores en el combobox según el texto introducido.
    """
    texto_filtro = self.entry_proveedor_id.get()
    self.actualizar_combobox_proveedores(texto_filtro)