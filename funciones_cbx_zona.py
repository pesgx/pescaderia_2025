import sqlite3
from tkinter import messagebox

def cargar_zonas(self):
    """ Carga los datos de las zonas desde la base de datos y los muestra en el combobox. """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()
        # Obtener todas las zonas
        cursor.execute("SELECT id_zona, nombre_zona FROM tabla_zonas")
        self.zonas = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Actualizar los valores del combobox
        self.actualizar_combobox_zonas()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las zonas: {str(e)}")

def actualizar_combobox_zonas(self, filtro=""):
    """ Actualiza los valores del combobox de zonas, aplicando un filtro si se proporciona. """
    valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.zonas
                         if filtro.lower() in nombre.lower() or filtro in str(id_)]
    self.entry_zona_id['values'] = valores_filtrados

def buscar_zona(self, event):
    """ Busca una zona por ID cuando se presiona Enter o Enter del teclado numérico.
    Si se encuentra, completa el combobox y pasa al siguiente campo.
    
    Args:
        event: El evento de teclado que activó esta función.
    """
    entrada = self.entry_zona_id.get()
    # Verificar si la entrada es un número
    if entrada.isdigit():
        id_zona = int(entrada)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Buscar la zona
            cursor.execute("SELECT id_zona, nombre_zona FROM tabla_zonas WHERE id_zona = ?", (id_zona,))
            zona = cursor.fetchone()
            # Cerrar la conexión
            conn.close()
            if zona:
                # Si se encuentra, actualizar el combobox
                self.entry_zona_id.set(f"{zona[0]} - {zona[1]}")
                # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                self.entry_factura.focus_set()
            else:
                # Si no se encuentra, mostrar un mensaje de error
                messagebox.showerror("Error", f"No se encontró una zona con ID {id_zona}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo buscar la zona: {str(e)}")
    else:
        # Si la entrada no es un número, no hacer nada
        pass

def filtrar_zonas(self, event):
    """ Filtra las zonas en el combobox según el texto introducido. """
    texto_filtro = self.entry_zona_id.get()
    self.actualizar_combobox_zonas(texto_filtro)
