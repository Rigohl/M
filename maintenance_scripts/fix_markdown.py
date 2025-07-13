#!/usr/bin/env python3
"""
Script para corregir automáticamente problemas comunes en archivos Markdown.
"""

import os
import sys
import re

def fix_markdown_file(file_path):
    """Corrige problemas de formato en un archivo Markdown."""
    try:
        with open(file_path, 'r+', encoding='utf-8') as f:
            content = f.read()
            original_content = content

            # 1. Asegurar que el archivo termina con una nueva línea
            if not content.endswith('\n'):
                content += '\n'

            # 2. Corregir espaciado en listas
            content = re.sub(r'^\s*([*-]|\d+\.)\s{2,}(.*)', r'\1 \2', content, flags=re.MULTILINE)

            # 3. Añadir líneas en blanco alrededor de los encabezados
            content = re.sub(r'(?<!\n)\n(#{1,6} .*)', r'\n\n\1', content)
            content = re.sub(r'(#{1,6} .*)\n(?!\n)', r'\1\n\n', content)

            if content != original_content:
                f.seek(0)
                f.write(content)
                f.truncate()
                print(f"✅ Corregido: {os.path.basename(file_path)}")
        return True
    except Exception as e:
        print(f"❌ Error al procesar {file_path}: {e}")
        return False

def main():
    """Función principal que procesa los archivos pasados como argumentos."""
    if len(sys.argv) < 2:
        print("Uso: python fix_markdown.py <archivo1.md> <archivo2.md> ...")
        return 1

    all_successful = True
    for file_path in sys.argv[1:]:
        if not fix_markdown_file(file_path):
            all_successful = False
    
    return 0 if all_successful else 1

if __name__ == "__main__":
    sys.exit(main())
