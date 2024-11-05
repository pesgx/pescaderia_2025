import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import time
import datetime

# Import CRUD modules
from crud_artes import CrudArtes
from crud_especies import CrudEspecies
from crud_expedidores import CrudExpedidores
from crud_metodos import CrudMetodos
from crud_producciones import CrudProducciones
from crud_proveedores import CrudProveedores
from crud_zonas import CrudZonas
from crud_barcos import CrudBarcos
from crud_usuarios import CrudUsuarios
from crud_detalle_listado import CrudDetalleListado
from crud_presentaciones import CrudPresentaciones
from crud_familias import CrudFamilias
from conexion_db import get_db_connection

class VentanaPrincipal:
    def __init__(self, master=None):
        self.master = master or tk.Tk()
        self.master.title("Sistema de Gestión de Pescaderías")
        self.master.geometry("700x500")
        
        # Crear un estilo para los botones 
        estilo = ttk.Style()
        estilo.theme_use('clam') # Cambia el tema para asegurarte de que los colores se apliquen correctamente 
        estilo.configure("TButton", background="snow3", foreground="black", font=('Arial', 12))

        # Almacenar el usuario actual
        self.usuario_actual = None

        # Crear un frame principal
        self.frame_principal = ttk.Frame(self.master)
        self.frame_principal.pack(expand=True, fill="both", padx=5, pady=5)

        # Cargar y mostrar la imagen
        self.cargar_imagen()

        # Añadir reloj y fecha
        self.label_reloj = tk.Label(self.frame_principal, font=('Arial', 20))
        self.label_reloj.pack(pady=5)
        self.label_fecha = tk.Label(self.frame_principal, font=('Arial', 14))
        self.label_fecha.pack(pady=5)
        self.actualizar_reloj_y_fecha()

        # Añadir texto de bienvenida
        self.label_bienvenida = tk.Label(self.frame_principal, text="Bienvenido al Sistema de Gestión de Pescaderías", font=('Arial', 16, 'bold'))
        self.label_bienvenida.pack(pady=5)

        # Crear frame para los botones
        self.frame_botones = ttk.Frame(self.frame_principal)
        self.frame_botones.pack(pady=5)

        # Crear botones individualmente y distribuirlos en 3 filas
        self.btn_artes = ttk.Button(self.frame_botones, text="Gestionar Artes", command=self.abrir_crud_artes)
        self.btn_artes.grid(row=0, column=0,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_especies = ttk.Button(self.frame_botones, text="Gestionar Especies", command=self.abrir_crud_especies)
        self.btn_especies.grid(row=0, column=1,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_expedidores = ttk.Button(self.frame_botones, text="Gestionar Expedidores", command=self.abrir_crud_expedidores)
        self.btn_expedidores.grid(row=0, column=2,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_metodos = ttk.Button(self.frame_botones, text="Gestionar Métodos", command=self.abrir_crud_metodos)
        self.btn_metodos.grid(row=1, column=0,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_producciones = ttk.Button(self.frame_botones, text="Gestionar Producciones", command=self.abrir_crud_producciones)
        self.btn_producciones.grid(row=1, column=1,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_proveedores = ttk.Button(self.frame_botones, text="Gestionar Proveedores", command=self.abrir_crud_proveedores)
        self.btn_proveedores.grid(row=1, column=2,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_zonas = ttk.Button(self.frame_botones, text="Gestionar Zonas", command=self.abrir_crud_zonas)
        self.btn_zonas.grid(row=2, column=0,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_barcos = ttk.Button(self.frame_botones, text="Gestionar Barcos", command=self.abrir_crud_barcos)
        self.btn_barcos.grid(row=2, column=1,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_registros = ttk.Button(self.frame_botones, text="Gestionar Registros", command=self.abrir_crud_detalle_listado)
        self.btn_registros.grid(row=2, column=2,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_presentaciones = ttk.Button(self.frame_botones, text="Gestionar Presentaciones", command=self.abrir_crud_presentaciones)
        self.btn_presentaciones.grid(row=3, column=0,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        self.btn_familias = ttk.Button(self.frame_botones, text="Gestionar Familias", command=self.abrir_crud_familias)
        self.btn_familias.grid(row=3, column=1,padx=1, pady=1, sticky='nsew', ipadx=1, ipady=1)

        # Añadir botón de salir
        self.btn_salir = ttk.Button(self.frame_botones, text="Salir", command=self.salir)
        self.btn_salir.grid(row=4, column=0,columnspan=3, padx=5, pady=5, sticky='nsew', ipadx=5, ipady=5)

        # Crear menú
        self.crear_menu()

    def cargar_imagen(self):
        try:
            imagen = Image.open("logo_pes_png.png")
            imagen = imagen.resize((100, 100))  # Ajusta el tamaño según sea necesario
            self.logo = ImageTk.PhotoImage(imagen)
            label_imagen = tk.Label(self.frame_principal, image=self.logo)
            label_imagen.pack(pady=5)
        except FileNotFoundError:
            print("No se pudo encontrar el archivo de imagen 'logo_pes.jpg'")

    def actualizar_reloj_y_fecha(self):
        hora_actual = time.strftime('%H:%M:%S')
        fecha_actual = datetime.date.today().strftime("%d/%m/%Y")
        self.label_reloj.config(text=hora_actual)
        self.label_fecha.config(text=fecha_actual)
        self.master.after(1000, self.actualizar_reloj_y_fecha)  # Actualizar cada segundo

    def crear_menu(self):
        menu_bar = tk.Menu(self.master)
        self.master.config(menu=menu_bar)

        crud_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="CRUD", menu=crud_menu)

        crud_menu.add_command(label="Listado", command=self.abrir_crud_detalle_listado)
        crud_menu.add_command(label="Artes", command=self.abrir_crud_artes)
        crud_menu.add_command(label="Especies", command=self.abrir_crud_especies)
        crud_menu.add_command(label="Expedidores", command=self.abrir_crud_expedidores)
        crud_menu.add_command(label="Métodos", command=self.abrir_crud_metodos)
        crud_menu.add_command(label="Producciones", command=self.abrir_crud_producciones)
        crud_menu.add_command(label="Proveedores", command=self.abrir_crud_proveedores)
        crud_menu.add_command(label="Zonas", command=self.abrir_crud_zonas)
        crud_menu.add_command(label="Barcos", command=self.abrir_crud_barcos)
        crud_menu.add_command(label="Presentaciones", command=self.abrir_crud_presentaciones)
        crud_menu.add_command(label="Familias", command=self.abrir_crud_familias)
        crud_menu.add_command(label="Usuarios", command=self.abrir_crud_usuarios)

    def abrir_crud_artes(self):
        CrudArtes(self.master)

    def abrir_crud_especies(self):
        CrudEspecies(self.master)

    def abrir_crud_expedidores(self):
        CrudExpedidores(self.master)

    def abrir_crud_metodos(self):
        CrudMetodos(self.master)

    def abrir_crud_producciones(self):
        CrudProducciones(self.master)

    def abrir_crud_proveedores(self):
        CrudProveedores(self.master)

    def abrir_crud_zonas(self):
        CrudZonas(self.master)

    def abrir_crud_barcos(self):
        CrudBarcos(self.master)

    def abrir_crud_detalle_listado(self):
        CrudDetalleListado(self.master)
        self.master.withdraw()  # Oculta la ventana principal

    def abrir_crud_presentaciones(self):
        CrudPresentaciones(self.master)

    def abrir_crud_familias(self):
        CrudFamilias(self.master)

    def abrir_crud_usuarios(self):
        if self.confirmar_credenciales():
            CrudUsuarios(self.master)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas o insuficientes")

    def confirmar_credenciales(self):
        # Crear una ventana de diálogo para ingresar las credenciales
        dialog = tk.Toplevel(self.master)
        dialog.title("Confirmar Credenciales")
        dialog.geometry("300x200")
        dialog.resizable(False, False)

        tk.Label(dialog, text="Usuario:").pack(pady=5)
        entry_usuario = tk.Entry(dialog)
        entry_usuario.pack(pady=5)

        tk.Label(dialog, text="Contraseña:").pack(pady=5)
        entry_contrasena = tk.Entry(dialog, show="*")
        entry_contrasena.pack(pady=5)

        resultado = [False]  # Usamos una lista para poder modificar el valor desde dentro de la función

        def verificar():
            usuario = entry_usuario.get()
            contrasena = entry_contrasena.get()

            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tabla_usuarios WHERE nombre_usuario = ? AND clave_usuario = ? AND rol_usuario = 'admin'", (usuario, contrasena))
            user = cursor.fetchone()
            conn.close()

            if user:
                resultado[0] = True
                dialog.destroy()
            else:
                messagebox.showerror("Error", "Credenciales incorrectas o usuario no es administrador")

        # Añadir botón de verificación
        tk.Button(dialog, text="Verificar", command=verificar).pack(pady=10)

        # Esperar hasta que se cierre la ventana de diálogo
        self.master.wait_window(dialog)

        return resultado[0]

    def salir(self):
        if messagebox.askyesno("Confirmar salida", "¿Está seguro que desea salir de la aplicación?"):
            self.master.quit()

if __name__ == "__main__":
    app = VentanaPrincipal()
    app.master.mainloop()