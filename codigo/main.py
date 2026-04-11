import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mirecordatorio",
        use_pure=True
    )

# ===== LEER =====
def cargar_recordatorios():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM recordatorios ORDER BY id DESC")
    resultados = cursor.fetchall()

    for r in resultados:

        if isinstance(r["hora"], str):
            r["hora"] = r["hora"][:5]

        if not isinstance(r["fecha"], str):
            r["fecha"] = str(r["fecha"])

    conexion.close()
    return resultados

# ===== CREAR =====
def crear_recordatorio(titulo, descripcion, fecha, hora):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO recordatorios (titulo, descripcion, fecha, hora)
        VALUES (%s, %s, %s, %s)
    """, (titulo, descripcion, fecha, hora))

    conexion.commit()
    conexion.close()

# ===== ELIMINAR =====
def eliminar_recordatorio(id_recordatorio):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("DELETE FROM recordatorios WHERE id = %s", (id_recordatorio,))
    conexion.commit()
    conexion.close()

# ===== EDITAR =====
def editar_recordatorio(id_recordatorio, titulo, descripcion, fecha, hora):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    UPDATE recordatorios
    SET titulo=%s, descripcion=%s, fecha=%s, hora=%s
    WHERE id=%s
    """

    cursor.execute(sql, (titulo, descripcion, fecha, hora, id_recordatorio))
    conexion.commit()
    conexion.close()