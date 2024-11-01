import sqlite3
from tkinter import messagebox

class GestionBarcos:
    def __init__(self):
        self.barcos = []
        self.cargar_barcos()

    def cargar_barcos(self):
        """ Carga los datos de los barcos desde la base de datos y los almacena en memoria. """
        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()
            # Obtener todos los barcos
            cursor.execute("SELECT id_barco, nombre_barco FROM tabla_barcos")
            self.barcos = cursor.fetchall()
            # Cerrar la conexión
            conn.close()
            # Actualizar los valores del combobox
            self.actualizar_combobox_barcos()
        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los barcos: {str(e)}")

    def actualizar_combobox_barcos(self, filtro=""):
        """ Actualiza los valores del combobox de barcos, aplicando un filtro si se proporciona. """
        valores_filtrados = [f"{id_} - {nombre}" for id_, nombre in self.barcos
                             if filtro.lower() in nombre.lower() or filtro in str(id_)]
        self.entry_barco_id['values'] = valores_filtrados

    def buscar_barco(self, event):
        """ Busca un barco por ID cuando se presiona Enter o Enter del teclado numérico.
        Si se encuentra, completa el combobox y pasa al siguiente campo.
        
        Args:
            event: El evento de teclado que activó esta función.
        """
        entrada = self.entry_barco_id.get()
        # Verificar si la entrada es un número
        if entrada.isdigit():
            id_barco = int(entrada)
            
            try:
                # Conectar a la base de datos
                conn = sqlite3.connect('pescaderia.db')
                cursor = conn.cursor()
                # Buscar el barco
                cursor.execute("SELECT id_barco, nombre_barco FROM tabla_barcos WHERE id_barco = ?", (id_barco,))
                barco = cursor.fetchone()
                # Cerrar la conexión
                conn.close()
                if barco:
                    # Si se encuentra, actualizar el combobox
                    self.entry_barco_id.set(f"{barco[0]} - {barco[1]}")
                    # Pasar al siguiente campo (en este caso, asumimos que es entry_factura)
                    self.entry_factura.focus_set()
                else:
                    # Si no se encuentra, mostrar un mensaje de error
                    messagebox.showerror("Error", f"No se encontró un barco con ID {id_barco}")
            except sqlite3.Error as e:
                messagebox.showerror("Error de Base de Datos", f"No se pudo buscar el barco: {str(e)}")
        else:
            # Si la entrada no es un número, no hacer nada
            pass

    def filtrar_barcos(self, event):
        """ Filtra los barcos en el combobox según el texto introducido. """
        texto_filtro = self.entry_barco_id.get()
        self.actualizar_combobox_barcos(texto_filtro)