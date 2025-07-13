#!/usr/bin/env python3
"""
Script para corregir automáticamente problemas comunes en archivos markdown
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple

def fix_markdown_file(file_path: str) -> Tuple[int, List[str]]:
    """
    Corrige problemas comunes en un archivo markdown
    
    Args:
        file_path: Ruta al archivo markdown
        
    Returns:
        Tuple con el número de correcciones y lista de problemas corregidos
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    fixes = []
    
    # 1. Agregar una nueva línea al final del archivo si no existe
    if not content.endswith('\n'):
        content = content + '\n'
        fixes.append("Añadida nueva línea al final del archivo")
    
    # 2. Corregir espacios después de marcadores de lista [Expected: 1; Actual: 3]
    content = re.sub(r'^(\s*)(\d+\.|\*|\+|\-)(\s{2,})(.+)$', r'\1\2 \4', content, flags=re.MULTILINE)
    
    # 3. Corregir indentación de listas anidadas
    content = re.sub(r'^(\s{4,})(\*|\+|\-)(\s+)(.+)$', r'  \1\2 \4', content, flags=re.MULTILINE)
    
    # 4. Asegurar que los encabezados tienen líneas en blanco alrededor
    # Antes de encabezados
    content = re.sub(r'([^\n])\n(#{1,6}\s.+)$', r'\1\n\n\2', content, flags=re.MULTILINE)
    # Después de encabezados
    content = re.sub(r'^(#{1,6}\s.+)\n([^\n])', r'\1\n\n\2', content, flags=re.MULTILINE)
    
    # 5. Asegurar que las listas tienen líneas en blanco alrededor
    # Antes de listas
    content = re.sub(r'([^\n])\n^(\s*(?:\d+\.|\*|\+|\-)\s.+)$', r'\1\n\n\2', content, flags=re.MULTILINE)
    # Después de listas
    list_end_pattern = r'^(\s*(?:\d+\.|\*|\+|\-)\s.+)\n((?!(?:\s*(?:\d+\.|\*|\+|\-)\s)).+)'
    content = re.sub(list_end_pattern, r'\1\n\n\2', content, flags=re.MULTILINE)
    
    # 6. Corregir bloques de código para que tengan lenguaje especificado
    content = re.sub(r'```\s*\n', r'```text\n', content)
    
    # Contar número de correcciones
    if content != original_content:
        fixes.append("Corregidos problemas de formato markdown")
        
    # Guardar el archivo si hubo cambios
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
    return len(fixes), fixes


def main():
    """Función principal"""
    if len(sys.argv) < 2:
        print("Uso: python fix-markdown.py <ruta_archivo_markdown> [ruta_archivo_markdown ...]")
        return 1
    
    total_fixes = 0
    
    for file_path in sys.argv[1:]:
        if not os.path.exists(file_path):
            print(f"❌ Archivo no encontrado: {file_path}")
            continue
            
        if not file_path.endswith('.md'):
            print(f"❌ No es un archivo markdown: {file_path}")
            continue
            
        print(f"🔍 Procesando {file_path}...")
        num_fixes, fixes = fix_markdown_file(file_path)
        
        if num_fixes > 0:
            print(f"✅ Realizadas {num_fixes} correcciones en {file_path}")
            for fix in fixes:
                print(f"  - {fix}")
            total_fixes += num_fixes
        else:
            print(f"✓ No se necesitaron correcciones en {file_path}")
    
    print(f"\n🎉 Total de correcciones: {total_fixes}")
    return 0


if __name__ == "__main__":
    sys.exit(main())