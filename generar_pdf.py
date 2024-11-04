import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

def generar_etiquetas_pdf(data):
    # Abre un diálogo para seleccionar la ubicación de guardado del archivo
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter
    nombre_archivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Guardar Etiquetas"
    )

    # Si el usuario cancela, nombre_archivo será una cadena vacía
    if not nombre_archivo:
        print("Guardado cancelado")
        return
    
    ancho_pagina, alto_pagina = A4
    ancho_etiqueta = ancho_pagina / 2  # Dos columnas de etiquetas
    alto_etiqueta = 5 * cm  # Alto de cada etiqueta

    c = canvas.Canvas(nombre_archivo, pagesize=A4)
    c.setFont("Helvetica", 10)
    y = alto_pagina - alto_etiqueta

    for i, registro in enumerate(data):
        columna = i % 2
        if i > 0 and columna == 0:
            y -= alto_etiqueta  # Salta a la siguiente fila si estamos en la segunda columna
        
        x = columna * ancho_etiqueta
        
        # Etiqueta 1 (a la izquierda o derecha según la columna)
        generar_contenido_etiqueta(c, x, y, registro)
        
        # Si hemos terminado la página, añadimos una nueva
        if y < alto_etiqueta:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = alto_pagina - alto_etiqueta

    c.save()
    print(f"Archivo guardado en: {nombre_archivo}")

def generar_contenido_etiqueta(c, x, y, registro):
    # Ajusta las posiciones de texto dentro de la etiqueta según el diseño
    c.drawString(x + 1 * cm, y, f"ZONA CAPTURA: {registro['zona']}")
    c.drawString(x + 1 * cm, y - 0.5 * cm, f"EXPEDIDOR: {registro['expedidor']}")
    c.drawString(x + 1 * cm, y - 1 * cm, f"DENOMINACIÓN COMERCIAL: {registro['especie']}")
    c.drawString(x + 1 * cm, y - 1.5 * cm, f"MÉTODO PRODUCCIÓN: {registro['metodo']}")
    c.drawString(x + 1 * cm, y - 2 * cm, f"PVP: {registro['pvp']}")
    c.drawString(x + 1 * cm, y - 2.5 * cm, f"MOD. PRESENTACIÓN: {registro['presentacion']}")
    c.drawString(x + 1 * cm, y - 3 * cm, f"ARTE: {registro['arte']}")
    c.drawString(x + 1 * cm, y - 3.5 * cm, f"BARCO: {registro['barco']}")
    c.drawString(x + 1 * cm, y - 4 * cm, f"DESCONGELADO: {registro['descongelado']}")
    c.drawString(x + 1 * cm, y - 4.5 * cm, f"LOTE EXTERNO: {registro['lote_ext']}")
    c.drawString(x + 1 * cm, y - 5 * cm, f"NOTA INTERNA: {registro['nota_int']}")
    c.drawString(x + 1 * cm, y - 5.5 * cm, f"LOTE INTERNO: {registro['lote_int']}")

# Datos de ejemplo
data = [
    {
        "especie": "Merluza",
        "pvp": "20 EUR",
        "zona": "Zona FAO 27",
        "expedidor": "Expedidor Ejemplo",
        "produccion": "Fresco",
        "arte": "Arrastre",
        "metodo": "Aguas Profundas",
        "presentacion": "Filete",
        "barco": "Barco Ejemplo",
        "descongelado": "No",
        "lote_ext": "L12345",
        "lote_int": "INT12345",
        "nota_ext": "Nota Ext",
        "nota_int": "Nota Int",
    },
    # Agrega más registros si es necesario
]

# Llama a la función para generar el PDF
generar_etiquetas_pdf(data)
