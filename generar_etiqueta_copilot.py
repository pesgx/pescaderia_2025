import sqlite3
from tkinter import Tk, Button, Label, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

def generar_pdf():
    """
    Función para generar un PDF con las etiquetas de productos a partir de la vista ETIQUETA_PDF en la base de datos pescaderia.db
    """
    # Conectar a la base de datos
    conn = sqlite3.connect('pescaderia.db')
    cursor = conn.cursor()

    # Consulta para obtener los datos de la vista ETIQUETA_PDF
    cursor.execute('SELECT * FROM ETIQUETA_PDF')
    registros = cursor.fetchall()

    if not registros:
        messagebox.showinfo("Información", "No hay datos disponibles en la vista ETIQUETA_PDF.")
        return

    # Crear el documento PDF
    archivo_pdf = "etiquetas_copilot.pdf"
    doc = SimpleDocTemplate(archivo_pdf, pagesize=A4)
    
    # Estilos para el documento
    estilos = getSampleStyleSheet()
    estilo_normal = ParagraphStyle(name='Normal', fontSize=5, alignment=1)
    estilo_especie = ParagraphStyle(name='Especie', fontSize=16, alignment=1)
    estilo_pvp = ParagraphStyle(name='PVP', fontSize=16, alignment=1)

    # Lista para almacenar los elementos del documento
    elementos = []

    for registro in registros:
        especie, cientifico_especie, pvp, zona, expedidor, produccion, arte, metodo, presentacion, barco, descongelado, lote_ext, lote_int, nota_ext = registro

        # Crear las líneas de texto para cada etiqueta
        lineas = [
            Paragraph(f"<b>{especie}</b>", estilo_especie),
            Paragraph(f"<b>Nombre Científico:</b> {cientifico_especie}", estilo_normal),
            Paragraph(f"{pvp}", estilo_pvp),
            Paragraph(f"<b>Zona:</b> {zona}", estilo_normal),
            Paragraph(f"<b>Expedidor:</b> {expedidor}", estilo_normal),
            Paragraph(f"<b>Producción:</b> {produccion}", estilo_normal),
            Paragraph(f"<b>Arte:</b> {arte}", estilo_normal),
            Paragraph(f"<b>Método:</b> {metodo}", estilo_normal),
            Paragraph(f"<b>Presentación:</b> {presentacion}", estilo_normal),
            Paragraph(f"<b>Barco:</b> {barco}", estilo_normal),
            Paragraph(f"<b>Descongelado:</b> {descongelado}", estilo_normal),
            Paragraph(f"<b>Lote Ext:</b> {lote_ext}", estilo_normal),
            Paragraph(f"<b>Lote Int:</b> {lote_int}", estilo_normal),
            Paragraph(f"<b>Nota Ext:</b> {nota_ext}", estilo_normal)
        ]

        # Añadir una tabla con una sola celda para centrar los datos y reducir la altura entre filas
        tabla = Table([[linea] for linea in lineas], colWidths=[doc.width])
        tabla.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 5),
            ('FONTSIZE', (0, 0), (0, 0), 16),  # tamaño para <nombre_especie>
            ('FONTSIZE', (2, 0), (2, 0), 16),  # tamaño para <pvp>
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1)  # altura mínima entre filas
        ]))

        elementos.append(tabla)
        elementos.append(Paragraph('<br/><br/>', estilo_normal))  # espacio entre etiquetas

    # Construir el documento PDF
    doc.build(elementos)

    messagebox.showinfo("Éxito", f"PDF generado exitosamente: {archivo_pdf}")

# Crear la interfaz gráfica con tkinter
def crear_interfaz():
    """
    Función para crear la interfaz gráfica de la aplicación.
    """
    raiz = Tk()
    raiz.title("Generador de Etiquetas de Productos")

    # Etiqueta de instrucciones
    Label(raiz, text="Generar etiquetas de productos en PDF").pack(pady=10)

    # Botón para generar el PDF
    Button(raiz, text="Generar PDF", command=generar_pdf).pack(pady=10)

    raiz.mainloop()

# Ejecutar la interfaz
crear_interfaz()
