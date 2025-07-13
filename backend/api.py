#!/usr/bin/env python3
"""
API de Backend para monitorear y reportar errores de dependencias
Proporciona endpoints para analizar y resolver problemas de dependencias
"""

import json
import os
import sys
import subprocess
from typing import Dict, List, Optional, Any
from pathlib import Path
import traceback
from flask import Flask, request, jsonify

# Importar módulos locales
from dependency_checker import DependencyChecker
from vercel_utils import VercelDeployHelper

app = Flask(__name__)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificación de salud del servicio"""
    return jsonify({
        "status": "healthy",
        "service": "dependency-monitor",
        "version": "1.0.0"
    })

@app.route('/api/check-dependencies', methods=['POST'])
def check_dependencies():
    """Endpoint para verificar conflictos de dependencias"""
    try:
        data = request.json
        project_dir = data.get('projectDir', '.')
        package_path = os.path.join(project_dir, 'package.json')
        
        checker = DependencyChecker(package_path=package_path)
        conflicts = checker.check_react_version_conflicts()
        
        return jsonify({
            "success": True,
            "conflicts": [
                {
                    "package": package,
                    "requiredReactVersion": version
                } for package, version in conflicts
            ],
            "hasConflicts": len(conflicts) > 0
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/fix-dependencies', methods=['POST'])
def fix_dependencies():
    """Endpoint para resolver automáticamente problemas de dependencias"""
    try:
        data = request.json
        project_dir = data.get('projectDir', '.')
        fix_type = data.get('fixType', 'auto')  # 'auto', 'npmrc', 'downgrade'
        
        # Cambiar al directorio del proyecto
        os.chdir(project_dir)
        
        actions_taken = []
        
        # Crear o actualizar .npmrc
        if fix_type in ['auto', 'npmrc']:
            npmrc_path = os.path.join(project_dir, '.npmrc')
            npmrc_content = """# Configuración para resolver conflictos de dependencias
legacy-peer-deps=true
auto-install-peers=true
strict-peer-deps=false
"""
            with open(npmrc_path, 'w') as f:
                f.write(npmrc_content)
            actions_taken.append("Created .npmrc with legacy-peer-deps=true")
        
        # Downgrade React si es necesario
        if fix_type in ['auto', 'downgrade']:
            package_path = os.path.join(project_dir, 'package.json')
            with open(package_path, 'r') as f:
                package_data = json.load(f)
            
            updated = False
            if "dependencies" in package_data:
                if "react" in package_data["dependencies"] and "19" in package_data["dependencies"]["react"]:
                    package_data["dependencies"]["react"] = "^18.2.0"
                    updated = True
                
                if "react-dom" in package_data["dependencies"] and "19" in package_data["dependencies"]["react-dom"]:
                    package_data["dependencies"]["react-dom"] = "^18.2.0"
                    updated = True
            
            if updated:
                with open(package_path, 'w') as f:
                    json.dump(package_data, f, indent=2)
                actions_taken.append("Downgraded React to version 18.2.0")
        
        return jsonify({
            "success": True,
            "actionsTaken": actions_taken
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/analyze-logs', methods=['POST'])
def analyze_logs():
    """Endpoint para analizar logs de despliegue y detectar errores"""
    try:
        data = request.json
        log_content = data.get('logContent')
        
        if not log_content:
            return jsonify({
                "success": False,
                "error": "No log content provided"
            }), 400
        
        # Guardar logs temporalmente para análisis
        temp_log_path = "temp_build_log.txt"
        with open(temp_log_path, "w") as f:
            f.write(log_content)
            
        # Analizar logs
        helper = VercelDeployHelper()
        analysis = helper.analyze_build_logs(temp_log_path)
        
        # Limpiar archivo temporal
        if os.path.exists(temp_log_path):
            os.remove(temp_log_path)
        
        return jsonify({
            "success": True,
            "analysis": analysis
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/project-structure', methods=['POST'])
def check_project_structure():
    """Endpoint para analizar la estructura del proyecto"""
    try:
        data = request.json
        project_dir = data.get('projectDir', '.')
        
        # Cambiar al directorio del proyecto
        original_dir = os.getcwd()
        os.chdir(project_dir)
        
        # Verificar estructura
        helper = VercelDeployHelper()
        issues = helper.verify_project_structure()
        
        # Volver al directorio original
        os.chdir(original_dir)
        
        return jsonify({
            "success": True,
            "issues": issues,
            "hasIssues": len(issues) > 0
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)