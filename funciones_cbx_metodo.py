import sqlite3
from tkinter import messagebox

def cargar_metodos(self):
    """ Carga los datos de los métodos desde la base de datos y los muestra en el combobox. """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()
        # Obtener todos los métodos
        cursor.execute("SELECT id_metodo, nombre_metodo FROM tabla_metodos")
        self.metodos = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Actualizar los valores del combobox
        self.actualizar_combobox_metodos()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los métodos: {str(e)}")

def actualizar_combobox_metodos(self, filtro=""):
    """ Actualiza los valores del combobox de métodos, aplicando un filtro si se proporciona. """
    valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.metodos
                        if filtro.lower() in nombre.lower() or filtro in str(id_)]
    self.entry_metodo_id['values'] = valores_filtrados

def buscar_metodo(self, event):
    """ Busca un método por ID cuando se presiona Enter o Enter del teclado numérico.
    Si se encuentra, completa el combobox y pasa al siguiente campo.
    
    Args:
        event: El evento de teclado que activó esta función.
    """
    entrada = self.entry_metodo_id.get()
    # Verificar si la entrada es un número
    if entrada.isdigit():
        id_metodo = int(entrada)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Buscar el método
            cursor.execute("SELECT id_metodo, nombre_metodo FROM tabla_metodos WHERE id_metodo = ?", (id_metodo,))
            metodo = cursor.fetchone()
            # Cerrar la conexión
            conn.close()
            if metodo:
                # Si se encuentra, actualizar el combobox
                self.entry_metodo_id.set(f"{metodo[0]} - {metodo[1]}")
                # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                self.entry_factura.focus_set()
            else:
                # Si no se encuentra, mostrar un mensaje de error
                messagebox.showerror("Error", f"No se encontró un método con ID {id_metodo}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo buscar el método: {str(e)}")
    else:
        # Si la entrada no es un número, no hacer nada
        pass

def filtrar_metodos(self, event):
    """ Filtra los métodos en el combobox según el texto introducido. """
    texto_filtro = self.entry_metodo_id.get()
    self.actualizar_combobox_metodos(texto_filtro)
