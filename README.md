# TaskMetrics API (Dockerized Backend)

Una API REST robusta para la gestión de tareas pendientes que incluye filtros dinámicos y un endpoint avanzado de métricas de productividad. El proyecto está completamente containerizado con Docker y conectado a una base de datos PostgreSQL real.

Este proyecto demuestra habilidades sólidas en desarrollo Backend, patrones de diseño de APIs, uso de ORMs y DevOps básico.

---

## Tecnologías Utilizadas

* **Backend:** Python 3.11 & FastAPI
* **Base de Datos:** PostgreSQL 16
* **ORM:** SQLAlchemy (con Psycopg2)
* **Containerización:** Docker & Docker Compose
* **Entorno:** Pydantic (Validación de datos y Variables de entorno)

---

## Características Principales

* **CRUD Completo de Tareas:** Creación, lectura, actualización y eliminación de tareas con persistencia en base de datos.
* **Filtros Dinámicos (Query Parameters):** Búsqueda avanzada de tareas filtrando simultáneamente por estado (`completed`) y nivel de prioridad (`priority`).
* **Cerebro de Métricas (`/tasks/metrics`):** Endpoint de analítica que delega el procesamiento matemático a PostgreSQL mediante funciones de agregación (`GROUP BY` y `COUNT`), calculando en tiempo real:
  * Total de tareas y desglose por estado (Pendientes/Completadas).
  * Porcentaje exacto de progreso del usuario.
  * Conteo exacto de tareas acumuladas por tipo de prioridad.
* **Seguridad Avanzada:** Arquitectura blindada mediante Variables de Entorno (`.env`), aislando por completo las credenciales de la base de datos del código fuente.

---

## Cómo Ejecutar el Proyecto

Gracias a la containerización con Docker, no necesitás tener instalado Python ni PostgreSQL en tu máquina local. Solo asegurate de tener Docker Desktop corriendo y seguí estos pasos:

### 1. Clonar el repositorio y entrar a la carpeta
```bash
git clone [https://github.com/EmiDelgadoV/task-metrics-api.git](https://github.com/EmiDelgadoV/task-metrics-api.git)
cd task-metrics-api
```

### 2. Configurar las variables de entorno
Creá un archivo `.env` en la raíz del proyecto y definí tus credenciales de base de datos para que el sistema funcione de forma segura:
```text
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_DB=task_metrics_db
DB_HOST=mi-base-datos
DB_PORT=5432
```

### 3. Levantar la infraestructura
Ejecutá el siguiente comando para que Docker descargue las imágenes, cree la base de datos y encienda la API automáticamente:
```bash
docker compose up -d --build
```

### 4. Acceder a la Documentación Interactiva (Swagger)
Una vez que el proceso termine, abrí tu navegador e ingresá a la siguiente URL para probar todos los endpoints y filtros en vivo:
* **Swagger UI:** [http://localhost:8080/docs](http://localhost:8080/docs)
```