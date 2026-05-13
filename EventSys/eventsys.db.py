import sqlite3

# Crear base de datos
conn = sqlite3.connect("eventsys.db")

cursor = conn.cursor()

# Crear tabla productos
cursor.execute("DROP TABLE IF EXISTS productos")
cursor.execute("""
CREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    categoria TEXT,
    cantidad INTEGER,
    precio REAL,
    descripcion TEXT,
    imagen TEXT
)
""")

# Inventario unificado con al menos 30 elementos
productos = [
    ("Mesa redonda", "Mesas", 36, 160.0, "Mesa redonda de 1.8m para banquetes", "imagenes de proyecto/mesas_circulares.jpeg"),
    ("Mesa cuadrada (tablón)", "Mesas", 8, 140.0, "Mesa cuadrada madera 1.2m", "imagenes de proyecto/mesas..jpeg"),
    ("Silla de metal color negro", "Sillas", 400, 25.0, "Silla metálica negra con acolchado", "imagenes de proyecto/Silla.jpeg"),
    ("Silla Tiffany blanca", "Sillas", 120, 45.0, "Silla Tiffany elegante", "imagenes de proyecto/Silla.jpeg"),
    ("Silla plegable", "Sillas", 200, 30.0, "Silla plegable plástico", "imagenes de proyecto/Silla.jpeg"),
    ("Silla dorada", "Sillas", 80, 50.0, "Silla banquetera dorada", "imagenes de proyecto/Silla.jpeg"),
    ("Mantel tipo 1 (blanco 2x1.5)", "Mantelería", 38, 12.0, "Mantel blanco rectangular", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 2 (negro 2x1.5)", "Mantelería", 30, 12.0, "Mantel negro rectangular", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 3 (rojo 2x1.5)", "Mantelería", 20, 12.0, "Mantel rojo rectangular", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 4 (azul 2x1.5)", "Mantelería", 10, 12.0, "Mantel azul rectangular", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 5 (verde 2x1.5)", "Mantelería", 10, 12.0, "Mantel verde rectangular", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 6 (tostado 2x1.5)", "Mantelería", 8, 12.0, "Mantel tostado rectangular", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 7 (morado 2x1.5)", "Mantelería", 20, 12.0, "Mantel morado rectangular", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 8 (dorado 2x1.5)", "Mantelería", 20, 15.0, "Mantel dorado elegante", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 9 (plateado 2x1.5)", "Mantelería", 15, 15.0, "Mantel plateado elegante", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 10 (rosa 2x1.5)", "Mantelería", 15, 12.0, "Mantel rosa pastel", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 11 (beige 2x1.5)", "Mantelería", 15, 10.0, "Mantel beige clásico", "imagenes de proyecto/mesas..jpeg"),
    ("Mantel tipo 12 (turquesa 2x1.5)", "Mantelería", 20, 12.0, "Mantel turquesa moderno", "imagenes de proyecto/mesas..jpeg"),
    ("Inflable Toy Story", "Inflables", 1, 2500.0, "Inflable temático Toy Story", "imagenes de proyecto/inflable.jpeg"),
    ("Inflable Chavo del 8", "Inflables", 1, 2500.0, "Inflable temático Chavo del 8", "imagenes de proyecto/inflable_2.jpeg"),
    ("Carpa 6x6", "Carpas", 1, 800.0, "Carpa 6x6 blanca", "imagenes de proyecto/carpa.jpeg"),
    ("Carpa 10x10", "Carpas", 1, 1200.0, "Carpa 10x10 azul", "imagenes de proyecto/carpa_grande.jpeg"),
    ("Arco de globos", "Decoración", 3, 400.0, "Arco de globos decorativos", "imagenes de proyecto/inflable.jpeg"),
    ("Centro de mesa floral", "Decoración", 40, 80.0, "Centro de mesa con flores artificiales", "imagenes de proyecto/mesas..jpeg"),
    ("Banderín de tela", "Decoración", 50, 35.0, "Banderín decorativo 3m", "imagenes de proyecto/mesas..jpeg"),
    ("Cubo de hielo", "Accesorios", 20, 50.0, "Cubo de hielo de plástico", "imagenes de proyecto/mesas..jpeg"),
    ("Cajón para pastel", "Accesorios", 30, 20.0, "Caja para pastel con ventana", "imagenes de proyecto/mesas..jpeg"),
    ("Mesa auxiliar alta", "Mesas", 15, 110.0, "Mesa alta para bar", "imagenes de proyecto/mesas_circulares.jpeg"),
    ("Silla con funda blanca", "Sillas", 160, 35.0, "Silla con funda de tela blanca", "imagenes de proyecto/Silla.jpeg"),
    ("Cubre sillas negras", "Sillas", 120, 10.0, "Cubre para silla talla estándar", "imagenes de proyecto/Silla.jpeg")
]

cursor.executemany(
"INSERT INTO productos (nombre,categoria,cantidad,precio,descripcion,imagen) VALUES (?,?,?,?,?,?)",
productos
)

# Crear tabla disponibilidad
cursor.execute("DROP TABLE IF EXISTS disponibilidad")
cursor.execute("""
CREATE TABLE disponibilidad (
    fecha TEXT PRIMARY KEY,
    estado TEXT,
    descripcion TEXT
)
""")

# Insertar disponibilidad para marzo 2026
disponibilidades = []
for i in range(1, 32):
    fecha = f"2026-03-{i:02d}"
    if i in [7, 14, 21]:
        estado = "reservado"
        desc = "Reservado"
    elif i == 28:
        estado = "parcial"
        desc = "Disponibilidad limitada"
    else:
        estado = "disponible"
        desc = "Disponible"
    disponibilidades.append((fecha, estado, desc))

cursor.executemany(
"INSERT INTO disponibilidad (fecha, estado, descripcion) VALUES (?, ?, ?)",
disponibilidades
)

conn.commit()
conn.close()

print("Base de datos creada correctamente")