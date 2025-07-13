#!/usr/bin/env python3
"""
Script maestro para corregir todos los errores del proyecto
"""

import os
import sys
import subprocess

def run_command(command, cwd=None):
    """Ejecuta un comando y devuelve el código de salida y la salida"""
    try:
        process = subprocess.Popen(
            command, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            cwd=cwd
        )
        stdout, stderr = process.communicate()
        return process.returncode, stdout, stderr
    except Exception as e:
        return -1, "", str(e)

def fix_python_dependencies():
    """Instala las dependencias de Python."""
    print("\n🔧 Instalando dependencias de Python...")
    script_path = os.path.join(os.path.dirname(__file__), "install_dependencies.py")
    if not os.path.exists(script_path):
        print(f"❌ Error: No se encontró el script {script_path}")
        return False
    
    returncode, stdout, stderr = run_command([sys.executable, script_path])
    print(stdout)
    if stderr:
        print(f"Error en install_dependencies.py: {stderr}")
    return returncode == 0

def fix_markdown_files():
    """Corrige todos los archivos Markdown en el proyecto."""
    print("\n🔧 Corrigiendo archivos Markdown...")
    script_path = os.path.join(os.path.dirname(__file__), "fix_markdown.py")
    if not os.path.exists(script_path):
        print(f"❌ Error: No se encontró el script {script_path}")
        return False

    project_root = "/workspaces/M"
    markdown_files_to_fix = []
    for root, _, files in os.walk(project_root):
        for file in files:
            if file.endswith(".md"):
                markdown_files_to_fix.append(os.path.join(root, file))

    if not markdown_files_to_fix:
        print("No se encontraron archivos Markdown para corregir.")
        return True

    returncode, stdout, stderr = run_command([sys.executable, script_path] + markdown_files_to_fix)
    print(stdout)
    if stderr:
        print(f"Error en fix_markdown.py: {stderr}")
    return returncode == 0

def main():
    """Función principal que ejecuta todas las correcciones."""
    print("🚀 Iniciando corrección de errores del proyecto...")
    
    # 1. Instalar dependencias de Python
    if not fix_python_dependencies():
        print("\n⚠️ Falló la instalación de dependencias de Python. Abortando.")
        return 1
        
    # 2. Corregir archivos Markdown
    if not fix_markdown_files():
        print("\n⚠️ Falló la corrección de archivos Markdown.")
        return 1

    print("\n✅ Proceso de corrección completado.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
