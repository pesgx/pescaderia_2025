import tkinter as tk
from tkinter import messagebox
import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def generar_pdf_etiquetas():
    """
    Función principal para generar un PDF con etiquetas de productos.
    Obtiene datos de la base de datos y crea una etiqueta por cada registro.
    """
    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()

        # Ejecutar la consulta
        cursor.execute("SELECT * FROM ETIQUETA_PDF")
        registros = cursor.fetchall()

        # Configurar el PDF
        pdf_filename = "etiquetas_v0.pdf"
        c = canvas.Canvas(pdf_filename, pagesize=A4)
        width, height = A4

        # Configurar tamaños de fuente
        tamano_normal = 6
        tamano_grande = 20

        # Posición inicial
        x = width / 2
        y = height - 10 * mm  # Reducido el margen superior

        for registro in registros:
            # Extraer datos del registro
            especie, cientifico, pvp, zona, expedidor, produccion, arte, metodo, presentacion, barco, descongelado, lote_ext, lote_int, nota_ext = registro

            # Dibujar cada campo centrado
            c.setFont("Helvetica-Bold", tamano_grande)
            c.drawCentredString(x, y, f"{especie}")
            y -= 8 * mm  # Reducido el espacio entre líneas

            c.setFont("Helvetica", tamano_normal)
            c.drawCentredString(x, y, f"Nombre científico: {cientifico}")
            y -= 4 * mm  # Reducido el espacio entre líneas

            c.setFont("Helvetica-Bold", tamano_grande)
            c.drawCentredString(x, y, f"PVP: {pvp} €")
            y -= 8 * mm  # Reducido el espacio entre líneas

            c.setFont("Helvetica", tamano_normal)
            c.drawCentredString(x, y, f"Zona de captura: {zona}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Expedidor: {expedidor}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Producción: {produccion}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Arte de pesca: {arte}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Método: {metodo}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Presentación: {presentacion}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Barco: {barco}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Descongelado: {'Sí' if descongelado else 'No'}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Lote externo: {lote_ext}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Lote interno: {lote_int}")
            y -= 4 * mm
            c.drawCentredString(x, y, f"Nota: {nota_ext}")

            # Nueva página para la siguiente etiqueta
            c.showPage()
            y = height - 10 * mm  # Reiniciar la posición Y para la nueva página

        # Guardar el PDF
        c.save()

        messagebox.showinfo("Éxito", f"PDF generado con éxito: {pdf_filename}")

    except sqlite3.Error as e:
        messagebox.showerror("Error de base de datos", f"Ocurrió un error con la base de datos: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")
    finally:
        if conn:
            conn.close()

# Crear la ventana principal de Tkinter
root = tk.Tk()
root.title("Generador de Etiquetas PDF")

# Botón para generar el PDF
btn_generar = tk.Button(root, text="Generar PDF de Etiquetas", command=generar_pdf_etiquetas)
btn_generar.pack(pady=20)

# Iniciar el bucle principal de Tkinter
root.mainloop()