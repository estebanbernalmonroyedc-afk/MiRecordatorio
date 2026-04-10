MiRecordatorio
Descripción
MiRecordatorio es una aplicación de escritorio que permite a los usuarios crear, visualizar, editar y eliminar recordatorios con fecha y hora. Su objetivo es ayudar a organizar tareas diarias de forma sencilla e intuitiva.

Funcionalidades
Crear recordatorios

Editar recordatorios

Eliminar recordatorios

Visualizar recordatorios

Gestión de tareas con fecha y hora

Tecnologías utilizadas
Python 3.11

Kivy 2.3.1

MySQL (MariaDB / XAMPP)

mysql-connector-python

Visual Studio Code

GitHub

Requisitos del sistema
Tener instalado Python 3.11

Tener instalado MySQL o XAMPP con el servicio activo

Tener instalada la librería:

pip install kivy mysql-connector-python
Configuración de la base de datos
Servidor: localhost

Puerto: 3306

Base de datos: mirecordatorio

Tabla: recordatorios

Es importante que el servidor MySQL esté encendido, de lo contrario la aplicación no funcionará.

Ejecución del proyecto
Para iniciar la aplicación, ejecutar el siguiente comando en la terminal:

py -3.11 interfaz/app_kivy.py
Estructura del proyecto
interfaz/ → Contiene la interfaz gráfica (Kivy)

codigo/ → Contiene la lógica y conexión a la base de datos

capturas_ui/ → Imágenes del funcionamiento de la aplicación

Capturas de la aplicación
Las capturas del funcionamiento de la aplicación se encuentran en la carpeta:

capturas_ui/
Notas importantes
La aplicación funciona únicamente si la base de datos está activa

Se recomienda usar Python 3.11 para evitar errores con Kivy

Los datos se almacenan en MySQL, no en archivos JSON

Autor
Esteban Bernal Monroy

Estado del proyecto
Versión inicial funcional

Organización
Politécnico Internacional

