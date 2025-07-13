# Scripts de Mantenimiento del Proyecto

Este directorio contiene scripts para mantener y corregir errores comunes en el proyecto.

## Herramientas disponibles

### fix_project_errors.py

Script maestro que corrige múltiples tipos de errores en el proyecto:

- Errores de importación en Python
- Errores de TypeScript
- Errores de formato en Markdown

Uso:

```bash
python scripts/fix_project_errors.py
```

### install_dependencies.py

Instala las dependencias Python faltantes que se detectan en los archivos del backend:

```bash
python scripts/install_dependencies.py
```

### fix-markdown.py

Corrige errores comunes en archivos Markdown:

```bash
python scripts/fix-markdown.py archivo1.md archivo2.md
```

## Buenas prácticas de mantenimiento

1. Ejecuta regularmente el script `fix_project_errors.py` para mantener el código limpio.
2. Asegúrate de que todas las dependencias estén actualizadas en `requirements.txt`.
3. Utiliza herramientas de linting como `flake8` para Python y `eslint` para TypeScript.
