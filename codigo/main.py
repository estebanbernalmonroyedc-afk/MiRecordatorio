import mysql.connector

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  
        database="mirecordatorio"
    )

# ===== LEER =====
def cargar_recordatorios():
    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("SELECT * FROM recordatorios")
    datos = cursor.fetchall()

    conexion.close()
    return datos

# ===== CREAR =====
def crear_recordatorio(titulo, descripcion, fecha, hora):
    conexion = conectar()
    cursor = conexion.cursor()

    sql = """
    INSERT INTO recordatorios (titulo, descripcion, fecha, hora)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(sql, (titulo, descripcion, fecha, hora))
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