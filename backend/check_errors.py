#!/usr/bin/env python3
"""
Script para verificar y resolver problemas comunes en el código Python.
Ejecutar con: python3 backend/check_errors.py
"""

import os
import sys
import subprocess
import importlib.util
from typing import List, Dict, Any, Tuple, Optional


class PythonCodeChecker:
    """Clase para verificar y resolver problemas comunes en código Python"""
    
    def __init__(self, backend_dir: str = "./backend"):
        """Inicializa el verificador de código"""
        self.backend_dir = backend_dir
        self.errors = []
        self.warnings = []
        
    def check_missing_imports(self) -> List[Dict[str, Any]]:
        """Verifica importaciones faltantes en los archivos Python"""
        missing_imports = []
        
        # Listar todos los archivos Python
        python_files = []
        for root, _, files in os.walk(self.backend_dir):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        
        # Lista de módulos estándar de Python
        std_modules = [
            "os", "sys", "json", "time", "datetime", "re", "math", 
            "random", "subprocess", "logging", "argparse", "pathlib"
        ]
        
        # Verificar cada archivo
        for py_file in python_files:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Análisis básico para encontrar imports
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Buscar imports
                if line.strip().startswith('import ') or line.strip().startswith('from '):
                    parts = line.strip().replace('import ', ' ').replace('from ', ' ').split()
                    if parts:
                        module_name = parts[0].split('.')[0]
                        
                        # Verificar si es un módulo estándar
                        if module_name in std_modules:
                            continue
                            
                        # Verificar si es un módulo local
                        if os.path.exists(os.path.join(self.backend_dir, f"{module_name}.py")):
                            continue
                            
                        # Verificar si es un módulo instalado
                        spec = importlib.util.find_spec(module_name)
                        if spec is None:
                            missing_imports.append({
                                "file": py_file,
                                "line": i + 1,
                                "module": module_name,
                                "import_statement": line.strip()
                            })
        
        return missing_imports
    
    def check_syntax_errors(self) -> List[Dict[str, Any]]:
        """Verifica errores de sintaxis en los archivos Python"""
        syntax_errors = []
        
        # Listar todos los archivos Python
        python_files = []
        for root, _, files in os.walk(self.backend_dir):
            for file in files:
                if file.endswith(".py"):
                    python_files.append(os.path.join(root, file))
        
        # Verificar cada archivo
        for py_file in python_files:
            try:
                with open(py_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Intentar compilar el código
                compile(content, py_file, 'exec')
            except SyntaxError as e:
                syntax_errors.append({
                    "file": py_file,
                    "line": e.lineno,
                    "column": e.offset,
                    "message": str(e)
                })
        
        return syntax_errors
    
    def install_missing_packages(self, missing_imports: List[Dict[str, Any]]) -> bool:
        """Instala los paquetes faltantes"""
        if not missing_imports:
            return True
            
        print("\n🔍 Instalando paquetes faltantes...")
        
        # Recopilar nombres de módulos únicos
        modules = set()
        for item in missing_imports:
            modules.add(item["module"])
        
        # Intentar instalar cada paquete
        success = True
        for module in modules:
            print(f"📦 Instalando {module}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", module])
                print(f"✅ {module} instalado correctamente")
            except subprocess.CalledProcessError:
                print(f"❌ Error al instalar {module}")
                success = False
        
        return success
    
    def update_requirements_txt(self) -> bool:
        """Actualiza el archivo requirements.txt con las dependencias instaladas"""
        print("\n📝 Actualizando requirements.txt...")
        
        req_file = os.path.join(self.backend_dir, "requirements.txt")
        
        try:
            # Generar el archivo con pip freeze
            result = subprocess.run(
                [sys.executable, "-m", "pip", "freeze"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Leer el archivo actual si existe
            current_reqs = set()
            if os.path.exists(req_file):
                with open(req_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            current_reqs.add(line)
            
            # Agregar nuevas dependencias
            new_reqs = set()
            for line in result.stdout.splitlines():
                if line and not line.startswith('#'):
                    new_reqs.add(line)
            
            # Combinar dependencias
            all_reqs = sorted(current_reqs.union(new_reqs))
            
            # Guardar el archivo actualizado
            with open(req_file, 'w', encoding='utf-8') as f:
                f.write("# Dependencias generadas automáticamente\n")
                for req in all_reqs:
                    f.write(f"{req}\n")
            
            print(f"✅ {req_file} actualizado correctamente")
            return True
        except Exception as e:
            print(f"❌ Error al actualizar requirements.txt: {e}")
            return False
    
    def run_all_checks(self) -> Tuple[bool, List[str]]:
        """Ejecuta todas las verificaciones y devuelve el estado"""
        print("🔍 Ejecutando verificaciones de código Python...")
        
        # Verificar importaciones faltantes
        missing_imports = self.check_missing_imports()
        if missing_imports:
            print(f"\n⚠️ Se encontraron {len(missing_imports)} importaciones faltantes:")
            for item in missing_imports:
                print(f"  - {item['file']}:{item['line']}: {item['import_statement']}")
            
            # Instalar paquetes faltantes
            self.install_missing_packages(missing_imports)
        else:
            print("✅ No se encontraron importaciones faltantes")
        
        # Verificar errores de sintaxis
        syntax_errors = self.check_syntax_errors()
        if syntax_errors:
            print(f"\n❌ Se encontraron {len(syntax_errors)} errores de sintaxis:")
            for item in syntax_errors:
                print(f"  - {item['file']}:{item['line']}: {item['message']}")
        else:
            print("✅ No se encontraron errores de sintaxis")
        
        # Actualizar requirements.txt
        self.update_requirements_txt()
        
        # Generar resumen
        success = not syntax_errors
        recommendations = []
        
        if missing_imports:
            recommendations.append("- Ejecuta `pip install -r backend/requirements.txt` para instalar las dependencias")
        
        if syntax_errors:
            recommendations.append("- Corrige los errores de sintaxis en los archivos Python")
        
        return success, recommendations


if __name__ == "__main__":
    checker = PythonCodeChecker()
    success, recommendations = checker.run_all_checks()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ Verificación completada con éxito!")
    else:
        print("⚠️ Se encontraron problemas que requieren atención")
    
    if recommendations:
        print("\nRecomendaciones:")
        for rec in recommendations:
            print(rec)
    
    sys.exit(0 if success else 1)