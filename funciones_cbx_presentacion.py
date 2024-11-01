import sqlite3
from tkinter import messagebox

def cargar_presentaciones(self):
    """ Carga los datos de las presentaciones desde la base de datos y los muestra en el combobox. """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()
        # Obtener todas las presentaciones
        cursor.execute("SELECT id_presentacion, nombre_presentacion FROM tabla_presentaciones")
        self.presentaciones = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Actualizar los valores del combobox
        self.actualizar_combobox_presentaciones()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las presentaciones: {str(e)}")

def actualizar_combobox_presentaciones(self, filtro=""):
    """ Actualiza los valores del combobox de presentaciones, aplicando un filtro si se proporciona. """
    valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.presentaciones
                        if filtro.lower() in nombre.lower() or filtro in str(id_)]
    self.entry_presentacion_id['values'] = valores_filtrados

def buscar_presentacion(self, event):
    """ Busca una presentación por ID cuando se presiona Enter o Enter del teclado numérico.
    Si se encuentra, completa el combobox y pasa al siguiente campo.
    
    Args:
        event: El evento de teclado que activó esta función.
    """
    entrada = self.entry_presentacion_id.get()
    # Verificar si la entrada es un número
    if entrada.isdigit():
        id_presentacion = int(entrada)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Buscar la presentación
            cursor.execute("SELECT id_presentacion, nombre_presentacion FROM tabla_presentaciones WHERE id_presentacion = ?", (id_presentacion,))
            presentacion = cursor.fetchone()
            # Cerrar la conexión
            conn.close()
            if presentacion:
                # Si se encuentra, actualizar el combobox
                self.entry_presentacion_id.set(f"{presentacion[0]} - {presentacion[1]}")
                # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                self.entry_barco.focus_set()
            else:
                # Si no se encuentra, mostrar un mensaje de error
                messagebox.showerror("Error", f"No se encontró una presentación con ID {id_presentacion}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo buscar la presentación: {str(e)}")
    else:
        # Si la entrada no es un número, no hacer nada
        pass

def filtrar_presentaciones(self, event):
    """ Filtra las presentaciones en el combobox según el texto introducido. """
    texto_filtro = self.entry_presentacion_id.get()
    self.actualizar_combobox_presentaciones(texto_filtro)
