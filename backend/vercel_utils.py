#!/usr/bin/env python3
"""
Utilidades para la integración con Vercel
Este módulo proporciona funciones para trabajar con despliegues en Vercel
"""

import json
import os
import subprocess
import sys
from typing import Dict, List, Optional, Any


class VercelDeployHelper:
    """Clase para ayudar con los despliegues en Vercel"""

    @staticmethod
    def create_vercel_json(settings: Optional[Dict[str, Any]] = None) -> None:
        """
        Crea o actualiza un archivo vercel.json con la configuración óptima
        
        Args:
            settings: Configuración personalizada para vercel.json
        """
        default_settings = {
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
        
        # Combinar configuraciones
        if settings:
            for key, value in settings.items():
                if isinstance(value, dict) and key in default_settings and isinstance(default_settings[key], dict):
                    default_settings[key].update(value)
                else:
                    default_settings[key] = value
        
        try:
            with open("vercel.json", "w") as f:
                json.dump(default_settings, f, indent=2)
            print("✅ Archivo vercel.json creado con éxito")
        except Exception as e:
            print(f"❌ Error al crear vercel.json: {e}")

    @staticmethod
    def analyze_build_logs(log_path: str) -> Dict[str, Any]:
        """
        Analiza los logs de build de Vercel para detectar errores
        
        Args:
            log_path: Ruta al archivo de log
            
        Returns:
            Diccionario con análisis de errores encontrados
        """
        if not os.path.exists(log_path):
            return {"error": "Archivo de log no encontrado"}
            
        errors = {
            "dependency_conflicts": [],
            "build_errors": [],
            "memory_issues": False,
            "timeout_issues": False
        }
        
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines):
                # Detectar errores de dependencias
                if "npm error ERESOLVE could not resolve" in line:
                    context = "".join(lines[i:i+15])
                    errors["dependency_conflicts"].append(context)
                
                # Detectar errores de memoria
                if "JavaScript heap out of memory" in line:
                    errors["memory_issues"] = True
                    
                # Detectar timeouts
                if "Timed out" in line or "timed out" in line:
                    errors["timeout_issues"] = True
                    
                # Otros errores de build
                if "Error:" in line and "npm error" not in line:
                    errors["build_errors"].append(line.strip())
                    
            return errors
        except Exception as e:
            return {"error": f"Error al analizar log: {str(e)}"}
    
    @staticmethod
    def verify_project_structure() -> List[str]:
        """
        Verifica la estructura del proyecto para buenas prácticas de Vercel
        
        Returns:
            Lista de problemas o recomendaciones encontrados
        """
        issues = []
        
        # Verificar archivos importantes
        important_files = [
            ("package.json", "Archivo de configuración de Node.js"),
            (".npmrc", "Configuración de NPM para manejo de dependencias"),
            ("next.config.js", "Configuración de Next.js"),
            ("tsconfig.json", "Configuración de TypeScript")
        ]
        
        for file_path, description in important_files:
            if not os.path.exists(file_path):
                issues.append(f"Falta {file_path}: {description}")
                
        # Verificar configuración de package.json
        if os.path.exists("package.json"):
            try:
                with open("package.json", "r") as f:
                    package_data = json.load(f)
                
                if "engines" not in package_data:
                    issues.append("Se recomienda especificar versiones de Node.js en 'engines' en package.json")
                    
                if "scripts" in package_data and "build" in package_data["scripts"]:
                    build_script = package_data["scripts"]["build"]
                    if "prebuild" not in package_data["scripts"]:
                        issues.append("Considera añadir un script 'prebuild' para verificar dependencias")
            except:
                issues.append("No se pudo analizar package.json")
                
        # Verificar directorio de build
        build_dirs = [".next", "dist", "build", "out"]
        has_build_dir = any(os.path.isdir(d) for d in build_dirs)
        if not has_build_dir:
            issues.append("No se detectó directorio de build (.next, dist, build, out)")
                
        return issues


def run_pre_deployment_checks() -> None:
    """Ejecuta verificaciones previas al despliegue"""
    from dependency_checker import DependencyChecker
    
    print("🔍 Ejecutando verificaciones pre-despliegue...")
    
    # Verificar dependencias
    checker = DependencyChecker()
    conflicts = checker.check_react_version_conflicts()
    if conflicts:
        print(f"⚠️ Se encontraron {len(conflicts)} conflictos de dependencias")
        checker.generate_npmrc()
        
    # Verificar estructura del proyecto
    helper = VercelDeployHelper()
    issues = helper.verify_project_structure()
    if issues:
        print("\n⚠️ Se encontraron problemas en la estructura del proyecto:")
        for issue in issues:
            print(f"  - {issue}")
    
    # Crear vercel.json si no existe
    if not os.path.exists("vercel.json"):
        print("\nCreando vercel.json con configuración optimizada...")
        helper.create_vercel_json()
    
    print("\n✅ Verificaciones pre-despliegue completadas")