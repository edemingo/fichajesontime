# Configuración de Variables de Entorno

Este proyecto utiliza variables de entorno para configurar la conexión con la API de FactorialHR.

## Archivo config.env

Crea un archivo `config.env` en la carpeta `api/` con las siguientes variables:

```env
apikey=tu_api_key_aqui
apiURL=https://api.factorialhr.com/api/2025-04-01/
```

## Variables requeridas

- **apikey**: Tu API key de FactorialHR
- **apiURL**: URL base de la API (por defecto: https://api.factorialhr.com/api/2025-04-01/)

## Uso en el código

Las variables se cargan automáticamente en la clase `Factorial`:

```python
from dotenv import load_dotenv
import os

# Cargar variables desde config.env
load_dotenv('config.env')

api_key = os.getenv('apikey')
api_url = os.getenv('apiURL')
```

## Seguridad

⚠️ **Importante**: Nunca commits el archivo `config.env` al repositorio. Asegúrate de que esté en `.gitignore`.

El archivo `.env.example` contiene un ejemplo de configuración sin valores reales.