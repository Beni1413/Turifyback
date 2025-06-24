TURIFY - BACKEND FASTAPI
Este backend maneja el sistema de reservas de la app Turify. Permite registrar usuarios, gestionar servicios, pedidos, y enviar correos con el resumen de lo comprado. Usa FastAPI y PostgreSQL.

Tecnologías:
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- smtplib + Gmail con contraseña de aplicación
- CORS Middleware

Archivos principales:
- main.py: define los endpoints
- crud.py: lógica de negocio y consultas a la base
- models.py: tablas con SQLAlchemy
- schemas.py: validaciones con Pydantic
- database.py: conexión a PostgreSQL
- emails.py: genera y envía el correo
- dependencies.py: verificación de roles

Funcionalidades:
- Registro y login de usuarios
- Guardado de contraseñas hasheadas
- Agregado y eliminación de productos del carrito
- Creación del pedido (cabecera)
- Creación de detalles del pedido (con los servicios contratados)
- Envío automático de correo con el resumen (nombre, servicios, totales)
- Gestión CRUD de servicios (alta, editar, borrar)
- Filtro de servicios por categoría
- Listado de pedidos (todos o por usuario logueado)
- Cambio de estado de un pedido (ej. a "anulado")
- Eliminación de pedidos
- Listado de clientes con rol "cliente"
- Roles simples (cliente o admin)
- Conexión segura con frontend en Firebase (CORS configurado)

Cómo ejecutarlo:
1. Crear entorno virtual
2. Instalar dependencias
3. Asegurar conexión a la base
4. Ejecutar: uvicorn main:app --reload

Notas:
- El correo se dispara solo desde crear_detalle_de_pedido()
- El frontend debe esperar la respuesta del pedido para usar su id al cargar los detalles
- Las URLs permitidas desde frontend están en CORS (web.app y firebaseapp.com)

