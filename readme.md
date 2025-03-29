# Proyecto KAT - Trivia sobre Lionel Messi

## Descripción del Proyecto

Este proyecto es una aplicación web de trivia sobre Lionel Messi, desarrollada utilizando Flask (un framework de Python) y SQLite como base de datos. Los usuarios pueden registrarse, iniciar sesión y responder preguntas sobre la carrera y logros de Messi. La aplicación incluye funcionalidades como:

- Sistema de autenticación de usuarios
- Panel de administración para gestionar preguntas
- Clasificación de usuarios según sus respuestas correctas
- Base de datos pre-cargada con preguntas sobre Messi

## Requisitos del Sistema

- Python 3.7 o superior
- Flask
- Werkzeug
- SQLite3

## Estructura del Proyecto

- `app.py`: Archivo principal de la aplicación Flask
- `messi_store.db`: Base de datos SQLite
- `templates/`: Contiene las plantillas HTML
- `static/`: Contiene archivos estáticos (CSS, JS, imágenes)

## Funcionalidades Principales

### Autenticación de Usuarios
- Registro de nuevos usuarios
- Inicio de sesión con validación de credenciales
- Cierre de sesión
- Usuario administrador predeterminado:
  - Email: `admin@example.com`
  - Contraseña: `admin123`

### Trivia
- 20 preguntas pre-cargadas sobre Lionel Messi
- Sistema de progreso por preguntas
- Registro de respuestas y cálculo de aciertos

### Panel de Administración
- Agregar nuevas preguntas
- Editar preguntas existentes
- Eliminar preguntas
- Acceso restringido a usuarios administradores

### Clasificación
- Muestra el ranking de usuarios según respuestas correctas
- Incluye el total de respuestas y aciertos por usuario

## Base de Datos

La aplicación utiliza SQLite y contiene las siguientes tablas:

### Usuario
- Almacena la información de los usuarios registrados
- Campos: id, email, password, es_admin

### Pregunta
- Contiene las preguntas y sus opciones de respuesta
- Campos: id, texto, opcion1, opcion2, opcion3, opcion4, respuesta_correcta

### Resultado
- Registra las respuestas de los usuarios
- Campos: id, usuario_id, pregunta_id, respuesta_usuario, es_correcta, fecha