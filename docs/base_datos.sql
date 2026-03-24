-- Crear base de datos
CREATE DATABASE IF NOT EXISTS MiRecordatorio;
USE MiRecordatorio;

-- =========================
-- TABLA PRINCIPAL
-- =========================
CREATE TABLE recordatorios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado ENUM('pendiente', 'completado') DEFAULT 'pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =========================
-- DATOS DE PRUEBA
-- =========================
INSERT INTO recordatorios (titulo, descripcion, fecha, hora, estado)
VALUES 
('Tarea programación', 'Terminar app en Kivy', '2026-03-25', '18:00:00', 'pendiente'),
('Reunión', 'Reunión con el equipo', '2026-03-26', '10:30:00', 'pendiente'),
('Ejercicio', 'Salir a correr', '2026-03-27', '06:00:00', 'completado');

-- =========================
-- CONSULTAS ÚTILES
-- =========================

-- Ver todos los recordatorios
SELECT * FROM recordatorios;

-- Ver solo pendientes
SELECT * FROM recordatorios WHERE estado = 'pendiente';

-- Eliminar un recordatorio por ID
DELETE FROM recordatorios WHERE id = 1;

-- Actualizar estado (marcar como completado)
UPDATE recordatorios 
SET estado = 'completado'
WHERE id = 2;