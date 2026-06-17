# 🥩 Parrilla Argentina — Panel de Administración

Trabajo práctico final para la materia **Introducción al Desarrollo del Software (IDS)** — Cátedra Lanzillotta, FIUBA.

**Grupo:** VEDAAVIFI
**Integrantes:** Valentina Huerta, Ailen Pestaña, Franco Requejo, Delfina Rodriguez, Valentina Ruffa, Abril Yebara, Ignacio Zamparolo

---

## Descripción

Sistema web full-stack para la gestión administrativa de un restaurante de parrilla argentina. Permite a los administradores gestionar el menú, combos, reservas, reseñas y servicios extra; y a los clientes realizar reservas y dejar reseñas.

---

## Stack tecnológico

| Capa | Tecnología |
|------|-----------|
| Frontend | Flask + Jinja2 (puerto 8080) |
| Backend API | Flask + Blueprints (puerto 5000) |
| Base de datos | MariaDB 11 / MySQL |
| Almacenamiento de imágenes | Supabase Storage |
| Autenticación | JWT (`PyJWT`) |
| Emails y QR | Flask + smtplib + qrcode |
| Scheduler | APScheduler (transiciones automáticas de reservas) |
| Contenedores | Docker + Docker Compose |

---

## Estructura del proyecto

```
VEDAAVIFI-TP-FINAL/
├── backend/
│   ├── app/
│   │   ├── app.py              # Entry point Flask API
│   │   ├── db_connection.py
│   │   ├── utils.py            # JWT, QR, emails, scheduler, filtros
│   │   ├── constants.py
│   │   ├── routes/             # Blueprints por recurso
│   │   │   ├── auth.py
│   │   │   ├── productos.py
│   │   │   ├── combos.py
│   │   │   ├── combo_version.py
│   │   │   ├── combo_detalle.py
│   │   │   ├── reservas.py
│   │   │   ├── resenias.py
│   │   │   ├── servicios_extra.py
│   │   │   ├── reportes.py
│   │   │   └── usuarios.py
│   │   ├── services/           # Lógica de negocio
│   │   └── validators/         # Validaciones de entrada
│   ├── dockerfile
│   └── requirements.txt
├── frontend/
│   ├── app/
│   │   ├── parrilla_argentina_admin/
│   │   │   ├── routes/         # Rutas del frontend
│   │   │   └── services/       # Llamadas a la API
│   │   ├── static/             # CSS y JS
│   │   └── templates/          # Jinja2 HTML
│   ├── run.py
│   └── requirements.txt
├── database/
│   └── mysql_db.sql            # Schema + datos iniciales
├── docker-compose.yml
└── init.sh                     # Script de setup local
```

---

## Funcionalidades

### Panel de administración (requiere login JWT)
- **Menú / Productos:** CRUD completo con imagen (subida a Supabase Storage), filtros dietarios (lactosa, vegetariano, vegano, sin TACC)
- **Combos:** gestión de combos con versiones (descripción, personas, precio) y detalle de productos incluidos
- **Reservas:** visualización y gestión de reservas; estados: `pendiente → confirmada → finalizada / vencida / cancelada`
- **Reseñas:** moderación con filtro de malas palabras
- **Servicios extra:** CRUD
- **Reportes:** estadísticas de uso

### Vista de clientes (pública)
- Consulta del menú con imágenes y filtros
- Formulario de reserva con validaciones
- Envío de reseña asociada a una reserva finalizada
- Confirmación de reserva por email con QR embebido

### Automatización
- APScheduler ejecuta transiciones automáticas de estado de reservas en background

---

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

API_BASE_URL=http://127.0.0.1:5000
REQUEST_TIMEOUT=10
MALAS_PALABRAS=idiota,pelotudo,estupido,boludo,imbecil,inutil,mierda,basura,garca,forro,hijodeputa,puto
SUPABASE_URL=https://cnsegpmrifgsccfynrhl.supabase.co/
SUPABASE_KEY=sb_secret_SGl_gD1QA6wOSkVNbkMZtw_puc_Eeyr
SUPABASE_BUCKET=productos
DB_USER=admin
DB_PASSWORD=1234
DATABASE=parrilla_argentina
DB_PORT=3307
FRONTEND_URL=http://127.0.0.1:8080
SMTP_USER=parrillaargentina.web@gmail.com
SMTP_PASSWORD=uhmwoyafvcrevuvk
```

---

## Instalación y ejecución

### Opción 1: Docker Compose (recomendada)

```bash
# Clonar el repositorio
git clone https://github.com/IgnacioZamparolo/VEDAAVIFI-TP-FINAL.git
cd VEDAAVIFI-TP-FINAL

# Levantar los servicios (MariaDB + Backend)
docker compose up -d --build
```

> El frontend se levanta por separado (ver Opción 2).

### Opción 2: Entorno local (sin Docker)

```bash
# Setup automático de entornos virtuales
bash init.sh

# Terminal 1 — Backend (puerto 5000)
cd backend
source .venv/bin/activate
python app/app.py

# Terminal 2 — Frontend (puerto 8080)
cd frontend
source .venv/bin/activate
python run.py
```

Accedé a `http://localhost:8080` en el navegador.

---

## Base de datos

El archivo `database/mysql_db.sql` crea automáticamente el schema al levantar el contenedor de MariaDB.

### Tablas principales

| Tabla | Descripción |
|-------|-------------|
| `productos` | Items del menú con atributos dietarios e imagen |
| `combos` | Combos disponibles |
| `combo_version` | Versiones de un combo (personas, precio) |
| `combo_detalle` | Relación combo ↔ productos |
| `reservas` | Reservas con estado y mesa asignada |
| `resenias` | Reseña vinculada a una reserva finalizada |
| `servicios_extra` | Servicios adicionales del restaurante |
| `usuarios` | Administradores del sistema |

