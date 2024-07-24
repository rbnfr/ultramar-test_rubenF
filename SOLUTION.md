# Prueba técnica Ultramar - Aplicación de Logística

## Visión General

Esta aplicación Django gestiona el transporte de vehículos usados para una empresa de logística. Proporciona una interfaz CRUD para reservas y permite asociar/desasociar vehículos con entregas concretas. La aplicación también incluye una API REST construida con Django Rest Framework y un comando de gestión para eliminar vehículos antiguos (de más de 6 meses desde su llegada).

## Características Principales

1. Operaciones CRUD para operaciones de entrada y vehículos
2. API REST para entradas y vehículos
3. Capacidad de asociar/desasociar vehículos con una determinada entrada
4. Comando de gestión para eliminar vehículos con fechas de llegada de más de 6 meses de antigüedad
5. Landing page sencilla con descripción de la aplicación y principales funciones en la barra superior.

## Decisiones técnicas

### 1. Diseño del Modelo

- **Modelo de operación de transporte**: Incluye campos para número de la entrada, puerto de carga, puerto de descarga, fecha de llegada y fecha de salida.
- **Modelo de vehículo**: Incluye campos para VIN, marca, modelo, peso y su asociación con uno de los transportes.
- La relación entre transporte y vehículo es de uno a muchos, permitiendo múltiples vehículos por operación de transporte.

### 2. Diseño de API

- Se utilizaron ViewSets de Django Rest Framework para operaciones CRUD fáciles.
- Se implementaron acciones personalizadas para asociar y desasociar vehículos con reservas.
- Se utilizaron serializadores anidados para incluir información de vehículos en las respuestas de reservas.

### 3. Integridad de datos

- Se utilizaron restricciones únicas en el número de reserva y VIN para garantizar la integridad de los datos.
- Se implementó un comportamiento SET_NULL on_delete para la relación Vehículo-Reserva para evitar la pérdida de datos cuando se elimina una reserva.

### 4. Organización del código
- Organización del código en estructura estándar de Django.
- Se utilizó la función de comandos de gestión de Django para la tarea de eliminación de vehículos.


## Mejoras

1. **Autenticación y Autorización**: Implementar autenticación de usuario y control de acceso basado en roles.

2. **Paginación**: Agregar paginación a los endpoints de la API para manejar grandes conjuntos de datos de manera eficiente.

3. **Filtrado y Búsqueda**: Implementar capacidades de filtrado y búsqueda en la API.

4. **Validación**: Agregar validación más robusta para las entradas de datos (por ejemplo, rangos de fechas, formato VIN, etc).

5. **Tests**: Escribir el resto de pruebas unitarias y de integración para modelos, vistas y endpoints de API.

6. **Documentación de API**: Usar herramientas como Swagger o DRF-YASG para la documentación automática de la API.

7. **Tareas en Segundo Plano**: Usar Celery para manejar la eliminación de vehículos antiguos como una tarea en segundo plano en caso de grandes volúmenes de datos.

8. **Containerización**: Dockerizar la aplicación para facilitar el despliegue y la escalabilidad.

9.  **Caché**: Implementar mecanismos de caché para mejorar el rendimiento de los datos accedidos con frecuencia.

10. **Monitoreo**: Configurar monitoreo y alertas para el rendimiento de la aplicación y la base de datos.

11. **Actualizar vistas**: Mejorar la apariencia y la usabilidad de las páginas de vistas de la aplicación. Hacer coincidir el estilo con la página de inicio.

12. **Solución de bugs**: Corregir redireccionamiento erróneo en página de detalle de vehículo. Corregir posibles errores de lógica de negocio.
