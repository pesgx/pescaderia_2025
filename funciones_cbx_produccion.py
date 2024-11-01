import sqlite3
from tkinter import messagebox

def cargar_producciones(self):
    """ Carga los datos de las producciones desde la base de datos y los muestra en el combobox. """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()
        # Obtener todas las producciones
        cursor.execute("SELECT id_produccion, nombre_produccion FROM tabla_producciones")
        self.producciones = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Actualizar los valores del combobox
        self.actualizar_combobox_producciones()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las producciones: {str(e)}")

def actualizar_combobox_producciones(self, filtro=""):
    """ Actualiza los valores del combobox de producciones, aplicando un filtro si se proporciona. """
    valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.producciones
                         if filtro.lower() in nombre.lower() or filtro in str(id_)]
    self.entry_produccion_id['values'] = valores_filtrados

def buscar_produccion(self, event):
    """ Busca una producción por ID cuando se presiona Enter o Enter del teclado numérico.
    Si se encuentra, completa el combobox y pasa al siguiente campo.
    
    Args:
        event: El evento de teclado que activó esta función.
    """
    entrada = self.entry_produccion_id.get()
    # Verificar si la entrada es un número
    if entrada.isdigit():
        id_produccion = int(entrada)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Buscar la producción
            cursor.execute("SELECT id_produccion, nombre_produccion FROM tabla_producciones WHERE id_produccion = ?", (id_produccion,))
            produccion = cursor.fetchone()
            # Cerrar la conexión
            conn.close()
            if produccion:
                # Si se encuentra, actualizar el combobox
                self.entry_produccion_id.set(f"{produccion[0]} - {produccion[1]}")
                # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                self.entry_factura.focus_set()
            else:
                # Si no se encuentra, mostrar un mensaje de error
                messagebox.showerror("Error", f"No se encontró una producción con ID {id_produccion}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo buscar la producción: {str(e)}")
    else:
        # Si la entrada no es un número, no hacer nada
        pass

def filtrar_producciones(self, event):
    """ Filtra las producciones en el combobox según el texto introducido. """
    texto_filtro = self.entry_produccion_id.get()
    self.actualizar_combobox_producciones(texto_filtro)
