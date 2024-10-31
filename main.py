import tkinter as tk
from login import Login
from conexion_db import crear_tablas

def main():
    root = tk.Tk()
    root.title("Gestión de Pescadería")
    
    # Crear las tablas en la base de datos si no existen
    crear_tablas()
    
    # Iniciar con el formulario de login
    login_form = Login(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()