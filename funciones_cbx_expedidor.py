import sqlite3
from tkinter import messagebox

def cargar_expedidores(self):
    """ Carga los datos de los expedidores desde la base de datos y los muestra en el combobox. """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()
        # Obtener todos los expedidores
        cursor.execute("SELECT id_expedidor, nombre_expedidor FROM tabla_expedidores")
        self.expedidores = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Actualizar los valores del combobox
        self.actualizar_combobox_expedidores()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los expedidores: {str(e)}")

def actualizar_combobox_expedidores(self, filtro=""):
    """ Actualiza los valores del combobox de expedidores, aplicando un filtro si se proporciona. """
    valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.expedidores
                         if filtro.lower() in nombre.lower() or filtro in str(id_)]
    self.entry_expedidor_id['values'] = valores_filtrados

def buscar_expedidor(self, event):
    """ Busca un expedidor por ID cuando se presiona Enter o Enter del teclado numérico.
    Si se encuentra, completa el combobox y pasa al siguiente campo.
    
    Args:
        event: El evento de teclado que activó esta función.
    """
    entrada = self.entry_expedidor_id.get()
    # Verificar si la entrada es un número
    if entrada.isdigit():
        id_expedidor = int(entrada)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Buscar el expedidor
            cursor.execute("SELECT id_expedidor, nombre_expedidor FROM tabla_expedidores WHERE id_expedidor = ?", (id_expedidor,))
            expedidor = cursor.fetchone()
            # Cerrar la conexión
            conn.close()
            if expedidor:
                # Si se encuentra, actualizar el combobox
                self.entry_expedidor_id.set(f"{expedidor[0]} - {expedidor[1]}")
                # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                self.entry_factura.focus_set()
            else:
                # Si no se encuentra, mostrar un mensaje de error
                messagebox.showerror("Error", f"No se encontró un expedidor con ID {id_expedidor}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo buscar el expedidor: {str(e)}")
    else:
        # Si la entrada no es un número, no hacer nada
        pass

def filtrar_expedidores(self, event):
    """ Filtra los expedidores en el combobox según el texto introducido. """
    texto_filtro = self.entry_expedidor_id.get()
    self.actualizar_combobox_expedidores(texto_filtro)
