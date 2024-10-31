import sqlite3

DATABASE_NAME = "pescaderia.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tablas():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Crear tabla_artes
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_artes (
        id_arte INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_arte TEXT NOT NULL,
        descr_arte TEXT
    )
    ''')
    
    # Crear tabla_familias
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_familias (
        id_familia INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_familia TEXT NOT NULL,
        descr_familia TEXT
    )
    ''')
    
    # Crear tabla_especies
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_especies (
        id_especie INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_especie TEXT NOT NULL,
        cientifico_especie TEXT,
        familia_id INTEGER,
        descr_especie TEXT,
        FOREIGN KEY (familia_id) REFERENCES tabla_familias(id_familia)
    )
    ''')
    
    # Crear tabla_expedidores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_expedidores (
        id_expedidor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_expedidor TEXT NOT NULL,
        descr_expedidor TEXT
    )
    ''')
    
    # Crear tabla_metodos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_metodos (
        id_metodo INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_metodo TEXT NOT NULL,
        descr_metodo TEXT
    )
    ''')
    
    # Crear tabla_producciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_producciones (
        id_produccion INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_produccion TEXT NOT NULL,
        descr_produccion TEXT
    )
    ''')
    
    # Crear tabla_proveedores
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_proveedores (
        id_proveedor INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_proveedor TEXT NOT NULL,
        nif_proveedor TEXT,
        nrs_proveedor TEXT
    )
    ''')
    
    # Crear tabla_zonas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_zonas (
        id_zona INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_zona TEXT NOT NULL,
        descr_zona TEXT
    )
    ''')
    
    # Crear tabla_presentaciones
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_presentaciones (
        id_presentacion INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_presentacion TEXT NOT NULL,
        descr_presentacion TEXT
    )
    ''')
    
    # Crear tabla_barcos
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_barcos (
        id_barco INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_barco TEXT NOT NULL,
        descr_barco TEXT
    )
    ''')
    
    # Crear tabla_listados
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_listados (
        id_listado INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha_listado DATE NOT NULL
    )
    ''')
    
    # Crear tabla_usuarios
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_usuarios (
        id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre_usuario TEXT NOT NULL UNIQUE,
        clave_usuario TEXT NOT NULL
    )
    ''')
    
    # Crear tabla_detalle_listado
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tabla_detalle_listado (
        id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
        listado_id INTEGER,
        fecha DATE,
        proveedor_id INTEGER,
        factura TEXT,
        especie_id INTEGER,
        compra DECIMAL(10, 2),
        cantidad DECIMAL(10, 2),
        iva DECIMAL(5, 2),
        costo DECIMAL(10, 2),
        porcentaje DECIMAL(5, 2),
        beneficio DECIMAL(10, 2),
        pvp DECIMAL(10, 2),
        zona_id INTEGER,
        expedidor_id INTEGER,
        produccion_id INTEGER,
        arte_id INTEGER,
        metodo_id INTEGER,
        presentacion_id INTEGER,
        barco_id INTEGER,
        descongelado BOOLEAN,
        lote_ext TEXT,
        lote_int TEXT,
        nota_ext TEXT,
        nota_int TEXT,
        reg_congelado BOOLEAN,
        FOREIGN KEY (listado_id) REFERENCES tabla_listados(id_listado),
        FOREIGN KEY (proveedor_id) REFERENCES tabla_proveedores(id_proveedor),
        FOREIGN KEY (especie_id) REFERENCES tabla_especies(id_especie),
        FOREIGN KEY (zona_id) REFERENCES tabla_zonas(id_zona),
        FOREIGN KEY (expedidor_id) REFERENCES tabla_expedidores(id_expedidor),
        FOREIGN KEY (produccion_id) REFERENCES tabla_producciones(id_produccion),
        FOREIGN KEY (arte_id) REFERENCES tabla_artes(id_arte),
        FOREIGN KEY (metodo_id) REFERENCES tabla_metodos(id_metodo),
        FOREIGN KEY (presentacion_id) REFERENCES tabla_presentaciones(id_presentacion),
        FOREIGN KEY (barco_id) REFERENCES tabla_barcos(id_barco)
    )
    ''')
    
    conn.commit()
    conn.close()

# Insertar un usuario por defecto
def insertar_usuario_default():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO tabla_usuarios (nombre_usuario, clave_usuario) VALUES (?, ?)", ("admin", "admin123"))
    
    conn.commit()
    conn.close()

# Llamar a esta función después de crear las tablas
crear_tablas()
insertar_usuario_default()