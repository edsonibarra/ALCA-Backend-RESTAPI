# ALCA Real Estate API - Guía Completa de Endpoints

## Información General

**Base URL**: `http://localhost:8000/api/`  
**Autenticación**: JWT Bearer Token requerido para la mayoría de endpoints  
**Formato de respuesta**: JSON  

---

## 🔐 Autenticación

### Registro de Usuario
- **Endpoint**: `POST /api/user/register/`
- **Descripción**: Registra un nuevo usuario en el sistema
- **Autenticación**: No requerida
- **Body**:
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

### Obtener Token de Acceso
- **Endpoint**: `POST /api/token/`
- **Descripción**: Obtiene tokens JWT para autenticación
- **Autenticación**: No requerida
- **Body**:
```json
{
  "username": "string",
  "password": "string"
}
```
- **Respuesta**:
```json
{
  "access": "jwt_access_token",
  "refresh": "jwt_refresh_token"
}
```

### Refrescar Token
- **Endpoint**: `POST /api/token/refresh/`
- **Descripción**: Renueva el token de acceso usando el refresh token
- **Autenticación**: No requerida
- **Body**:
```json
{
  "refresh": "jwt_refresh_token"
}
```

### Información del Usuario Actual
- **Endpoint**: `GET /api/me/`
- **Descripción**: Obtiene información del usuario autenticado
- **Autenticación**: Requerida
- **Respuesta**:
```json
{
  "id": 1,
  "username": "string"
}
```

---

## 🏠 Propiedades en Venta (Houses for Sale)

### Listar Propiedades en Venta
- **Endpoint**: `GET /api/houses-for-sale/`
- **Descripción**: Lista todas las propiedades en venta con paginación
- **Autenticación**: Requerida
- **Parámetros de consulta**:
  - `page`: Número de página (default: 1)
  - `page_size`: Elementos por página (default: 20)
  - `owner_id`: Filtrar por ID del propietario
  - `search`: Búsqueda en título, calle, colonia, ciudad, comentarios
  - `ordering`: Ordenar por campos (-created_at, selling_cost, etc.)

#### Filtros Avanzados:
- **Precio**: `min_price`, `max_price`
- **Ubicación**: `city`, `nghood`, `postal_code`
- **Características**: `min_beds`, `max_beds`, `min_baths`, `max_baths`
- **Área**: `min_construccion`, `max_construccion`, `min_superficie`, `max_superficie`
- **Amenidades**: `infonavit`, `patio`, `negociable`
- **Otros**: `min_cochera`, `max_cochera`, `min_minisplits`, `max_minisplits`
- **Estado**: `estatus`
- **Pago**: `metodo_de_pago`
- **Servicios**: `servicios`

### Crear Propiedad en Venta
- **Endpoint**: `POST /api/houses-for-sale/`
- **Descripción**: Crea una nueva propiedad en venta
- **Autenticación**: Requerida
- **Body**:
```json
{
  "title": "string",
  "street": "string",
  "number": 123,
  "nghood": "string",
  "postal_code": 12345,
  "city": "string",
  "selling_cost": 1000000,
  "infonavit": true,
  "comments": "string",
  "owner": 1,
  "estatus": "string",
  "cochera": 2,
  "baths": 2.5,
  "patio": true,
  "beds": 3,
  "minisplits": 2,
  "construccion": 120.5,
  "superficie": 200.0,
  "servicios": "string",
  "metodo_de_pago": "string",
  "negociable": true
}
```

### Obtener Propiedad Específica
- **Endpoint**: `GET /api/houses-for-sale/{id}/`
- **Descripción**: Obtiene detalles de una propiedad específica
- **Autenticación**: Requerida

### Actualizar Propiedad
- **Endpoint**: `PUT /api/houses-for-sale/{id}/`
- **Endpoint**: `PATCH /api/houses-for-sale/{id}/`
- **Descripción**: Actualiza una propiedad existente
- **Autenticación**: Requerida

