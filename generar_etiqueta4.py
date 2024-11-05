from reportlab.pdfgen import canvas
import sqlite3
from reportlab.lib.units import mm

def generar_etiquetas(base_datos, vista, salida, ancho_etiqueta=100, alto_etiqueta=150, margen=10, fuente="Helvetica", tamano_fuente=10):
    """
    Genera etiquetas PDF a partir de una vista de una base de datos SQLite.

    Args:
        base_datos (str): Ruta a la base de datos SQLite.
        vista (str): Nombre de la vista en la base de datos.
        salida (str): Nombre del archivo PDF de salida.
        ancho_etiqueta (int, optional): Ancho de la etiqueta en mm. Defaults to 100.
        alto_etiqueta (int, optional): Alto de la etiqueta en mm. Defaults to 150.
        margen (int, optional): Margen en mm. Defaults to 10.
        fuente (str, optional): Nombre de la fuente. Defaults to "Helvetica".
        tamano_fuente (int, optional): Tamaño de la fuente. Defaults to 10.
    """

    try:
        # Conexión a la base de datos
        conn = sqlite3.connect(base_datos)
        cursor = conn.cursor()

        # Obtener datos de la vista
        cursor.execute(f"SELECT * FROM {vista}")
        datos = cursor.fetchall()

        # Crear el documento PDF
        pdf = canvas.Canvas(salida)
        pdf.setFont(fuente, tamano_fuente)

        # Dimensiones de la página
        ancho_pagina, alto_pagina = pdf._pagesize

        # Crear las etiquetas
        x, y = margen, margen
        for fila in datos:
            # Crear una etiqueta por fila
            y_pos = y
            for campo in fila:
                pdf.drawString(x + 10, y_pos, str(campo))
                y_pos -= tamano_fuente + 2

            # Nueva línea si se llega al final de la página
            if y_pos < margen:
                x += ancho_etiqueta
                y = alto_pagina - margen
                if x > ancho_pagina - margen:
                    x = margen
                    pdf.showPage()
                    y = alto_pagina - margen

        pdf.save()
        conn.close()
        print(f"Etiquetas generadas en {salida}")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Ejemplo de uso:
generar_etiquetas("pescaderia.db", "ETIQUETA_PDF", "etiquetas4.pdf")