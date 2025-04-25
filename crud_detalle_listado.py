import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from tkinter import filedialog
from generar_pdf import generar_pdf_consulta  # Importar la función desde el nuevo módulo


class CrudDetalleListado(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)

        # botones de función especial
        self.bind('<F2>', self.seleccionar_primera_linea)
        self.bind('<F3>', self.actualizar_registro)
        
        # Configuración básica de la ventana
        self.title("Gestión de Detalle de Listado")
        self.geometry("1200x850")

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
        self.entry_compra.bind('<FocusOut>', self.validar_y_calcular)


        ttk.Label(self.frame_linea_uno, text="Cantidad:").grid(row=1, column=4, padx=5, pady=5, sticky='e')
        self.entry_cantidad = ttk.Entry(self.frame_linea_uno,)
        self.entry_cantidad.grid(row=1, column=5, padx=5, pady=5, sticky='w')
        self.entry_cantidad.bind('<FocusOut>', self.validar_y_calcular)
 

        ttk.Label(self.frame_linea_uno, text="IVA (%):").grid(row=2, column=4, padx=5, pady=5, sticky='e')
        self.entry_iva = ttk.Entry(self.frame_linea_uno)
        self.entry_iva.grid(row=2, column=5, padx=5, pady=5, sticky='w')
        self.entry_iva.bind('<FocusOut>', self.validar_y_calcular)
 

        # Columna 4
        ttk.Label(self.frame_linea_uno, text="Costo (€):").grid(row=0, column=6, padx=5, pady=5, sticky='e')
        self.entry_costo = ttk.Entry(self.frame_linea_uno)
        self.entry_costo.grid(row=0, column=7, padx=5, pady=5, sticky='w')
        # DESACTIVAMOS PARA QUE NO SE PUEDA MODIFICAR
        self.entry_costo.config(state='disabled')

        ttk.Label(self.frame_linea_uno, text="Porcentaje:").grid(row=1, column=6, padx=5, pady=5, sticky='e')
        self.entry_porcentaje = ttk.Entry(self.frame_linea_uno)
        self.entry_porcentaje.grid(row=1, column=7, padx=5, pady=5, sticky='w')
        self.entry_porcentaje.bind('<FocusOut>', self.validar_y_calcular)


        ttk.Label(self.frame_linea_uno, text="Beneficio (€):").grid(row=2, column=6, padx=5, pady=5, sticky='e')
        self.entry_beneficio = ttk.Entry(self.frame_linea_uno)
        self.entry_beneficio.grid(row=2, column=7, padx=5, pady=5, sticky='w')
        # DESACTIVAMOS PARA QUE NO SE PUEDA MODIFICAR
        self.entry_beneficio.config(state='disabled')

        ttk.Label(self.frame_linea_uno, text="PVP (€):").grid(row=3, column=6, padx=5, pady=5, sticky='e')
        self.entry_pvp = ttk.Entry(self.frame_linea_uno)
        self.entry_pvp.grid(row=3, column=7, padx=5, pady=5, sticky='w')
        # DESACTIVAMOS PARA QUE NO SE PUEDA MODIFICAR
        self.entry_pvp.config(state='disabled')

        # Campos en frame_linea_dos (4 columnas)
        # Columna 1
        ttk.Label(self.frame_linea_dos, text="Zona:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.entry_zona_id = ttk.Combobox(self.frame_linea_dos)
        self.entry_zona_id.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.entry_zona_id.bind('<Return>', self.buscar_zona)
        self.entry_zona_id.bind('<KP_Enter>', self.buscar_zona)
        self.entry_zona_id.bind('<KeyRelease>', self.filtrar_zonas)

        ttk.Label(self.frame_linea_dos, text="Expedidor:").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.entry_expedidor_id = ttk.Combobox(self.frame_linea_dos)
        self.entry_expedidor_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.entry_expedidor_id.bind('<Return>', self.buscar_expedidor)
        self.entry_expedidor_id.bind('<KP_Enter>', self.buscar_expedidor)
        self.entry_expedidor_id.bind('<KeyRelease>', self.filtrar_expedidores)

        # Columna 2
        ttk.Label(self.frame_linea_dos, text="Producción:").grid(row=0, column=2, padx=5, pady=5, sticky='e')
        self.entry_produccion_id = ttk.Combobox(self.frame_linea_dos)
        self.entry_produccion_id.grid(row=0, column=3, padx=5, pady=5, sticky='w')
        self.entry_produccion_id.bind('<Return>', self.buscar_produccion)
        self.entry_produccion_id.bind('<KP_Enter>', self.buscar_produccion)
        self.entry_produccion_id.bind('<KeyRelease>', self.filtrar_producciones)

        ttk.Label(self.frame_linea_dos, text="Arte:").grid(row=1, column=2, padx=5, pady=5, sticky='e')
        self.entry_arte_id = ttk.Combobox(self.frame_linea_dos)
        self.entry_arte_id.grid(row=1, column=3, padx=5, pady=5, sticky='w')
        self.entry_arte_id.bind('<Return>', self.buscar_arte)
        self.entry_arte_id.bind('<KP_Enter>', self.buscar_arte)
        self.entry_arte_id.bind('<KeyRelease>', self.filtrar_artes)

        # Columna 3
        ttk.Label(self.frame_linea_dos, text="Método:").grid(row=0, column=4, padx=5, pady=5, sticky='e')
        self.entry_metodo_id = ttk.Combobox(self.frame_linea_dos)
        self.entry_metodo_id.grid(row=0, column=5, padx=5, pady=5, sticky='w')
        self.entry_metodo_id.bind('<Return>', self.buscar_metodo)
        self.entry_metodo_id.bind('<KP_Enter>', self.buscar_metodo)
        self.entry_metodo_id.bind('<KeyRelease>', self.filtrar_metodos)

        ttk.Label(self.frame_linea_dos, text="Presentación:").grid(row=1, column=4, padx=5, pady=5, sticky='e')
        self.entry_presentacion_id = ttk.Combobox(self.frame_linea_dos)
        self.entry_presentacion_id.grid(row=1, column=5, padx=5, pady=5, sticky='w')
        self.entry_presentacion_id.bind('<Return>', self.buscar_presentacion)
        self.entry_presentacion_id.bind('<KP_Enter>', self.buscar_presentacion)
        self.entry_presentacion_id.bind('<KeyRelease>', self.filtrar_presentaciones)

        # Columna 4
        ttk.Label(self.frame_linea_dos, text="Barco:").grid(row=0, column=6, padx=5, pady=5, sticky='e')
        self.entry_barco_id = ttk.Combobox(self.frame_linea_dos)
        self.entry_barco_id.grid(row=0, column=7, padx=5, pady=5, sticky='w')
        self.entry_barco_id.bind('<Return>', self.buscar_barco)
        self.entry_barco_id.bind('<KP_Enter>', self.buscar_barco)
        self.entry_barco_id.bind('<KeyRelease>', self.filtrar_barcos)

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
        def anadir_registro_wrapper():
            self.anadir_registro()
            self.limpiar_campos()

        def actualizar_registro_wrapper():
            self.actualizar_registro()
            self.limpiar_campos()

        def eliminar_registro_wrapper():
            self.eliminar_registro()
            self.limpiar_campos()
        # Botones CRUD
        self.btn_anadir = ttk.Button(self.frame_botones, text="AÑADIR")
        self.btn_anadir.grid(row=0, column=0, padx=5, pady=5)
        self.btn_anadir.config(command=anadir_registro_wrapper)

        self.btn_actualizar = ttk.Button(self.frame_botones, text="ACTUALIZAR")
        self.btn_actualizar.grid(row=0, column=1, padx=5, pady=5)
        self.btn_actualizar.config(command=actualizar_registro_wrapper)

        self.btn_eliminar = ttk.Button(self.frame_botones, text="ELIMINAR")
        self.btn_eliminar.grid(row=0, column=2, padx=5, pady=5)
        self.btn_eliminar.config(command=eliminar_registro_wrapper)

        self.btn_pdf = ttk.Button(self.frame_botones, text="PDF")
        self.btn_pdf.grid(row=0, column=3, padx=5, pady=5)
        self.btn_pdf.config(command=generar_pdf_consulta)  # Vincular al módulo externo

        self.btn_salir = ttk.Button(self.frame_botones, text="SALIR")
        self.btn_salir.grid(row=0, column=4, padx=5, pady=5)
        self.btn_salir.config(command=self.volver_a_ventana_principal)

        lbl_label_opcines = ttk.Label(self.frame_botones, text="F2: Seleccionar primera línea tabla")
        lbl_label_opcines.grid(row=1, column=0, padx=5, pady=5)
        lbl_label_opcines.config(foreground="blue")

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
        self.tree.bind('<<TreeviewSelect>>', self.seleccionar_registro)       
        # Cargar datos de COMBOBOX
        self.cargar_proveedores()
        self.cargar_especies()
        self.cargar_zonas()
        self.cargar_expedidores()
        self.cargar_producciones()
        self.cargar_artes()
        self.cargar_metodos()
        self.cargar_presentaciones()
        self.cargar_barcos()
        # Cargar los registros iniciales
        self.cargar_registros()
        # Eventos de teclado
        self.entry_proveedor_id.bind('<Return>', self.buscar_proveedor)
        self.entry_especie_id.bind('<Return>', self.buscar_especie)
        self.entry_zona_id.bind('<Return>', self.buscar_zona)
        self.entry_expedidor_id.bind('<Return>', self.buscar_expedidor)
        self.entry_produccion_id.bind('<Return>', self.buscar_produccion)
        self.entry_arte_id.bind('<Return>',self.buscar_arte)
        self.entry_metodo_id.bind('<Return>',self.buscar_metodo)
        self.entry_presentacion_id.bind('<Return>',self.buscar_presentacion)
        self.entry_barco_id.bind('<Return>',self.buscar_barco)

#############################################################################################
#############################################################################################
########################        OTROS METODOS     ###########################################
#############################################################################################
#############################################################################################
    def validar_y_calcular(self, event=None):
        """
        Valida los valores de los campos y calcula automáticamente los valores de costo, beneficio y PVP.
        Si los valores no son numéricos, muestra un mensaje de error y borra el campo.
        """
        try:
            # Validar que los campos no estén vacíos y contengan valores numéricos
            compra = self.entry_compra.get()
            cantidad = self.entry_cantidad.get()
            iva = self.entry_iva.get()
            porcentaje = self.entry_porcentaje.get()

            if not compra or not cantidad or not iva or not porcentaje:
                return  # No hacer nada si algún campo está vacío

            # Intentar convertir los valores a float
            compra = float(compra)
            cantidad = float(cantidad)
            iva = float(iva)
            porcentaje = float(porcentaje)

            # Validar que cantidad no sea cero para evitar división por cero
            if cantidad == 0:
                raise ValueError("La cantidad no puede ser cero.")

            # Realizar cálculos
            costo = (compra / cantidad) * (1 + iva / 100)
            beneficio = costo * (porcentaje / 100)
            pvp = costo + beneficio

            # Actualizar los campos calculados
            self.entry_costo.config(state='normal')
            self.entry_costo.delete(0, tk.END)
            self.entry_costo.insert(0, f"{costo:.2f}")
            self.entry_costo.config(state='disabled')

            self.entry_beneficio.config(state='normal')
            self.entry_beneficio.delete(0, tk.END)
            self.entry_beneficio.insert(0, f"{beneficio:.2f}")
            self.entry_beneficio.config(state='disabled')

            self.entry_pvp.config(state='normal')
            self.entry_pvp.delete(0, tk.END)
            self.entry_pvp.insert(0, f"{pvp:.2f}")
            self.entry_pvp.config(state='disabled')

        except ValueError:
            # Si ocurre un error, mostrar mensaje y borrar el campo que generó el evento
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
            widget = event.widget  # Obtener el widget que generó el evento
            widget.delete(0, tk.END)


    def volver_a_ventana_principal(self):
        """
        Oculta la ventana actual y vuelve a mostrar la ventana principal.
        """
        self.destroy()  # Cierra la ventana actual
        self.master.deiconify()  # Muestra la ventana principal
    
    def seleccionar_primera_linea(self, event=None):
        """
        Selecciona la primera línea del Treeview.
        """
    # Vincular la tecla F2 al evento        
        if self.tree.get_children():
            primera_linea = self.tree.get_children()[0]
            self.tree.selection_set(primera_linea)
            self.tree.focus(primera_linea)
            self.tree.see(primera_linea)
            self.tree.focus_set()  # Asegura que el foco permanezca en el Treeview


    def limpiar_campos(self):
            """
            Limpia todos los campos del formulario.
            """
            self.entry_id_detalle.delete(0, tk.END)
            self.entry_listado_id.delete(0, tk.END)
            self.entry_fecha.set_date(None)
            self.entry_proveedor_id.set('')
            self.entry_factura.delete(0, tk.END)
            self.entry_especie_id.set('')
            self.entry_compra.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.entry_iva.delete(0, tk.END)
            self.entry_costo.delete(0, tk.END)
            self.entry_porcentaje.delete(0, tk.END)
            self.entry_beneficio.delete(0, tk.END)
            self.entry_pvp.delete(0, tk.END)
            self.entry_zona_id.set('')
            self.entry_expedidor_id.set('')
            self.entry_produccion_id.set('')
            self.entry_arte_id.set('')
            self.entry_metodo_id.set('')
            self.entry_presentacion_id.set('')
            self.entry_barco_id.set('')
            self.entry_descongelado.state(['!selected'])
            self.entry_lote_ext.delete(0, tk.END)
            self.entry_lote_int.delete(0, tk.END)
            self.entry_nota_ext.delete(0, tk.END)
            self.entry_nota_int.delete(0, tk.END)
            self.entry_reg_congelado.state(['!selected'])

    def seleccionar_registro(self, event):
            """
            Completa los campos del formulario con los datos del registro seleccionado en el treeview.
            """
            # Obtener el ítem seleccionado
            seleccion = self.tree.selection()
            if not seleccion:
                return

            # Obtener los valores del ítem seleccionado
            valores = self.tree.item(seleccion)['values']

            # Limpiar los campos actuales
            self.limpiar_campos()

            # Obtener los datos completos del registro seleccionado
            try:
                conn = sqlite3.connect('pescaderia.db')
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT dl.*, 
                        p.nombre_proveedor, 
                        e.nombre_especie,
                        z.nombre_zona,
                        ex.nombre_expedidor,
                        pr.nombre_produccion,
                        a.nombre_arte,
                        m.nombre_metodo,
                        pres.nombre_presentacion,
                        b.nombre_barco
                    FROM tabla_detalle_listado dl
                    LEFT JOIN tabla_proveedores p ON dl.proveedor_id = p.id_proveedor
                    LEFT JOIN tabla_especies e ON dl.especie_id = e.id_especie
                    LEFT JOIN tabla_zonas z ON dl.zona_id = z.id_zona
                    LEFT JOIN tabla_expedidores ex ON dl.expedidor_id = ex.id_expedidor
                    LEFT JOIN tabla_producciones pr ON dl.produccion_id = pr.id_produccion
                    LEFT JOIN tabla_artes a ON dl.arte_id = a.id_arte
                    LEFT JOIN tabla_metodos m ON dl.metodo_id = m.id_metodo
                    LEFT JOIN tabla_presentaciones pres ON dl.presentacion_id = pres.id_presentacion
                    LEFT JOIN tabla_barcos b ON dl.barco_id = b.id_barco
                    WHERE dl.id_detalle = ?
                """, (valores[0],))
                registro = cursor.fetchone()

                if registro:
                    # Llenar los campos con los datos del registro
                    self.entry_id_detalle.insert(0, registro[0])
                    self.entry_listado_id.insert(0, registro[1])

                    # Manejo de diferentes formatos de fecha
                    fecha_str = registro[2]
                    try:
                        fecha = datetime.strptime(fecha_str, '%d/%m/%Y').date()
                    except ValueError:
                        try:
                            fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
                        except ValueError:
                            fecha = datetime.now().date()
                            print(f"Formato de fecha no reconocido: {fecha_str}. Usando la fecha actual.")

                    self.entry_fecha.set_date(fecha)

                    # Configurar comboboxes con ID y nombre
                    self.entry_proveedor_id.set(f"{registro[3]} - {registro[26]}")
                    self.entry_factura.insert(0, registro[4])
                    self.entry_especie_id.set(f"{registro[5]} - {registro[27]}")
                    self.entry_compra.insert(0, registro[6])
                    self.entry_cantidad.insert(0, registro[7])
                    self.entry_iva.insert(0, registro[8])
                    self.entry_costo.insert(0, registro[9])
                    self.entry_porcentaje.insert(0, registro[10])
                    self.entry_beneficio.insert(0, registro[11])
                    self.entry_pvp.insert(0, registro[12])
                    self.entry_zona_id.set(f"{registro[13]} - {registro[28]}")
                    self.entry_expedidor_id.set(f"{registro[14]} - {registro[29]}")
                    self.entry_produccion_id.set(f"{registro[15]} - {registro[30]}")
                    self.entry_arte_id.set(f"{registro[16]} - {registro[31]}")
                    self.entry_metodo_id.set(f"{registro[17]} - {registro[32]}")
                    self.entry_presentacion_id.set(f"{registro[18]} - {registro[33]}")
                    self.entry_barco_id.set(f"{registro[19]} - {registro[34]}")

                    if registro[20]:
                        self.entry_descongelado.state(['selected'])
                    else:
                        self.entry_descongelado.state(['!selected'])
                    self.entry_lote_ext.insert(0, registro[21])
                    self.entry_lote_int.insert(0, registro[22])
                    self.entry_nota_ext.insert(0, registro[23])
                    self.entry_nota_int.insert(0, registro[24])
                    if registro[25]:
                        self.entry_reg_congelado.state(['selected'])
                    else:
                        self.entry_reg_congelado.state(['!selected'])

            except sqlite3.Error as e:
                messagebox.showerror("Error de Base de Datos", f"No se pudo cargar el registro: {str(e)}")
            finally:
                if conn:
                    conn.close()

    def generar_pdf_consulta(self):
        # Ocultar la ventana principal de tkinter
        self.withdraw()
        
        # Abrir diálogo para seleccionar ubicación y nombre de archivo
        pdf_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar archivo PDF"
        )
        
        # Volver a mostrar la ventana principal si se cancela la operación
        self.deiconify()
        
        if not pdf_path:
            print("Operación cancelada por el usuario.")
            return

        # Conectar a la base de datos SQLite
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()

        # Ejecutar la consulta para obtener solo las columnas especificadas de la vista
        cursor.execute("SELECT fecha, especie, pvp, nota_int FROM consulta_detalle_listado")
        registros = cursor.fetchall()

        # Crear el archivo PDF con margen de 5 mm
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setTitle("Consulta Detalle Listado")

        # Crear una tabla con los datos específicos
        data = [["Fecha", "Especie", "PVP (€)", "Nota Interna"]]  # Encabezados de las columnas

        # Agregar filas de datos con formato
        for row in registros:
            fecha = row[0] or ""
            especie = row[1] or ""
            pvp = f"{row[2]:,.2f} €" if row[2] is not None else ""  # Formato de moneda
            nota_int = row[3] or ""
            data.append([fecha, especie, pvp, nota_int])

        # Establecer el estilo de la tabla
        table = Table(data, colWidths=[60, 150, 70, 200])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 1), (0, -1), 'CENTER'),       # Alineación de 'fecha' al centro
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),         # Alineación de 'nombre_especie' a la izquierda
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),        # Alineación de 'pvp' a la derecha
            ('ALIGN', (3, 1), (3, -1), 'CENTER'),       # Alineación de 'nota_int' al centro
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ]))

        # Dibujar la tabla en el PDF, iniciando en la esquina superior izquierda con margen de 5 mm
        table.wrapOn(c, 5, 5)
        table.drawOn(c, 5, 780)  # Ajusta la posición vertical si es necesario

        # Guardar y cerrar el PDF
        c.save()
        conn.close()
        print(f"PDF generado exitosamente en {pdf_path}")
#############################################################################################
#############################################################################################
########################        METODOS CRUD     #####################################
#############################################################################################
#############################################################################################
    def anadir_registro(self):
        """
        Añade un nuevo registro a la tabla_detalle_listado.
        """
        try:
            # Obtener los valores de los campos
            valores = self.obtener_valores_campos()

            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()

            # Preparar la consulta SQL
            sql = """
            INSERT INTO tabla_detalle_listado (
                listado_id, fecha, proveedor_id, factura, especie_id, compra, cantidad, iva, costo,
                porcentaje, beneficio, pvp, zona_id, expedidor_id, produccion_id, arte_id, metodo_id,
                presentacion_id, barco_id, descongelado, lote_ext, lote_int, nota_ext, nota_int, reg_congelado
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            # Ejecutar la consulta
            cursor.execute(sql, valores)
            conn.commit()

            messagebox.showinfo("Éxito", "Registro añadido correctamente")

            # Actualizar el treeview
            self.cargar_registros()

        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo añadir el registro: {str(e)}")
        finally:
            if conn:
                conn.close()

    def actualizar_registro(self,event=None):
        """
        Actualiza un registro existente en la tabla_detalle_listado.
        """
        try:
            # Obtener el ID del registro seleccionado
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, seleccione un registro para actualizar")
                return

            id_detalle = self.tree.item(seleccion)['values'][0]

            # Obtener los valores actualizados de los campos
            valores = self.obtener_valores_campos()

            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()

            # Preparar la consulta SQL
            sql = """
            UPDATE tabla_detalle_listado SET
                listado_id=?, fecha=?, proveedor_id=?, factura=?, especie_id=?, compra=?, cantidad=?,
                iva=?, costo=?, porcentaje=?, beneficio=?, pvp=?, zona_id=?, expedidor_id=?,
                produccion_id=?, arte_id=?, metodo_id=?, presentacion_id=?, barco_id=?, descongelado=?,
                lote_ext=?, lote_int=?, nota_ext=?, nota_int=?, reg_congelado=?
            WHERE id_detalle=?
            """

            # Ejecutar la consulta
            cursor.execute(sql, valores + (id_detalle,))
            conn.commit()

            messagebox.showinfo("Éxito", "Registro actualizado correctamente")

            # Actualizar el treeview
            self.cargar_registros()
            self.limpiar_campos()
            self.seleccionar_primera_linea()
            

        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo actualizar el registro: {str(e)}")
        finally:
            if conn:
                conn.close()

    def eliminar_registro(self):
        """
        Elimina un registro existente de la tabla_detalle_listado.
        """
        try:
            # Obtener el ID del registro seleccionado
            seleccion = self.tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Por favor, seleccione un registro para eliminar")
                return

            id_detalle = self.tree.item(seleccion)['values'][0]

            # Confirmar la eliminación
            if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este registro?"):
                return

            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()

            # Preparar la consulta SQL
            sql = "DELETE FROM tabla_detalle_listado WHERE id_detalle=?"

            # Ejecutar la consulta
            cursor.execute(sql, (id_detalle,))
            conn.commit()

            messagebox.showinfo("Éxito", "Registro eliminado correctamente")

            # Actualizar el treeview
            self.cargar_registros()

        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudo eliminar el registro: {str(e)}")
        finally:
            if conn:
                conn.close()

    def obtener_valores_campos(self):
        """
        Obtiene los valores de todos los campos de entrada.
        """
        return (
            self.entry_listado_id.get(),
            self.entry_fecha.get(),
            self.entry_proveedor_id.get().split(' - ')[0],  # Asumiendo que el formato es "ID - Nombre"
            self.entry_factura.get(),
            self.entry_especie_id.get().split(' - ')[0],
            self.entry_compra.get(),
            self.entry_cantidad.get(),
            self.entry_iva.get(),
            self.entry_costo.get(),
            self.entry_porcentaje.get(),
            self.entry_beneficio.get(),
            self.entry_pvp.get(),
            self.entry_zona_id.get().split(' - ')[0],
            self.entry_expedidor_id.get().split(' - ')[0],
            self.entry_produccion_id.get().split(' - ')[0],
            self.entry_arte_id.get().split(' - ')[0],
            self.entry_metodo_id.get().split(' - ')[0],
            self.entry_presentacion_id.get().split(' - ')[0],
            self.entry_barco_id.get().split(' - ')[0],
            1 if self.entry_descongelado.instate(['selected']) else 0,
            self.entry_lote_ext.get(),
            self.entry_lote_int.get(),
            self.entry_nota_ext.get(),
            self.entry_nota_int.get(),
            1 if self.entry_reg_congelado.instate(['selected']) else 0
        )

    def cargar_registros(self):
        """
        Carga los registros de la tabla_detalle_listado en el treeview.
        """
        # Limpiar el treeview
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            # Conectar a la base de datos
            conn = sqlite3.connect('pescaderia.db')
            cursor = conn.cursor()

            # Obtener los registros
            cursor.execute("""
                SELECT dl.id_detalle, dl.fecha, p.nombre_proveedor, e.nombre_especie, dl.pvp, dl.nota_int
                FROM tabla_detalle_listado dl
                LEFT JOIN tabla_proveedores p ON dl.proveedor_id = p.id_proveedor
                LEFT JOIN tabla_especies e ON dl.especie_id = e.id_especie
                ORDER BY e.nombre_especie;
            """)
            registros = cursor.fetchall()

            # Insertar los registros en el treeview
            for registro in registros:
                self.tree.insert('', 'end', values=registro)

        except sqlite3.Error as e:
            messagebox.showerror("Error de Base de Datos", f"No se pudieron cargar los registros: {str(e)}")
        finally:
            if conn:
                conn.close()

    def limpiar_campos(self):
            """
            Limpia todos los campos del formulario.
            """
            self.entry_id_detalle.delete(0, tk.END)
            self.entry_listado_id.delete(0, tk.END)
            self.entry_fecha.set_date(None)
            self.entry_proveedor_id.set('')
            self.entry_factura.delete(0, tk.END)
            self.entry_especie_id.set('')
            self.entry_compra.delete(0, tk.END)
            self.entry_cantidad.delete(0, tk.END)
            self.entry_iva.delete(0, tk.END)
            self.entry_costo.delete(0, tk.END)
            self.entry_porcentaje.delete(0, tk.END)
            self.entry_beneficio.delete(0, tk.END)
            self.entry_pvp.delete(0, tk.END)
            self.entry_zona_id.set('')
            self.entry_expedidor_id.set('')
            self.entry_produccion_id.set('')
            self.entry_arte_id.set('')
            self.entry_metodo_id.set('')
            self.entry_presentacion_id.set('')
            self.entry_barco_id.set('')
            self.entry_descongelado.state(['!selected'])
            self.entry_lote_ext.delete(0, tk.END)
            self.entry_lote_int.delete(0, tk.END)
            self.entry_nota_ext.delete(0, tk.END)
            self.entry_nota_int.delete(0, tk.END)
            self.entry_reg_congelado.state(['!selected'])
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
                    self.entry_compra.focus_set()
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

#############################################################################################
#############################################################################################
########################        FUNCIONES ZONAS      #####################################
#############################################################################################
#############################################################################################
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
                    self.entry_expedidor_id.focus_set()
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

#############################################################################################
#############################################################################################
########################        FUNCIONES EXPEDIDORES      #####################################
#############################################################################################
#############################################################################################
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
                    self.entry_produccion_id.focus_set()
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

#############################################################################################
#############################################################################################
########################        FUNCIONES PRODUCCIONES      #################################
#############################################################################################
#############################################################################################
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
                    self.entry_arte_id.focus_set()
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

#############################################################################################
#############################################################################################
########################        FUNCIONES ARTES      ########################################
#############################################################################################
#############################################################################################
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
                    self.entry_metodo_id.focus_set()
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

#############################################################################################
#############################################################################################
########################        FUNCIONES METODOS      ######################################
#############################################################################################
#############################################################################################
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
                    self.entry_presentacion_id.focus_set()
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

#############################################################################################
#############################################################################################
########################        FUNCIONES PRESENTACIONES      ###############################
#############################################################################################
#############################################################################################
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
                    self.entry_barco_id.focus_set()
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

#############################################################################################
#############################################################################################
########################        FUNCIONES BARCOS      #######################################
#############################################################################################
#############################################################################################
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
                    self.entry_descongelado.focus_set()
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




if __name__ == "__main__":
    root = tk.Tk()
    app = CrudDetalleListado(root)
    root.mainloop()