### Eliminar Propiedad
- **Endpoint**: `DELETE /api/houses-for-sale/{id}/`
- **Descripción**: Elimina una propiedad
- **Autenticación**: Requerida

### Subir Imágenes a Propiedad en Venta
- **Endpoint**: `POST /api/houses-for-sale/{id}/upload_images/`
- **Descripción**: Sube múltiples imágenes a una propiedad
- **Autenticación**: Requerida
- **Content-Type**: `multipart/form-data`
- **Campos**:
  - `images`: Archivos de imagen (múltiples)
  - `caption`: Descripción de la imagen (opcional)
  - `is_main`: Si es imagen principal (boolean, opcional)
  - `order`: Orden de visualización (número, opcional)

### Búsqueda por Ubicación
- **Endpoint**: `GET /api/houses-for-sale/search_by_location/`
- **Descripción**: Búsqueda específica por ubicación
- **Autenticación**: Requerida
- **Parámetros**: `city`, `nghood`, `postal_code`

### Búsqueda por Rango de Precio
- **Endpoint**: `GET /api/houses-for-sale/price_range/`
- **Descripción**: Búsqueda por rango de precio
- **Autenticación**: Requerida
- **Parámetros**: `min_price`, `max_price`

---

## 🏡 Propiedades en Renta (Houses for Rent)

### Listar Propiedades en Renta
- **Endpoint**: `GET /api/houses-for-rent/`
- **Descripción**: Lista todas las propiedades en renta con paginación
- **Autenticación**: Requerida
- **Parámetros similares a houses-for-sale**

#### Filtros Específicos para Renta:
- **Precio**: `min_rent`, `max_rent`
- **Ubicación**: `city`, `nghood`, `postal_code`
- **Características**: `min_bedrooms`, `max_bedrooms`, `min_bathrooms`, `max_bathrooms`
- **Amenidades**: `garage`, `patio`, `petfriendly`
- **Otros**: `min_minisplits`, `max_minisplits`
- **Servicios**: `included_services`

### Crear Propiedad en Renta
- **Endpoint**: `POST /api/houses-for-rent/`
- **Descripción**: Crea una nueva propiedad en renta
- **Autenticación**: Requerida
- **Body**:
```json
{
  "title": "string",
  "street": "string",
  "number": 123,
  "nghood": "string",
  "postal_code": 12345,
  "city": "string",
  "rent_cost": 15000,
  "garage": true,
  "bedrooms": 3,
  "bathrooms": 2.5,
  "minisplits": 2,
  "included_services": "string",
  "petfriendly": true,
  "comments": "string",
  "patio": true,
  "owner": 1
}
```

### Operaciones CRUD Completas
- **GET** `/api/houses-for-rent/{id}/` - Obtener específica
- **PUT/PATCH** `/api/houses-for-rent/{id}/` - Actualizar
- **DELETE** `/api/houses-for-rent/{id}/` - Eliminar

### Subir Imágenes a Propiedad en Renta
- **Endpoint**: `POST /api/houses-for-rent/{id}/upload_images/`
- **Descripción**: Sube múltiples imágenes a una propiedad en renta
- **Autenticación**: Requerida
- **Content-Type**: `multipart/form-data`
- **Campos**: Mismos que houses-for-sale

### Búsqueda por Ubicación
- **Endpoint**: `GET /api/houses-for-rent/search_by_location/`
- **Descripción**: Búsqueda específica por ubicación
- **Autenticación**: Requerida

### Búsqueda por Rango de Renta
- **Endpoint**: `GET /api/houses-for-rent/rent_range/`
- **Descripción**: Búsqueda por rango de renta mensual
- **Autenticación**: Requerida
- **Parámetros**: `min_rent`, `max_rent`

---

## 📸 Gestión de Imágenes de Propiedades

