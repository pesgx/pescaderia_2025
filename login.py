import tkinter as tk
from tkinter import messagebox
from conexion_db import get_db_connection
from ventana_principal import VentanaPrincipal

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("300x150")

        self.label_usuario = tk.Label(root, text="Usuario:")
        self.label_usuario.pack()
        self.entry_usuario = tk.Entry(root)
        self.entry_usuario.pack()

        self.label_password = tk.Label(root, text="Contraseña:")
        self.label_password.pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()

        self.btn_login = tk.Button(root, text="Iniciar sesión", command=self.login)
        self.btn_login.pack(pady=10)

    def login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if self.verificar_credenciales(usuario, password):
            messagebox.showinfo("Login exitoso", "Bienvenido al sistema")
            self.root.destroy()  # Cerrar ventana de login
            self.abrir_ventana_principal()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def verificar_credenciales(self, usuario, password):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tabla_usuarios WHERE nombre_usuario = ? AND clave_usuario = ?", (usuario, password))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    def abrir_ventana_principal(self):
        ventana_principal = tk.Tk()
        app = VentanaPrincipal(ventana_principal)
        ventana_principal.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    login = Login(root)
    root.mainloop()