#!/usr/bin/env python3
"""
Script para instalar dependencias Python faltantes
"""

import os
import sys
import subprocess
from typing import List, Dict, Set, Optional

def check_import(module_name: str) -> bool:
    """
    Verifica si un módulo puede ser importado
    
    Args:
        module_name: Nombre del módulo a verificar
        
    Returns:
        True si el módulo puede ser importado, False en caso contrario
    """
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False

def get_module_package_mapping() -> Dict[str, str]:
    """
    Obtiene un mapeo de nombres de módulos a nombres de paquetes
    
    Returns:
        Diccionario con nombres de módulos como claves y nombres de paquetes como valores
    """
    return {
        "openai": "openai",
        "flask": "flask",
        "fastapi": "fastapi",
        "pydantic": "pydantic",
        "supabase": "supabase",
        "pytest": "pytest",
        "testclient": "httpx",
        "uvicorn": "uvicorn",
        "databases": "databases",
        "sqlalchemy": "sqlalchemy",
        "asyncpg": "asyncpg",
        "requests": "requests",
        "dotenv": "python-dotenv",
        "jwt": "pyjwt",
        "bcrypt": "bcrypt"
    }

def find_missing_imports(directory: str) -> Set[str]:
    """
    Busca imports faltantes en un directorio
    
    Args:
        directory: Directorio a revisar
        
    Returns:
        Conjunto de nombres de módulos faltantes
    """
    missing_modules = set()
    module_mapping = get_module_package_mapping()
    
    # Recorrer todos los archivos Python en el directorio
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py"):
                continue
                
            file_path = os.path.join(root, file)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Buscar imports
                import_lines = [line.strip() for line in content.split('\n') 
                                if line.strip().startswith("import ") or line.strip().startswith("from ")]
                
                for line in import_lines:
                    words = line.split()
                    if line.startswith("import "):
                        module_name = words[1].split('.')[0]
                    else:  # from ... import
                        module_name = words[1].split('.')[0]
                    
                    if module_name in module_mapping and not check_import(module_name):
                        missing_modules.add(module_name)
                        
            except Exception as e:
                print(f"Error al analizar {file_path}: {e}")
                
    return missing_modules

def install_missing_modules(modules: Set[str]) -> bool:
    """
    Instala los módulos faltantes
    
    Args:
        modules: Conjunto de nombres de módulos a instalar
        
    Returns:
        True si todos los módulos fueron instalados correctamente, False en caso contrario
    """
    if not modules:
        return True
        
    module_mapping = get_module_package_mapping()
    success = True
    
    for module in modules:
        package = module_mapping.get(module, module)
        print(f"📦 Instalando {package}...")
        
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"✅ {package} instalado correctamente")
        except subprocess.CalledProcessError:
            print(f"❌ Error al instalar {package}")
            success = False
            
    return success

def update_requirements_file(modules: Set[str], requirements_path: str) -> None:
    """
    Actualiza el archivo requirements.txt con los módulos instalados
    
    Args:
        modules: Conjunto de nombres de módulos instalados
        requirements_path: Ruta al archivo requirements.txt
    """
    if not modules:
        return
        
    module_mapping = get_module_package_mapping()
    packages = [module_mapping.get(module, module) for module in modules]
    
    # Leer el archivo existente si existe
    existing_packages = set()
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    existing_packages.add(line.split('==')[0])
    
    # Obtener las versiones instaladas de los nuevos paquetes
    new_requirements = []
    for package in packages:
        if package in existing_packages:
            continue
            
        try:
            output = subprocess.check_output([sys.executable, "-m", "pip", "show", package], text=True)
            for line in output.split('\n'):
                if line.startswith("Name: "):
                    name = line[6:].strip()
                elif line.startswith("Version: "):
                    version = line[9:].strip()
                    new_requirements.append(f"{name}=={version}")
                    break
        except subprocess.CalledProcessError:
            pass
    
    # Actualizar el archivo
    if new_requirements:
        with open(requirements_path, 'a', encoding='utf-8') as f:
            f.write("\n# Dependencias añadidas automáticamente\n")
            for req in new_requirements:
                f.write(f"{req}\n")
        print(f"✅ Actualizado {requirements_path}")

def main() -> int:
    """Función principal"""
    print("🔍 Buscando dependencias faltantes...")
    
    backend_dir = "/workspaces/M/backend"
    if not os.path.exists(backend_dir):
        print(f"❌ Directorio no encontrado: {backend_dir}")
        return 1
    
    # Buscar imports faltantes
    missing_modules = find_missing_imports(backend_dir)
    
    if not missing_modules:
        print("✅ No se encontraron dependencias faltantes")
        return 0
    
    print(f"\n🔍 Se encontraron {len(missing_modules)} dependencias faltantes:")
    for module in missing_modules:
        print(f"  - {module}")
    
    # Instalar módulos faltantes
    success = install_missing_modules(missing_modules)
    
    if success:
        # Actualizar requirements.txt
        requirements_path = os.path.join(backend_dir, "requirements.txt")
        update_requirements_file(missing_modules, requirements_path)
        
        print("\n✅ Todas las dependencias fueron instaladas correctamente")
    else:
        print("\n⚠️ Algunas dependencias no pudieron ser instaladas")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())