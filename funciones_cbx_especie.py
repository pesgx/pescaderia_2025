import sqlite3
from tkinter import messagebox

def cargar_especies(self):
    """
    Carga los datos de las especies desde la base de datos y los muestra en el combobox. 
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()
        # Obtener todas las especies
        cursor.execute("SELECT id_especie, nombre_especie FROM tabla_especies")
        self.especies = cursor.fetchall()
        # Cerrar la conexión
        conn.close()
        # Actualizar los valores del combobox
        self.actualizar_combobox_especies()
    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar las especies: {str(e)}")

def actualizar_combobox_especies(self, filtro=""):
    """
    Actualiza los valores del combobox de especies, aplicando un filtro si se proporciona. 
    """
    valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.especies
                         if filtro.lower() in nombre.lower() or filtro in str(id_)]
    self.entry_especie_id['values'] = valores_filtrados

def buscar_especie(self, event):
    """
    Busca una especie por ID cuando se presiona Enter o Enter del teclado numérico.
    Si se encuentra, completa el combobox y pasa al siguiente campo.
    
    Args:
        event: El evento de teclado que activó esta función.
    """
    entrada = self.entry_especie_id.get()
    # Verificar si la entrada es un número
    if entrada.isdigit():
        id_especie = int(entrada)
        
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Buscar la especie
            cursor.execute("SELECT id_especie, nombre_especie FROM tabla_especies WHERE id_especie = ?", (id_especie,))
            especie = cursor.fetchone()
            # Cerrar la conexión
            conn.close()
            if especie:
                # Si se encuentra, actualizar el combobox
                self.entry_especie_id.set(f"{especie[0]} - {especie[1]}")
                # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                self.entry_factura.focus_set()
            else:
                # Si no se encuentra, mostrar un mensaje de error
                messagebox.showerror("Error", f"No se encontró una especie con ID {id_especie}")
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo buscar la especie: {str(e)}")
    else:
        # Si la entrada no es un número, no hacer nada
        pass

def filtrar_especies(self, event):
    """
    Filtra las especies en el combobox según el texto introducido. 
    """
    texto_filtro = self.entry_especie_id.get()
    self.actualizar_combobox_especies(texto_filtro)
