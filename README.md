# La Tienda de Gerardo — Backend

API REST desarrollada en Python con **FastAPI**, **SQLAlchemy ORM** y base de datos **PostgreSQL** (Neon).

## Video demostrativo

> 🎥 URL del video: [https://youtu.be/7MaAc7e1gsg]

---

## Tecnologías

| Tecnología | Versión | Uso |
|---|---|---|
| FastAPI | 0.115.0 | Framework principal de la API REST |
| Uvicorn | 0.30.6 | Servidor ASGI |
| SQLAlchemy | 2.0.23 | ORM y gestión de base de datos |
| Pydantic | 2.9.2 | Validación de datos y schemas |
| Alembic | 1.13.1 | Migraciones de base de datos |
| psycopg2 | 2.9.11 | Driver PostgreSQL |
| python-dotenv | 1.0.0 | Variables de entorno |

---

## Entidades

| Entidad | Tabla | Auditoría | Descripción |
|---|---|---|---|
| Usuario | `usuarios` | ✅ | Clase base (Cliente y Administrador) |
| Tienda | `tiendas` | ✅ | Entidad raíz del sistema |
| Catalogo | `catalogos` | ✅ | Pertenece a una Tienda, agrupa los productos |
| Categoria | `categorias` | ✅ | Clasificación de productos |
| Producto | `productos` | ✅ | Pertenece a un Catálogo y una Categoría |
| Descuento | `descuentos` | ✅ | Reglas de descuento por volumen de compra |
| Carrito | `carritos` | ✅ | Pertenece a un Cliente |
| DetalleCarrito | `detalle_carrito` | ✅ | Ítems dentro de un carrito |
| Factura | `facturas` | ✅ | Generada tras una compra |
| DetalleFactura | `detalle_factura` | ✅ | Snapshot de ítems comprados |

---

## Relaciones

```
Tienda (1,1) ──── (1,1) Catalogo
Catalogo (1,N) ──── (N,1) Producto
Categoria (1,N) ──── (N,1) Producto
Usuario (1,N) ──── (N,1) Carrito
Carrito (1,N) ──── (N,1) DetalleCarrito
DetalleCarrito (N,1) ──── (1,N) Producto
Usuario (1,N) ──── (N,1) Factura
Factura (1,N) ──── (N,1) DetalleFactura
Factura (N,1) ──── (1,N) Descuento
Categoria ──auditoría──► Usuario (id_usuario_creacion, id_usuario_edita)
Producto ──auditoría──► Usuario (id_usuario_creacion, id_usuario_edita)
```

---

## Endpoints disponibles

| Prefijo | Módulo | Descripción |
|---|---|---|
| `/auth` | `endpoints/auth.py` | Login y registro de usuarios |
| `/usuarios` | `endpoints/usuarios.py` | Gestión de usuarios |
| `/productos` | `endpoints/productos.py` | CRUD de productos |
| `/categorias` | `endpoints/categorias.py` | CRUD de categorías |
| `/descuentos` | `endpoints/descuentos_tienda.py` | Gestión de descuentos |
| `/carrito` | `endpoints/carrito.py` | Carrito de compras |
| `/facturas` | `endpoints/facturas.py` | Consulta y generación de facturas |

La documentación interactiva de la API está disponible en `/docs` (Swagger UI) y `/redoc` (ReDoc) una vez levantado el servidor.

---

## Estructura del proyecto

```
├── main.py                         # Punto de entrada FastAPI + startup
├── schemas.py                      # Schemas Pydantic globales
├── sistema_gestion.py              # Lógica de gestión (legacy)
├── requirements.txt
├── alembic.ini
├── .env
├── .env.example
├── src/
│   ├── auth/
│   │   ├── dependencies.py         # Inyección de usuario autenticado (get_current_user, require_admin)
│   │   └── security.py             # PasswordManager: hash y verificación de contraseñas (PBKDF2)
│   ├── core/
│   │   ├── error_handlers.py       # Registro global de manejadores de error en FastAPI
│   │   ├── exceptions.py           # Excepciones personalizadas de la aplicación
│   │   └── responses.py            # Clase RespuestaAPI estandarizada
│   ├── database/
│   │   └── config.py               # Conexión a PostgreSQL, create_tables, get_db
│   ├── endpoints/
│   │   ├── auth.py                 # POST /auth/login, POST /auth/registrar
│   │   ├── usuarios.py             # GET/PUT/DELETE /usuarios/...
│   │   ├── productos.py            # GET/POST/PUT/DELETE /productos/...
│   │   ├── categorias.py           # GET/POST/PUT/DELETE /categorias/...
│   │   ├── descuentos_tienda.py    # GET/POST/PUT/DELETE /descuentos/...
│   │   ├── carrito.py              # GET/POST/DELETE /carrito/...
│   │   └── facturas.py             # GET/POST /facturas/...
│   ├── entities/
│   │   ├── usuario.py
│   │   ├── tienda.py
│   │   ├── catalogo.py
│   │   ├── categoria.py
│   │   ├── producto.py
│   │   ├── descuento.py
│   │   ├── carrito.py
│   │   ├── detalle_carrito.py
│   │   ├── factura.py
│   │   └── detalle_factura.py
│   └── crud/
│       ├── usuario_crud.py
│       ├── tienda_crud.py
│       ├── categoria_crud.py
│       ├── producto_crud.py
│       ├── descuento_crud.py
│       ├── carrito_crud.py
│       └── factura_crud.py
└── migrations/
    ├── env.py
    └── versions/
        └── 001_initial.py
```

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone <url-del-repo>
cd BackendProyectoTiendaOnline

# 2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con la DATABASE_URL de Neon

# 5. Ejecutar migraciones
python -m alembic upgrade head

# 6. Levantar el servidor
python main.py
```

El servidor queda disponible en `http://localhost:8000`.

---

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://usuario:contrasena@host/neondb?sslmode=require
```

---

## Inicialización automática

Al arrancar el servidor, el sistema ejecuta automáticamente:

- Creación de tablas si no existen (`create_tables`)
- Inicialización de la tienda raíz (`TiendaCrud.inicializar`)
- Carga de descuentos base (`DescuentoCrud.seed_descuentos_base`)
- Creación del administrador por defecto si no hay ninguno:
  - **Usuario:** `admin`
  - **Contraseña:** `Admin123!`

---

## Autenticación

La API usa autenticación por **token de sesión** (Bearer token). El flujo es:

1. `POST /auth/registrar` — crear cuenta (rol `cliente` o `administrador`)
2. `POST /auth/login` — obtener el token
3. Incluir el token en las cabeceras de cada petición protegida:
   ```
   Authorization: Bearer <token>
   ```

Las contraseñas se almacenan con **PBKDF2-HMAC-SHA256** y salt aleatorio.

---

## Manejo de errores

Los errores de la aplicación siguen una estructura estandarizada a través de excepciones personalizadas (`AppException` y subclases) capturadas por los handlers globales registrados en `core/error_handlers.py`.

| Excepción | Código HTTP |
|---|---|
| `UsuarioNoEncontrado` | 404 |
| `CredencialesInvalidas` | 401 |
| `UsuarioYaExiste` | 400 |
| `ProductoNoEncontrado` | 404 |
| `CategoriaNoEncontrada` | 404 |
| `StockInsuficiente` | 400 |
| `CarritoNoEncontrado` | 404 |
| `FacturaNoEncontrada` | 404 |
| `OperacionNoPermitida` | 403 |
| `DatosInvalidos` | 400 |

---

## Funcionalidades

- Registro e inicio de sesión con roles (Cliente / Administrador)
- Autenticación por token de sesión con contraseñas hasheadas (PBKDF2)
- API REST completa documentada con Swagger UI (`/docs`)
- Tienda con catálogo de productos organizados por categorías
- Carrito de compras con previsualización de descuento y total a pagar
- Descuentos configurables por el administrador según volumen de compra
- Generación de facturas con detalle persistido en base de datos
- Auditoría en Categorías y Productos (quién creó, quién editó)
- Eliminación lógica de usuarios (desactivación sin borrar registros)
- Panel de administrador: gestión de usuarios, categorías, productos y descuentos
- Manejo global de errores con respuestas estandarizadas
- CORS habilitado para integración con frontends

---

## Distribución del trabajo

| Integrante | Archivos |
|---|---|
| Kevin | `usuario.py`, `categoria.py`, `producto.py`, `usuario_crud.py`, `categoria_crud.py`, `producto_crud.py`, `database/config.py`, `main.py`, `endpoints/usuarios.py`, `endpoints/productos.py`, `endpoints/categorias.py` |
| Gabriel | `tienda.py`, `catalogo.py`, `descuento.py`, `tienda_crud.py`, `descuento_crud.py`, `endpoints/descuentos_tienda.py`, `migrations/versions/001_initial.py`, `README.md` |
| Sebas | `carrito.py`, `detalle_carrito.py`, `factura.py`, `detalle_factura.py`, `carrito_crud.py`, `factura_crud.py`, `endpoints/carrito.py`, `endpoints/facturas.py`, `auth/`, `core/` |