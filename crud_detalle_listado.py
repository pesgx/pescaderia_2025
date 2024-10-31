import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3

class CrudDetalleListado(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        
        # Configuración básica de la ventana
        self.title("Gestión de Detalle de Listado")
        self.geometry("1200x800")

        # Frame principal
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Frame línea uno (datos principales)
        self.frame_linea_uno = ttk.LabelFrame(self.main_frame, text="Datos Principales")
        self.frame_linea_uno.pack(fill=tk.X, padx=5, pady=5)

        # Frame línea dos (datos adicionales)
        self.frame_linea_dos = ttk.LabelFrame(self.main_frame, text="Datos Adicionales")
        self.frame_linea_dos.pack(fill=tk.X, padx=5, pady=5)

        # Campos en frame_linea_uno (4 columnas)
        # Columna 1
        ttk.Label(self.frame_linea_uno, text="ID Detalle:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_id_detalle = ttk.Entry(self.frame_linea_uno)
        self.entry_id_detalle.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="Listado ID:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_listado_id = ttk.Entry(self.frame_linea_uno)
        self.entry_listado_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="Fecha:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_fecha = DateEntry(self.frame_linea_uno, width=12, background='darkblue', 
                                     foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.entry_fecha.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="Proveedor:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_proveedor_id = ttk.Combobox(self.frame_linea_uno)
        self.entry_proveedor_id.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.entry_proveedor_id.bind('<Return>', self.buscar_proveedor)
        self.entry_proveedor_id.bind('<KP_Enter>', self.buscar_proveedor)
        self.entry_proveedor_id.bind('<KeyRelease>', self.filtrar_proveedores)


        ttk.Label(self.frame_linea_uno, text="Factura:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.entry_factura = ttk.Entry(self.frame_linea_uno)
        self.entry_factura.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="Especie:").grid(row=2, column=2, padx=5, pady=5, sticky='e')
        self.entry_especie_id = ttk.Combobox(self.frame_linea_uno)
        self.entry_especie_id.grid(row=2, column=3, padx=5, pady=5, sticky='w')
        self.entry_especie_id.bind('<Return>', self.buscar_especie)
        self.entry_especie_id.bind('<KP_Enter>', self.buscar_especie)
        self.entry_especie_id.bind('<KeyRelease>', self.filtrar_especies)

        # Columna 3
        ttk.Label(self.frame_linea_uno, text="Compra (€):").grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.entry_compra = ttk.Entry(self.frame_linea_uno)
        self.entry_compra.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="Cantidad:").grid(row=1, column=4, padx=5, pady=5, sticky='e')
        self.entry_cantidad = ttk.Entry(self.frame_linea_uno)
        self.entry_cantidad.grid(row=1, column=5, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="IVA (%):").grid(row=2, column=4, padx=5, pady=5, sticky='e')
        self.entry_iva = ttk.Entry(self.frame_linea_uno)
        self.entry_iva.grid(row=2, column=5, padx=5, pady=5, sticky='w')

        # Columna 4
        ttk.Label(self.frame_linea_uno, text="Costo (€):").grid(row=0, column=6, padx=5, pady=5, sticky='e')
        self.entry_costo = ttk.Entry(self.frame_linea_uno)
        self.entry_costo.grid(row=0, column=7, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="Porcentaje:").grid(row=1, column=6, padx=5, pady=5, sticky='e')
        self.entry_porcentaje = ttk.Entry(self.frame_linea_uno)
        self.entry_porcentaje.grid(row=1, column=7, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="Beneficio (€):").grid(row=2, column=6, padx=5, pady=5, sticky='e')
        self.entry_beneficio = ttk.Entry(self.frame_linea_uno)
        self.entry_beneficio.grid(row=2, column=7, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_uno, text="PVP (€):").grid(row=3, column=6, padx=5, pady=5, sticky='e')
        self.entry_pvp = ttk.Entry(self.frame_linea_uno)
        self.entry_pvp.grid(row=3, column=7, padx=5, pady=5, sticky='w')

        # Campos en frame_linea_dos (4 columnas)
        # Columna 1
        ttk.Label(self.frame_linea_dos, text="Zona:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_zona_id = ttk.Combobox(self.frame_linea_dos, state="readonly")
        self.entry_zona_id.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_dos, text="Expedidor:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_expedidor_id = ttk.Combobox(self.frame_linea_dos, state="readonly")
        self.entry_expedidor_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        # Columna 2
        ttk.Label(self.frame_linea_dos, text="Producción:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_produccion_id = ttk.Combobox(self.frame_linea_dos, state="readonly")
        self.entry_produccion_id.grid(row=0, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_dos, text="Arte:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.entry_arte_id = ttk.Combobox(self.frame_linea_dos, state="readonly")
        self.entry_arte_id.grid(row=1, column=3, padx=5, pady=5, sticky='w')

        # Columna 3
        ttk.Label(self.frame_linea_dos, text="Método:").grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.entry_metodo_id = ttk.Combobox(self.frame_linea_dos, state="readonly")
        self.entry_metodo_id.grid(row=0, column=5, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_dos, text="Presentación:").grid(row=1, column=4, padx=5, pady=5, sticky='e')
        self.entry_presentacion_id = ttk.Combobox(self.frame_linea_dos, state="readonly")
        self.entry_presentacion_id.grid(row=1, column=5, padx=5, pady=5, sticky='w')

        # Columna 4
        ttk.Label(self.frame_linea_dos, text="Barco:").grid(row=0, column=6, padx=5, pady=5, sticky='e')
        self.entry_barco_id = ttk.Combobox(self.frame_linea_dos, state="readonly")
        self.entry_barco_id.grid(row=0, column=7, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_dos, text="Descongelado:").grid(row=1, column=6, padx=5, pady=5, sticky='e')
        self.entry_descongelado = ttk.Checkbutton(self.frame_linea_dos)
        self.entry_descongelado.grid(row=1, column=7, padx=5, pady=5, sticky='w')

        # Campos adicionales
        ttk.Label(self.frame_linea_dos, text="Lote Externo:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.entry_lote_ext = ttk.Entry(self.frame_linea_dos)
        self.entry_lote_ext.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_dos, text="Lote Interno:").grid(row=2, column=2, padx=5, pady=5, sticky='e')
        self.entry_lote_int = ttk.Entry(self.frame_linea_dos)
        self.entry_lote_int.grid(row=2, column=3, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_dos, text="Nota Externa:").grid(row=2, column=4, padx=5, pady=5, sticky='e')
        self.entry_nota_ext = ttk.Entry(self.frame_linea_dos)
        self.entry_nota_ext.grid(row=2, column=5, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_dos, text="Nota Interna:").grid(row=2, column=6, padx=5, pady=5, sticky='e')
        self.entry_nota_int = ttk.Entry(self.frame_linea_dos)
        self.entry_nota_int.grid(row=2, column=7, padx=5, pady=5, sticky='w')

        ttk.Label(self.frame_linea_dos, text="Reg. Congelado:").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.entry_reg_congelado = ttk.Checkbutton(self.frame_linea_dos)
        self.entry_reg_congelado.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        # Frame para botones CRUD
        self.frame_botones = ttk.LabelFrame(self.main_frame, text="Operaciones")
        self.frame_botones.pack(fill=tk.X, padx=5, pady=5)

        # Botones CRUD
        self.btn_anadir = ttk.Button(self.frame_botones, text="AÑADIR")
        self.btn_anadir.grid(row=0, column=0, padx=5, pady=5)

        self.btn_actualizar = ttk.Button(self.frame_botones, text="ACTUALIZAR")
        self.btn_actualizar.grid(row=0, column=1, padx=5, pady=5)

        self.btn_eliminar = ttk.Button(self.frame_botones, text="ELIMINAR")
        self.btn_eliminar.grid(row=0, column=2, padx=5, pady=5)

        self.btn_salir = ttk.Button(self.frame_botones, text="SALIR")
        self.btn_salir.grid(row=0, column=3, padx=5, pady=5)

        # Frame para el Treeview
        self.frame_treeview = ttk.LabelFrame(self.main_frame, text="Listado de Registros")
        self.frame_treeview.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configuración del Treeview
        columnas = ("id_detalle", "fecha", "proveedor", "especie", "pvp", "nota_int")
        self.tree = ttk.Treeview(self.frame_treeview, columns=columnas, show='headings')

        # Configurar las columnas
        self.tree.heading("id_detalle", text="ID")
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("proveedor", text="Proveedor")
        self.tree.heading("especie", text="Especie")
        self.tree.heading("pvp", text="PVP")
        self.tree.heading("nota_int", text="Nota Interna")

        # Ajustar el ancho de las columnas
        self.tree.column("id_detalle", width=50)
        self.tree.column("fecha", width=100)
        self.tree.column("proveedor", width=150)
        self.tree.column("especie", width=150)
        self.tree.column("pvp", width=100)
        
        self.tree.column("nota_int", width=200)

        # Añadir scrollbar
        scrollbar = ttk.Scrollbar(self.frame_treeview, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Cargar datos de COMBOBOX
        self.cargar_proveedores()
        self.cargar_especies()

#############################################################################################
#############################################################################################
########################        FUNCIONES PROVEEDORES     #####################################
#############################################################################################
#############################################################################################
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

#############################################################################################
#############################################################################################
########################        FUNCIONES ESPECIES      #####################################
#############################################################################################
#############################################################################################
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

if __name__ == "__main__":
    root = tk.Tk()
    app = CrudDetalleListado(root)
    root.mainloop()