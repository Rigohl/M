#!/usr/bin/env python3
"""
Script para instalar las dependencias de Python listadas en requirements.txt.
"""

import os
import sys
import subprocess

def install_dependencies():
    """Instala las dependencias desde backend/requirements.txt."""
    requirements_path = "/workspaces/M/backend/requirements.txt"
    if not os.path.exists(requirements_path):
        print(f"❌ Error: No se encontró el archivo {requirements_path}")
        return False

    print(f"📦 Instalando dependencias desde {requirements_path}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_path])
        print("✅ Dependencias instaladas correctamente.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def main():
    """Función principal."""
    if not install_dependencies():
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
