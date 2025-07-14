# Despliegue y buenas prácticas para backend FastAPI en Supabase

## Requisitos mínimos

- Python 3.11 o superior
- Archivo `requirements.txt` actualizado
- Variables de entorno gestionadas de forma segura (no hardcodear claves)
- Logging estructurado
- Endpoint `/health` para monitoreo

## Ejecución local

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Ejemplo de Dockerfile (opcional, recomendado para Supabase)

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Variables de entorno recomendadas

- `JWT_SECRET`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUNO_API_KEY`

Configúralas en el dashboard de Supabase o usando un archivo `.env` (no lo subas al repo).

## Logging y monitoreo

El backend ya implementa logging estructurado. Puedes conectar servicios externos (Sentry, Datadog, etc.) si lo deseas.

## Endpoint de health check

El endpoint `/health` responde con `{"status": "ok"}` para monitoreo y readiness.

## Recomendaciones extra

- Mantén tus dependencias actualizadas.
- Usa HTTPS en producción.
- No expongas claves ni secretos en el código.
- Usa pruebas automáticas (`pytest`).

---
Para dudas sobre despliegue en Supabase, consulta la [documentación oficial](https://supabase.com/docs/guides/functions).
# Despliegue y buenas prácticas para backend FastAPI en Supabase

## Requisitos mínimos

- Python 3.11 o superior
- Archivo `requirements.txt` actualizado
- Variables de entorno gestionadas de forma segura (no hardcodear claves)
- Logging estructurado
- Endpoint `/health` para monitoreo

## Ejecución local

```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

## Ejemplo de Dockerfile (opcional, recomendado para Supabase)

```Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Variables de entorno recomendadas

- `JWT_SECRET`
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUNO_API_KEY`

Configúralas en el dashboard de Supabase o usando un archivo `.env` (no lo subas al repo).

## Logging y monitoreo

El backend ya implementa logging estructurado. Puedes conectar servicios externos (Sentry, Datadog, etc.) si lo deseas.

## Endpoint de health check

El endpoint `/health` responde con `{"status": "ok"}` para monitoreo y readiness.

## Recomendaciones extra

- Mantén tus dependencias actualizadas.
- Usa HTTPS en producción.
- No expongas claves ni secretos en el código.
- Usa pruebas automáticas (`pytest`).

---
Para dudas sobre despliegue en Supabase, consulta la [documentación oficial](https://supabase.com/docs/guides/functions).
## Backend Moderno Optimizado

Este backend está construido con Python y FastAPI, siguiendo buenas prácticas modernas:

- **FastAPI** como framework principal para APIs REST.
- **Pydantic** para validación y sanitización de datos.
- **Supabase** para autenticación y almacenamiento.
- **Integración centralizada con APIs externas** (OpenAI, Suno, etc.).
- **Logging y manejo de errores robusto**.
- **Pruebas unitarias y de integración** con pytest.
- **Estructura limpia y sin duplicados**.

### Instalación

1. Instala las dependencias:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Configura tus variables de entorno en `.env`.
3. Ejecuta el backend:
   ```bash
   uvicorn backend.main:app --reload
   ```

### Estructura recomendada

- `main.py`: Entrypoint FastAPI.
- `ai_integration.py`: Integración IA y APIs externas.
- `config.py`: Configuración y variables de entorno.
- `routes/`: Rutas adicionales.
- `tests/`: Pruebas unitarias y de integración.
- `utils/`, `error_handler.py`: Utilidades y manejo de errores.

### Pruebas

```bash
pytest backend/tests/
```

### Buenas prácticas

- Mantén la lógica de negocio en módulos separados.
- Usa Pydantic para validar todos los datos de entrada.
- Centraliza la configuración y credenciales.
- Documenta tus endpoints con docstrings y/o OpenAPI.
- Elimina código y carpetas duplicadas o no usadas.
### Detección y resolución automática de problemas