### Listar Imágenes
- **Endpoint**: `GET /api/property-images/`
- **Descripción**: Lista todas las imágenes con filtros
- **Autenticación**: Requerida
- **Parámetros**:
  - `content_type`: Tipo de propiedad (house_for_sale, house_for_rent)
  - `object_id`: ID de la propiedad específica

### Crear Imagen
- **Endpoint**: `POST /api/property-images/`
- **Descripción**: Sube una nueva imagen
- **Autenticación**: Requerida
- **Content-Type**: `multipart/form-data`

### Obtener Imagen Específica
- **Endpoint**: `GET /api/property-images/{id}/`
- **Descripción**: Obtiene detalles de una imagen específica
- **Autenticación**: Requerida
- **Respuesta**:
```json
{
  "id": 1,
  "image": "path/to/image.jpg",
  "image_url": "presigned_url",
  "secure_url": "presigned_url",
  "caption": "string",
  "is_main": true,
  "order": 1,
  "created_at": "2025-01-01T00:00:00Z"
}
```

### Actualizar Imagen
- **Endpoint**: `PUT/PATCH /api/property-images/{id}/`
- **Descripción**: Actualiza metadatos de una imagen
- **Autenticación**: Requerida

### Eliminar Imagen
- **Endpoint**: `DELETE /api/property-images/{id}/`
- **Descripción**: Elimina una imagen del sistema y S3
- **Autenticación**: Requerida

### Obtener URL Segura
- **Endpoint**: `GET /api/property-images/{id}/secure_url/`
- **Descripción**: Genera una URL presignada para acceder a la imagen
- **Autenticación**: Requerida
- **Parámetros**:
  - `expiration`: Tiempo de expiración en segundos (default: 3600)
- **Respuesta**:
```json
{
  "secure_url": "https://alca-inmo.s3.amazonaws.com/...",
  "expires_in": 3600,
  "image_id": 1
}
```

### Redireccionar a Imagen
- **Endpoint**: `GET /api/property-images/{id}/redirect_to_image/`
- **Descripción**: Redirecciona directamente a la URL segura de la imagen
- **Autenticación**: Requerida
- **Parámetros**:
  - `expiration`: Tiempo de expiración en segundos (default: 3600)

### Subida Masiva de Imágenes
- **Endpoint**: `POST /api/property-images/bulk_upload/`
- **Descripción**: Sube múltiples imágenes de una vez
- **Autenticación**: Requerida
- **Content-Type**: `multipart/form-data`
- **Campos**:
  - `images`: Múltiples archivos de imagen
  - `content_type`: Tipo de propiedad (house_for_sale, house_for_rent)
  - `object_id`: ID de la propiedad
  - `caption`, `is_main`, `order`: Opcionales

### Establecer como Imagen Principal
- **Endpoint**: `PATCH /api/property-images/{id}/set_as_main/`
- **Descripción**: Establece una imagen como principal para su propiedad
- **Autenticación**: Requerida

---

## 👥 Gestión de Propietarios

### Listar Propietarios
- **Endpoint**: `GET /api/owners/`
- **Descripción**: Lista todos los propietarios
- **Autenticación**: Requerida

### Crear Propietario
- **Endpoint**: `POST /api/owners/`
- **Descripción**: Crea un nuevo propietario
- **Autenticación**: Requerida

### Operaciones CRUD Completas
- **GET** `/api/owners/{id}/` - Obtener específico
- **PUT/PATCH** `/api/owners/{id}/` - Actualizar
- **DELETE** `/api/owners/{id}/` - Eliminar

---

## 🔧 Autenticación de API

### Headers Requeridos

Para endpoints que requieren autenticación:

```http
Authorization: Bearer {jwt_access_token}
Content-Type: application/json
```

Para subida de archivos:

```http
Authorization: Bearer {jwt_access_token}
Content-Type: multipart/form-data
```

---

## 📝 Códigos de Respuesta HTTP

