# Scripts de Mantenimiento del Proyecto

Este directorio contiene scripts para mantener y corregir errores comunes en el proyecto.

## Cómo usar los scripts

### 1. Corregir todos los errores (Recomendado)

Este es el script principal que ejecuta todas las correcciones necesarias, incluyendo la instalación de dependencias y la limpieza de archivos Markdown.

**Uso:**

```bash
python maintenance_scripts/fix_project_errors.py
```

### 2. Instalar dependencias de Python

Si solo necesitas asegurarte de que todas las dependencias de Python estén instaladas, puedes usar este script.

**Uso:**

```bash
python maintenance_scripts/install_dependencies.py
```

### 3. Corregir archivos Markdown

Si solo quieres corregir el formato de los archivos `.md` del proyecto.

**Uso:**

```bash
python maintenance_scripts/fix_markdown.py <ruta_al_archivo.md>
```

Por ejemplo:

```bash
python maintenance_scripts/fix_markdown.py README.md
```

---
**Nota:** Asegúrate de tener Python instalado en tu sistema para poder ejecutar estos scripts.
