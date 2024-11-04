import sqlite3
import tkinter as tk
from tkinter import filedialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm

# Función para obtener todos los registros de la base de datos
def obtener_datos():
    # Conecta con la base de datos
    conexion = sqlite3.connect("pescaderia.db")  # Cambia por el nombre de tu base de datos
    cursor = conexion.cursor()
    
    # Consulta para obtener todos los registros
    cursor.execute("""
        SELECT 
            e.nombre_especie AS especie,
            dl.pvp,
            z.nombre_zona AS zona,
            ex.nombre_expedidor AS expedidor,
            pr.nombre_produccion AS produccion,
            a.nombre_arte AS arte,
            m.nombre_metodo AS metodo,
            ps.nombre_presentacion AS presentacion,
            b.nombre_barco AS barco,
            dl.descongelado,
            dl.lote_ext,
            dl.lote_int,
            dl.nota_ext,
            dl.nota_int,
            dl.reg_congelado
        FROM 
            tabla_detalle_listado dl
        LEFT JOIN 
            tabla_especies e ON dl.especie_id = e.id_especie
        LEFT JOIN 
            tabla_zonas z ON dl.zona_id = z.id_zona
        LEFT JOIN 
            tabla_expedidores ex ON dl.expedidor_id = ex.id_expedidor
        LEFT JOIN 
            tabla_producciones pr ON dl.produccion_id = pr.id_produccion
        LEFT JOIN 
            tabla_artes a ON dl.arte_id = a.id_arte
        LEFT JOIN 
            tabla_metodos m ON dl.metodo_id = m.id_metodo
        LEFT JOIN 
            tabla_presentaciones ps ON dl.presentacion_id = ps.id_presentacion
        LEFT JOIN 
            tabla_barcos b ON dl.barco_id = b.id_barco;
    """)
    
    # Convierte los resultados en una lista de diccionarios
    registros = [
        {
            "especie": row[0],
            "pvp": row[1],
            "zona": row[2],
            "expedidor": row[3],
            "produccion": row[4],
            "arte": row[5],
            "metodo": row[6],
            "presentacion": row[7],
            "barco": row[8],
            "descongelado": row[9],
            "lote_ext": row[10],
            "lote_int": row[11],
            "nota_ext": row[12],
            "nota_int": row[13],
            "reg_congelado": row[14],
        }
        for row in cursor.fetchall()
    ]
    
    # Cierra la conexión
    conexion.close()
    
    return registros

# Función para generar el PDF de etiquetas
def generar_etiquetas_pdf(data):
    # Abre un diálogo para seleccionar la ubicación de guardado del archivo
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal de tkinter
    nombre_archivo = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Guardar Etiquetas"
    )

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
        generar_contenido_etiqueta(c, x, y, registro)

        # Si llegamos al final de la página, creamos una nueva
        if y < alto_etiqueta:
            c.showPage()
            c.setFont("Helvetica", 10)
            y = alto_pagina - alto_etiqueta

    c.save()
    print(f"Archivo guardado en: {nombre_archivo}")

# Función para añadir el contenido de una etiqueta
def generar_contenido_etiqueta(c, x, y, registro):
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

# Función principal para ejecutar la generación de etiquetas
def ejecutar_generacion_pdf():
    data = obtener_datos()
    generar_etiquetas_pdf(data)

# Botón de interfaz para generar el PDF
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Generador de PDF")

    boton_generar_pdf = tk.Button(root, text="Generar PDF", command=ejecutar_generacion_pdf)
    boton_generar_pdf.pack(pady=20)

    root.mainloop()