- **200 OK**: Operación exitosa
- **201 Created**: Recurso creado exitosamente
- **400 Bad Request**: Datos inválidos en la solicitud
- **401 Unauthorized**: Token de autenticación requerido o inválido
- **403 Forbidden**: Sin permisos para realizar la operación
- **404 Not Found**: Recurso no encontrado
- **500 Internal Server Error**: Error interno del servidor

---

## 🔍 Ejemplos de Uso

### Ejemplo: Crear una propiedad y subir imágenes

1. **Autenticarse**:
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

2. **Crear propiedad**:
```bash
curl -X POST http://localhost:8000/api/houses-for-sale/ \
  -H "Authorization: Bearer {token}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Casa en venta", "owner": 1, "selling_cost": 1000000}'
```

3. **Subir imágenes**:
```bash
curl -X POST http://localhost:8000/api/houses-for-sale/1/upload_images/ \
  -H "Authorization: Bearer {token}" \
  -F "images=@image1.jpg" \
  -F "images=@image2.jpg" \
  -F "is_main=true"
```

### Ejemplo: Buscar propiedades con filtros

```bash
curl -X GET "http://localhost:8000/api/houses-for-sale/?min_price=500000&max_price=2000000&city=Guadalajara&min_beds=2" \
  -H "Authorization: Bearer {token}"
```

### Ejemplo: Obtener URL segura de imagen

```bash
curl -X GET "http://localhost:8000/api/property-images/1/secure_url/?expiration=7200" \
  -H "Authorization: Bearer {token}"
```

---

## 🛡️ Seguridad de Imágenes

- **Almacenamiento**: Todas las imágenes se almacenan en S3 con ACL privado
- **Acceso**: Solo a través de URLs presignadas con expiración
- **Autenticación**: Requerida para todas las operaciones de imágenes
- **Bucket**: `alca-inmo` (privado)
- **Expiración por defecto**: 1 hora (3600 segundos)

---

## 📊 Paginación

Todos los endpoints de listado soportan paginación:

```json
{
  "count": 100,
  "next": "http://localhost:8000/api/houses-for-sale/?page=2",
  "previous": null,
  "results": [...]
}
```

**Parámetros de paginación**:
- `page`: Número de página
- `page_size`: Elementos por página (máximo 100)

---

## 🔄 Filtrado y Ordenamiento

### Filtrado
Usar parámetros de consulta para filtrar resultados:
- Filtros exactos: `?city=Guadalajara`
- Filtros de rango: `?min_price=100000&max_price=500000`
- Filtros de texto: `?search=casa moderna`

### Ordenamiento
Usar el parámetro `ordering`:
- Ascendente: `?ordering=selling_cost`
- Descendente: `?ordering=-selling_cost`
- Múltiple: `?ordering=-created_at,selling_cost`

---

## 📱 Notas para Desarrollo Frontend

1. **Tokens JWT**: Almacenar de forma segura y renovar automáticamente
2. **Imágenes**: Usar las URLs seguras proporcionadas por la API
3. **Filtros**: Implementar filtros dinámicos para mejor UX
4. **Paginación**: Implementar scroll infinito o paginación tradicional
5. **Subida de archivos**: Mostrar progreso de subida para mejor UX
6. **Caché**: Las URLs de imágenes expiran, no cachear por mucho tiempo

---

## 🐛 Solución de Problemas

### Error 401 - Unauthorized
- Verificar que el token JWT esté incluido en el header
- Verificar que el token no haya expirado
- Renovar token usando el refresh endpoint

### Error 400 - Bad Request
- Verificar formato de datos enviados
- Verificar campos requeridos
- Verificar tipos de datos (números, strings, etc.)

### Imágenes no se muestran
- Verificar que la URL no haya expirado
- Generar nueva URL segura
- Verificar permisos de acceso

### Error de subida de imágenes
- Verificar tamaño de archivo (máximo 10MB)
- Verificar formato de imagen (JPEG, PNG)
- Verificar que el Content-Type sea multipart/form-data