import sqlite3
from tkinter import Tk, Button, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Función para generar el PDF
def generar_pdf():
    # Conexión a la base de datos
    try:
        conn = sqlite3.connect("pescaderia.db")
        cursor = conn.cursor()
        
        # Consulta de los datos en la vista ETIQUETA_PDF
        cursor.execute("SELECT * FROM ETIQUETA_PDF")
        registros = cursor.fetchall()
        
        # Verificar si hay registros
        if not registros:
            messagebox.showinfo("Información", "No hay registros en la vista ETIQUETA_PDF")
            return
        
        # Crear el archivo PDF
        nombre_pdf = "etiquetas_chat.pdf"
        c = canvas.Canvas(nombre_pdf, pagesize=A4)
        
        # Configurar el tamaño y la posición inicial
        ancho, alto = A4
        margen_y = alto - 30  # Margen superior inicial

        # Altura mínima entre filas
        espacio_vertical = 12  # Ajustado para mejorar el espaciado

        for registro in registros:
            # Desempaquetar los datos y convertir cada campo en texto
            especie, cientifico_especie, pvp, zona, expedidor, produccion, arte, metodo, presentacion, barco, descongelado, lote_ext, lote_int, nota_ext = map(str, registro)
            
            # Nombre de la especie en tamaño 16
            c.setFont("Helvetica-Bold", 16)
            c.drawCentredString(ancho / 2, margen_y, especie)

            # PVP en tamaño 16
            c.setFont("Helvetica", 16)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 2, f"{pvp}€")
            
            # Otros campos en tamaño 5, organizados en dos columnas compartiendo filas donde corresponde
            c.setFont("Helvetica-Bold", 5)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 4, "Nombre Científico")
            c.setFont("Helvetica", 5)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 5, cientifico_especie)
            
            # Zona y Expedidor en la misma fila
            c.setFont("Helvetica-Bold", 5)
            c.drawString(ancho / 4, margen_y - espacio_vertical * 6, "Zona:")
            c.drawString(ancho / 2, margen_y - espacio_vertical * 6, "Expedidor:")
            c.setFont("Helvetica", 5)
            c.drawString(ancho / 4, margen_y - espacio_vertical * 7, zona)
            c.drawString(ancho / 2, margen_y - espacio_vertical * 7, expedidor)

            # Producción y Arte en la misma fila
            c.setFont("Helvetica-Bold", 5)
            c.drawString(ancho / 4, margen_y - espacio_vertical * 8, "Producción:")
            c.drawString(ancho / 2, margen_y - espacio_vertical * 8, "Arte:")
            c.setFont("Helvetica", 5)
            c.drawString(ancho / 4, margen_y - espacio_vertical * 9, produccion)
            c.drawString(ancho / 2, margen_y - espacio_vertical * 9, arte)
            
            # Método y Presentación en la misma fila
            c.setFont("Helvetica-Bold", 5)
            c.drawString(ancho / 4, margen_y - espacio_vertical * 10, "Método:")
            c.drawString(ancho / 2, margen_y - espacio_vertical * 10, "Presentación:")
            c.setFont("Helvetica", 5)
            c.drawString(ancho / 4, margen_y - espacio_vertical * 11, metodo)
            c.drawString(ancho / 2, margen_y - espacio_vertical * 11, presentacion)
            
            # Barco y Descongelado en la misma fila
            c.setFont("Helvetica-Bold", 5)
            c.drawString(ancho / 4, margen_y - espacio_vertical * 12, "Barco:")
            c.drawString(ancho / 2, margen_y - espacio_vertical * 12, "Descongelado:")
            c.setFont("Helvetica", 5)
            c.drawString(ancho / 4, margen_y - espacio_vertical * 13, barco)
            c.drawString(ancho / 2, margen_y - espacio_vertical * 13, descongelado)
            
            # Lote Externo en una fila independiente
            c.setFont("Helvetica-Bold", 5)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 14, "Lote Externo")
            c.setFont("Helvetica", 5)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 15, lote_ext)
            
            # Lote Interno en una fila independiente
            c.setFont("Helvetica-Bold", 5)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 16, "Lote Interno")
            c.setFont("Helvetica", 5)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 17, lote_int)
            
            # Nota Externa en una fila independiente
            c.setFont("Helvetica-Bold", 5)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 18, "Nota Externa")
            c.setFont("Helvetica", 5)
            c.drawCentredString(ancho / 2, margen_y - espacio_vertical * 19, nota_ext)
            
            # Pasar a la siguiente etiqueta
            c.showPage()
        
        # Guardar y cerrar el PDF
        c.save()
        conn.close()
        
        # Mensaje de éxito
        messagebox.showinfo("Éxito", f"PDF generado exitosamente: {nombre_pdf}")
        
    except sqlite3.Error as e:
        messagebox.showerror("Error", f"Error al acceder a la base de datos: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el PDF: {e}")

# Configuración de la interfaz gráfica con tkinter
def iniciar_app():
    # Crear la ventana principal
    ventana = Tk()
    ventana.title("Generador de Etiquetas de Producto en PDF")
    ventana.geometry("300x100")
    
    # Botón para generar el PDF
    boton_generar = Button(ventana, text="Generar PDF", command=generar_pdf)
    boton_generar.pack(pady=20)
    
    # Ejecutar la aplicación
    ventana.mainloop()

# Iniciar la aplicación
if __name__ == "__main__":
    iniciar_app()
