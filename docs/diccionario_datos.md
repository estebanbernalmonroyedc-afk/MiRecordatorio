# 📘 Diccionario de Datos - MiRecordatorio

## 🗄️ Tabla: recordatorios

| Campo           | Tipo de dato     | Descripción                                      | Restricciones                  | Ejemplo                |
|----------------|------------------|--------------------------------------------------|--------------------------------|------------------------|
| id             | INT              | Identificador único del recordatorio             | PRIMARY KEY, AUTO_INCREMENT    | 1                      |
| titulo         | VARCHAR(100)     | Nombre o título del recordatorio                 | NOT NULL                       | "Tarea programación"   |
| descripcion    | TEXT             | Descripción detallada del recordatorio           | NULL permitido                 | "Terminar app en Kivy" |
| fecha          | DATE             | Fecha programada del recordatorio                | NOT NULL                       | 2026-03-25             |
| hora           | TIME             | Hora programada del recordatorio                 | NOT NULL                       | 18:00:00               |
| estado         | ENUM             | Estado del recordatorio (pendiente/completado)   | DEFAULT 'pendiente'            | "pendiente"            |
| fecha_creacion | TIMESTAMP        | Fecha en que se creó el recordatorio             | DEFAULT CURRENT_TIMESTAMP      | 2026-03-20 14:30:00    |

---

## 📌 Descripción general

La tabla **recordatorios** almacena la información de los recordatorios creados por el usuario en la aplicación *MiRecordatorio*.  

Cada registro representa un recordatorio con su título, descripción, fecha y hora programada, así como su estado (pendiente o completado) y la fecha en que fue creado.

---

## 🔄 Observación

Actualmente, la aplicación utiliza un archivo JSON (`recordatorios.json`) para almacenar los datos.  
Sin embargo, este diccionario de datos corresponde al diseño propuesto para una futura implementación con base de datos relacional (MySQL).
