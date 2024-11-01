import sqlite3
from tkinter import messagebox

def cargar_artes(self):
    """ Carga los datos de las artes desde la base de datos y los muestra en el combobox. """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()
        # Obtener todas las artes
        cursor.execute("SELECT id_arte, nombre_arte FROM tabla_artes")
        self.artes = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Actualizar los valores del combobox
        self.actualizar_combobox_artes()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las artes: {str(e)}")

def actualizar_combobox_artes(self, filtro=""):
    """ Actualiza los valores del combobox de artes, aplicando un filtro si se proporciona. """
    valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.artes
                         if filtro.lower() in nombre.lower() or filtro in str(id_)]
    self.entry_arte_id['values'] = valores_filtrados

def buscar_arte(self, event):
    """ Busca un arte por ID cuando se presiona Enter o Enter del teclado numérico.
    Si se encuentra, completa el combobox y pasa al siguiente campo.
    
    Args:
        event: El evento de teclado que activó esta función.
    """
    entrada = self.entry_arte_id.get()
    # Verificar si la entrada es un número
    if entrada.isdigit():
        id_arte = int(entrada)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Buscar el arte
            cursor.execute("SELECT id_arte, nombre_arte FROM tabla_artes WHERE id_arte = ?", (id_arte,))
            arte = cursor.fetchone()
            # Cerrar la conexión
            conn.close()
            if arte:
                # Si se encuentra, actualizar el combobox
                self.entry_arte_id.set(f"{arte[0]} - {arte[1]}")
                # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                self.entry_factura.focus_set()
            else:
                # Si no se encuentra, mostrar un mensaje de error
                messagebox.showerror("Error", f"No se encontró un arte con ID {id_arte}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo buscar el arte: {str(e)}")
    else:
        # Si la entrada no es un número, no hacer nada
        pass

def filtrar_artes(self, event):
    """ Filtra las artes en el combobox según el texto introducido. """
    texto_filtro = self.entry_arte_id.get()
    self.actualizar_combobox_artes(texto_filtro)
