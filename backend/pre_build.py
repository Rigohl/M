#!/usr/bin/env python3
"""
Script Pre-Build para resolver problemas comunes antes de la compilación
Se ejecuta automáticamente antes del comando de build en Vercel
"""

import json
import os
import sys
import subprocess
import shutil
from typing import Dict, List, Optional, Any


def setup_npmrc() -> None:
    """Configura .npmrc para manejar dependencias problemáticas"""
    npmrc_content = """# Configuración para resolver conflictos de dependencias
legacy-peer-deps=true
auto-install-peers=true
strict-peer-deps=false
"""
    with open(".npmrc", "w") as f:
        f.write(npmrc_content)
    print("✅ Configuración .npmrc aplicada")


def fix_react_dependencies() -> None:
    """Verifica y soluciona problemas con las dependencias de React"""
    try:
        # Cargar package.json
        with open("package.json", "r") as f:
            package_data = json.load(f)
        
        # Verificar si existe un conflicto de versión de React
        has_cmdk = False
        react_version = None
        
        if "dependencies" in package_data:
            if "cmdk" in package_data["dependencies"]:
                has_cmdk = True
            if "react" in package_data["dependencies"]:
                react_version = package_data["dependencies"]["react"]
        
        # Si tenemos React 19 y cmdk, ajustar la versión de React a 18
        if has_cmdk and react_version and ("19" in react_version):
            print("⚠️ Detectado conflicto entre React 19 y cmdk")
            package_data["dependencies"]["react"] = "^18.2.0"
            if "react-dom" in package_data["dependencies"]:
                package_data["dependencies"]["react-dom"] = "^18.2.0"
            
            # Guardar cambios
            with open("package.json", "w") as f:
                json.dump(package_data, f, indent=2)
            print("✅ Versión de React ajustada a 18.2.0 para compatibilidad con cmdk")
    except Exception as e:
        print(f"❌ Error al procesar package.json: {e}")


def clean_node_modules() -> None:
    """Limpia node_modules si es necesario para una instalación fresca"""
    if os.path.exists("node_modules"):
        try:
            # Verificar si existe lock
            has_issues = False
            if os.path.exists("package-lock.json"):
                try:
                    with open("package-lock.json", "r") as f:
                        lock_data = json.load(f)
                    if "lockfileVersion" in lock_data and lock_data["lockfileVersion"] < 2:
                        has_issues = True
                except:
                    has_issues = True
            
            # Si encontramos problemas en el lock, eliminar node_modules
            if has_issues:
                print("⚠️ Detectados posibles problemas con node_modules, limpiando...")
                shutil.rmtree("node_modules")
                if os.path.exists("package-lock.json"):
                    os.remove("package-lock.json")
                print("✅ node_modules eliminado para instalación fresca")
        except Exception as e:
            print(f"❌ Error al limpiar node_modules: {e}")


def setup_vercel_config() -> None:
    """Configura vercel.json optimizado si no existe"""
    if not os.path.exists("vercel.json"):
        try:
            vercel_config = {
                "version": 2,
                "builds": [
                    {
                        "src": "package.json",
                        "use": "@vercel/node",
                        "config": {
                            "installCommand": "python3 backend/pre_build.py && npm install --legacy-peer-deps"
                        }
                    }
                ],
                "routes": [
                    { "src": "/(.*)", "dest": "/" }
                ],
                "env": {
                    "NODE_OPTIONS": "--max-old-space-size=4096"
                }
            }
            
            with open("vercel.json", "w") as f:
                json.dump(vercel_config, f, indent=2)
                
            print("✅ vercel.json creado con configuración optimizada")
        except Exception as e:
            print(f"❌ Error al crear vercel.json: {e}")


def update_build_script() -> None:
    """Actualiza el script de build en package.json para incluir verificaciones"""
    try:
        if os.path.exists("package.json"):
            with open("package.json", "r") as f:
                package_data = json.load(f)
            
            if "scripts" not in package_data:
                package_data["scripts"] = {}
                
            # Agregar script prebuild si no existe
            if "prebuild" not in package_data["scripts"]:
                package_data["scripts"]["prebuild"] = "python3 backend/pre_build.py"
                
            # Guardar cambios
            with open("package.json", "w") as f:
                json.dump(package_data, f, indent=2)
                
            print("✅ Script prebuild configurado en package.json")
    except Exception as e:
        print(f"❌ Error al actualizar package.json: {e}")


def main() -> None:
    """Función principal que ejecuta todas las verificaciones pre-build"""
    print("🔍 Ejecutando verificaciones pre-build...")
    
    # Ejecutar todas las verificaciones
    setup_npmrc()
    fix_react_dependencies()
    clean_node_modules()
    setup_vercel_config()
    update_build_script()
    
    print("\n✅ Pre-build completado. Listo para iniciar build!")


if __name__ == "__main__":
    main()