**Credenciales de admin por defecto:**
- Email: `parrillaargentina@gmail.com`
- Contraseña: `123456`

---

## API — Endpoints principales

| Método | Ruta | Acceso | Descripción |
|--------|------|--------|-------------|
| POST | `/auth/login` | Público | Login admin, retorna JWT |
| GET | `/productos` | Público | Listar menú |
| POST | `/productos` | Admin | Crear producto |
| PUT | `/productos/<id>` | Admin | Editar producto |
| DELETE | `/productos/<id>` | Admin | Eliminar producto |
| GET | `/combos` | Público | Listar combos |
| GET | `/reservas` | Admin | Listar reservas |
| POST | `/reservas` | Público | Crear reserva |
| GET | `/resenias` | Admin | Listar reseñas |
| POST | `/resenias` | Público | Crear reseña |
| GET | `/reportes` | Admin | Ver reportes |

---
## Documentacion
**Swagger:**
openapi: 3.0.0 
info: 
  title: API Parrilla Argentina 
  version: 1.0.0 
  description: Contrato de diseño para el sistema de gestión de la 
parrilla (Reservas, Combos, Productos y Reportes). 
servers: 
  - url: http://localhost:5000 
    description: Servidor Local de Flask 
 
paths: 
  # --- Módulo: Auth --- 
  /auth/login: 
    post: 
      tags: 
        - Autenticación 
      summary: Iniciar sesión en el sistema 
      requestBody: 
        required: true 
        content: 
          application/json: 
            schema: 
              type: object 
              properties: 
                email: 
                  type: string 
                password: 
                  type: string 
      responses: 
        '200': 
          description: Autenticación exitosa (Devuelve token o sesión) 
        '401': 
          description: Credenciales incorrectas 
 
  # --- Módulo: Usuarios --- 
  /usuarios: 
    get: 
      tags: 
        - Usuarios 
      summary: Obtener lista de usuarios (Solo Admin) 
      responses: 
        '200': 
          description: Lista de usuarios obtenida correctamente 
    post: 
      tags: 
        - Usuarios 
      summary: Registrar un nuevo usuario 
      requestBody: 
        required: true 
        content: 
          application/json: 
            schema: 
              type: object 
              properties: 
                nombre: 
                  type: string 
                email: 
                  type: string 
                password: 
                  type: string 
      responses: 
        '201': 
          description: Usuario creado con éxito 
 
  # --- Módulo: Productos --- 
  /productos: 
    get: 
      tags: 
        - Productos 
      summary: Obtener todos los productos del menú 
      responses: 
        '200': 
          description: Lista de productos 
    post: 
      tags: 
        - Productos 
      summary: Agregar un nuevo producto al menú 
      responses: 
        '201': 
          description: Producto agregado 
 
  # --- Módulo: Combos, Detalles y Versiones --- 
  /combos: 
    get: 
      tags: 
        - Combos y Promociones 
      summary: Listar todos los combos disponibles 
      responses: 
        '200': 
          description: Lista de combos 
  /combos/detalles: 
    get: 
      tags: 
        - Combos y Promociones 
      summary: Obtener el desglose de ingredientes/productos por combo 
      responses: 
        '200': 
          description: Detalle de los combos devuelto 
  /combos/versiones: 
    get: 
      tags: 
        - Combos y Promociones 
      summary: Historial o versiones activas de los combos 
      responses: 
        '200': 
          description: Lista de versiones de combos 
 
  # --- Módulo: Reservas --- 
  /reservas: 
    get: 
      tags: 
        - Reservas 
      summary: Listar todas las reservas registradas 
      responses: 
        '200': 
          description: Lista de reservas obtenida correctamente 
    post: 
      tags: 
        - Reservas 
      summary: Crear una nueva reserva de mesa 
      requestBody: 
        required: true 
        content: 
          application/json: 
            schema: 
              type: object 
              properties: 
                mail: 
                  type: string 
                cant_personas: 
                  type: integer 
                dia: 
                  type: string 
                horario: 
                  type: string 
      responses: 
        '201': 
          description: Reserva confirmada con éxito 
 
  # --- Módulo: Reseñas --- 
  /resenias: 
    get: 
      tags: 
        - Reseñas y Feedback 
      summary: Obtener las opiniones de los clientes 
      responses: 
        '200': 
          description: Lista de opiniones 
    post: 
      tags: 
        - Reseñas y Feedback 
      summary: Publicar una nueva reseña 
      responses: 
        '201': 
          description: Reseña guardada 
 
  # --- Módulo: Servicios Extra --- 
  /servicios_extra: 
    get: 
      tags: 
        - Servicios Adicionales 
      summary: Listar servicios extras (ej. shows, decoración, 
estacionamiento) 
      responses: 
        '200': 
          description: Lista de servicios extras 
 
  # --- Módulo: Reportes --- 
  /reportes: 
    get: 
      tags: 
        - Reportes y Estadísticas 
summary: Obtener métricas del negocio (reservas del mes, platos 
más vendidos) 
responses: 
'200': 
description: Datos estadísticos generados correctamente 

**Informe:**

https://docs.google.com/document/d/1Q0X54ZwN_QJlRAj-Ywm_9kUKmZ22esz73_J1EF5A87Y/edit?usp=sharing


## Equipo

**VEDAAVIFI** — Proyecto final IDS, Cátedra Lanzillotta, FIUBA