#!/usr/bin/env python3
"""
Verificador de dependencias para proyectos Node.js
Este script analiza package.json y verifica conflictos de dependencias
"""

import json
import subprocess
import os
import sys
from typing import Dict, List, Optional, Tuple, Any


class DependencyChecker:
    """Clase para verificar y resolver dependencias en proyectos Node.js"""
    
    def __init__(self, package_path: str = "./package.json"):
        """
        Inicializa el verificador de dependencias
        
        Args:
            package_path: Ruta al archivo package.json
        """
        self.package_path = package_path
        self.package_data = self._load_package_json()
        
    def _load_package_json(self) -> Dict[str, Any]:
        """Carga el archivo package.json"""
        try:
            with open(self.package_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {self.package_path}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: El archivo {self.package_path} no es un JSON válido")
            sys.exit(1)
    
    def check_react_version_conflicts(self) -> List[Tuple[str, str]]:
        """
        Verifica conflictos con versiones de React
        
        Returns:
            Lista de dependencias con conflictos y sus versiones requeridas
        """
        conflicts = []
        dependencies = {**self.package_data.get("dependencies", {}), 
                       **self.package_data.get("devDependencies", {})}
        
        # Obtener versión de React
        react_version = dependencies.get("react", "")
        if not react_version:
            return conflicts
            
        # Ejecutar npm info para obtener dependencias de pares
        for package, version in dependencies.items():
            if package == "react" or package == "react-dom":
                continue
                
            try:
                result = subprocess.run(
                    ["npm", "info", f"{package}@{version}", "peerDependencies", "--json"],
                    capture_output=True, text=True, check=False
                )
                
                if result.returncode == 0 and result.stdout.strip():
                    peer_deps = json.loads(result.stdout)
                    if peer_deps and "react" in peer_deps:
                        required_react = peer_deps["react"]
                        # Verificar si la versión actual de React cumple con los requisitos
                        if "^19" in react_version and ("^16" in required_react or "^17" in required_react or "^18" in required_react):
                            conflicts.append((package, required_react))
            except Exception as e:
                print(f"Error al verificar dependencia {package}: {e}")
                
        return conflicts
    
    def generate_npmrc(self) -> None:
        """Genera un archivo .npmrc para resolver conflictos de dependencias"""
        npmrc_content = """# Configuración para resolver conflictos de dependencias
legacy-peer-deps=true
auto-install-peers=true
strict-peer-deps=false
"""
        try:
            with open(".npmrc", "w") as f:
                f.write(npmrc_content)
            print("✅ Archivo .npmrc creado con éxito")
        except Exception as e:
            print(f"❌ Error al crear .npmrc: {e}")
    
    def downgrade_react(self) -> None:
        """Downgrade React a la versión 18 para compatibilidad"""
        if "dependencies" in self.package_data and "react" in self.package_data["dependencies"]:
            self.package_data["dependencies"]["react"] = "^18.2.0"
            
        if "dependencies" in self.package_data and "react-dom" in self.package_data["dependencies"]:
            self.package_data["dependencies"]["react-dom"] = "^18.2.0"
            
        try:
            with open(self.package_path, "w") as f:
                json.dump(self.package_data, f, indent=2)
            print("✅ React downgraded a versión 18.2.0")
        except Exception as e:
            print(f"❌ Error al actualizar package.json: {e}")
    
    def fix_dependencies(self) -> None:
        """Identifica y corrige problemas de dependencias"""
        conflicts = self.check_react_version_conflicts()
        
        if conflicts:
            print(f"⚠️ Se encontraron {len(conflicts)} conflictos de dependencias:")
            for package, react_version in conflicts:
                print(f"  - {package} requiere React {react_version}")
            
            print("\nRecomendaciones para solucionar:")
            print("1. Generar archivo .npmrc para usar legacy-peer-deps")
            print("2. Downgrade React a versión 18")
            print("3. Actualizar las dependencias que causan conflictos")
            
            choice = input("\n¿Desea aplicar soluciones automáticas? (y/n): ")
            if choice.lower() == 'y':
                self.generate_npmrc()
                self.downgrade_react()
        else:
            print("✅ No se encontraron conflictos de versiones con React")


if __name__ == "__main__":
    print("🔍 Verificando dependencias del proyecto...")
    checker = DependencyChecker()
    checker.fix_dependencies()