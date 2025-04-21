import sqlite3
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.pdfgen import canvas
from tkinter import filedialog, messagebox

def generar_pdf_consulta():
    """
    Genera un PDF con los registros de la vista 'consulta_detalle_listado' de la base de datos.
    """
    # Abrir diálogo para seleccionar ubicación y nombre de archivo
    pdf_path = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Guardar archivo PDF"
    )
    
    if not pdf_path:
        return  # Si el usuario cancela, no hacer nada

    try:
        # Conectar a la base de datos
        conn = sqlite3.connect('pescaderia.db')
        cursor = conn.cursor()

        # Obtener los registros de la vista 'consulta_detalle_listado'
        cursor.execute("SELECT fecha, especie, pvp, nota_int FROM consulta_detalle_listado ORDER BY especie")
        registros = cursor.fetchall()

        # Crear el archivo PDF
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setTitle("Consulta Detalle Listado")
        width, height = A4

        # Ajustar el margen superior a 1 cm (28.35 puntos)
        margen_superior = 28.35
        margen_izquierdo = 28.35

        # Título del PDF
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margen_izquierdo, height - margen_superior, "")

        # Crear la tabla con los datos
        data = [["Fecha", "Especie", "PVP (€)", "Nota Interna"]]  # Encabezados
        for row in registros:
            fecha = row[0] or ""
            especie = row[1] or ""
            
            # Validar si el valor de PVP es numérico antes de formatearlo
            try:
                pvp = f"{float(row[2]):,.2f} €" if row[2] is not None else ""
            except ValueError:
                pvp = ""  # Si no es numérico, dejar el campo vacío

            nota_int = row[3] or ""
            data.append([fecha, especie, pvp, nota_int])

        # Estilo de la tabla
        table = Table(data, colWidths=[80, 120, 70, 150])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),  # Reducir el relleno inferior
            ('TOPPADDING', (0, 0), (-1, -1), 0),     # Reducir el relleno superior
            ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
            # Alineación específica para columnas
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),  # Columna 'Especie' a la izquierda
            ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # Columna 'PVP' a la derecha
            ('ALIGN', (3, 1), (3, -1), 'LEFT'),  # Columna 'Nota Interna' a la izquierda
        ]))

        # Dibujar la tabla en el PDF
        table.wrapOn(c, width, height)
        table.drawOn(c, margen_izquierdo, height - margen_superior - 120)  # Ajustar posición de la tabla

        # Guardar el PDF
        c.save()

        messagebox.showinfo("Éxito", f"PDF generado correctamente en:\n{pdf_path}")

    except sqlite3.Error as e:
        messagebox.showerror("Error de Base de Datos", f"No se pudo generar el PDF: {str(e)}")
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar el PDF: {str(e)}")
    finally:
        if conn:
            conn.close()