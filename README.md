# La Tienda de Gerardo — Backend

Proyecto de tienda online desarrollado en Python con SQLAlchemy ORM y base de datos PostgreSQL en Neon.

## Video demostrativo

> 🎥 URL del video: [_\[pendiente de agregar\]_](https://youtu.be/QsUPNqouevY)

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

## Estructura del proyecto
```
├── main.py
├── sistema_gestion.py
├── requirements.txt
├── alembic.ini
├── .env
├── .env.example
├── src/
│   ├── database/
│   │   └── config.py
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

## Distribución del trabajo

| Integrante | Archivos |
|---|---|
| Kevin | `usuario.py`, `categoria.py`, `producto.py`, `usuario_crud.py`, `categoria_crud.py`, `producto_crud.py`, `database/config.py`, `main.py` |
| Gabriel | `tienda.py`, `catalogo.py`, `descuento.py`, `tienda_crud.py`, `descuento_crud.py`, `migrations/versions/001_initial.py`, `README.md` |
| Sebas | `carrito.py`, `detalle_carrito.py`, `factura.py`, `detalle_factura.py`, `carrito_crud.py`, `factura_crud.py` |

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

# 6. Ejecutar el sistema
python main.py
```

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:
```
DATABASE_URL=postgresql://usuario:contrasena@host/neondb?sslmode=require
```


## Funcionalidades

- Registro e inicio de sesión con roles (Cliente / Administrador)
- Tienda con catálogo de productos organizados por categorías
- Carrito de compras con previsualización de descuento y total a pagar
- Descuentos configurables por el administrador según volumen de compra
- Generación de facturas con detalle persistido en base de datos
- Auditoría en Categorías y Productos (quién creó, quién editó)
- Eliminación lógica de usuarios (desactivación sin borrar registros)
- Panel de administrador: gestión de usuarios, categorías, productos y descuentos