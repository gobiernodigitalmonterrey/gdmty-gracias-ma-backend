# GDMTY Gracias MA Backend

## Requisitos previos

- Python 3.8 o superior
- MySQL
- pip (gestor de paquetes de Python)

## Instalación

1. Clonar el repositorio:

```bash
git clone https://github.com/gobiernodigitalmonterrey/gdmty-gracias-ma-backend.git
cd gdmty-gracias-ma-backend
```

2. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

## Configuración de la base de datos

1. Crear una base de datos MySQL llamada `gracias_ma`:

```sql
CREATE DATABASE gracias_ma;
```

2. Configurar las credenciales de la base de datos:

El proyecto está configurado para conectarse a MySQL con las siguientes credenciales:

```
Usuario: root
Contraseña: 1234
Host: localhost
Base de datos: gracias_ma
```

Si necesitas cambiar estas credenciales, modifica el archivo `app/db/database.py`:

```python
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://usuario:contraseña@host/gracias_ma"
```

## Creacion de archivo .env para las credenciales de GCP

```
PATH_KEYS_JSON=/Users/martin/Desktop/SIGA/gdmty-gracias-ma-backend/app/keys/god-datastore-dev-24292c5052e8.json
BUCKET_NAME=god-gracias-ma
```

## Ejecución del proyecto

1. Iniciar el servidor de desarrollo:

```bash
python -m dotenv run -- uvicorn main:app --reload
```

## Ejecutar el proyecto con Dockerfile

```bash
docker build -t nombre_contendor . 
```

```bash
docker run -d -p 8000:8000 nombre_contendor
```


El servidor se iniciará en `http://127.0.0.1:8000`

## Documentación de la API

Una vez que el servidor esté en ejecución, puedes acceder a la documentación interactiva de la API en:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Endpoints disponibles

### Formulario

- **POST** `/formulario/enviar_formulario`: Envía un nuevo formulario con los datos del usuario y archivos adjuntos (INE frontal, INE reverso, acta de nacimiento).

## Estructura del proyecto

- `main.py`: Punto de entrada de la aplicación
- `app/db/`: Configuración de la base de datos y modelos
- `app/routers/`: Definición de rutas y endpoints
- `app/views/`: Lógica de negocio
- `app/schemas.py`: Esquemas de datos para validación
- `uploads/`: Directorio donde se almacenan los archivos subidos

## Notas adicionales

- El sistema crea automáticamente un directorio `uploads` para almacenar los archivos subidos.
- Las tablas de la base de datos se crean automáticamente al iniciar la aplicación.