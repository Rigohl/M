#!/usr/bin/env python3
"""
Monitor de dependencias para integración continua
Este script monitorea y reporta problemas de dependencias en proyectos Node.js
"""

import json
import os
import sys
import subprocess
import time
import hashlib
from typing import Dict, List, Optional, Any
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("dependency_monitor.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("DependencyMonitor")


class DependencyMonitor:
    """Monitor de dependencias para proyectos Node.js"""
    
    def __init__(self, project_dir: str = '.', report_dir: str = './reports'):
        """
        Inicializa el monitor de dependencias
        
        Args:
            project_dir: Directorio del proyecto a monitorear
            report_dir: Directorio donde guardar los reportes
        """
        self.project_dir = Path(project_dir)
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)
        
        # Verificar si existe package.json
        self.package_path = self.project_dir / 'package.json'
        if not self.package_path.exists():
            logger.error(f"No se encontró package.json en {self.project_dir}")
            raise FileNotFoundError(f"No se encontró package.json en {self.project_dir}")
    
    def _load_package_json(self) -> Dict[str, Any]:
        """Carga el archivo package.json"""
        with open(self.package_path, 'r') as f:
            return json.load(f)
    
    def _get_dependency_hash(self) -> str:
        """Genera un hash de las dependencias actuales"""
        package_data = self._load_package_json()
        deps = {
            **package_data.get('dependencies', {}),
            **package_data.get('devDependencies', {})
        }
        deps_str = json.dumps(deps, sort_keys=True)
        return hashlib.md5(deps_str.encode()).hexdigest()
    
    def check_for_changes(self) -> bool:
        """
        Verifica si hay cambios en las dependencias desde el último chequeo
        
        Returns:
            True si hay cambios, False en caso contrario
        """
        hash_file = self.report_dir / 'last_dependency_hash.txt'
        current_hash = self._get_dependency_hash()
        
        if not hash_file.exists():
            # Primera vez que se ejecuta
            with open(hash_file, 'w') as f:
                f.write(current_hash)
            return True
        
        with open(hash_file, 'r') as f:
            previous_hash = f.read().strip()
        
        if current_hash != previous_hash:
            # Actualizar el hash
            with open(hash_file, 'w') as f:
                f.write(current_hash)
            return True
        
        return False
    
    def check_for_conflicts(self) -> List[Dict[str, str]]:
        """
        Verifica si hay conflictos de dependencias
        
        Returns:
            Lista de conflictos detectados
        """
        try:
            result = subprocess.run(
                ["npm", "ls", "--json", "--depth=0"],
                cwd=self.project_dir,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0 and result.stderr:
                # Hay posibles conflictos o problemas
                npm_output = json.loads(result.stdout)
                
                conflicts = []
                if "problems" in npm_output:
                    for problem in npm_output["problems"]:
                        if "peer dep missing" in problem or "requires a peer" in problem:
                            conflicts.append({"type": "peer_dependency", "message": problem})
                        elif "invalid" in problem:
                            conflicts.append({"type": "invalid_dependency", "message": problem})
                        else:
                            conflicts.append({"type": "other", "message": problem})
                            
                # Verificar errores específicos
                for line in result.stderr.split('\n'):
                    if "ERESOLVE" in line and "could not resolve" in line:
                        conflicts.append({
                            "type": "dependency_resolution",
                            "message": line
                        })
                
                return conflicts
            
            return []
        except Exception as e:
            logger.error(f"Error al verificar conflictos: {e}")
            return [{"type": "error", "message": str(e)}]
    
    def generate_report(self) -> Dict[str, Any]:
        """
        Genera un reporte completo de dependencias
        
        Returns:
            Diccionario con información del reporte
        """
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        report_data = {
            "timestamp": timestamp,
            "projectName": self._load_package_json().get("name", "unknown"),
            "conflicts": self.check_for_conflicts(),
            "recommendations": []
        }
        
        # Generar recomendaciones
        if report_data["conflicts"]:
            report_data["recommendations"].append({
                "type": "npmrc",
                "message": "Agregar .npmrc con legacy-peer-deps=true"
            })
            
            # Detectar problemas específicos de versión
            for conflict in report_data["conflicts"]:
                if "react@19" in conflict.get("message", "") and "requires a peer of react@^18" in conflict.get("message", ""):
                    report_data["recommendations"].append({
                        "type": "downgrade",
                        "message": "Downgrade React a la versión 18 para mayor compatibilidad"
                    })
                    break
        
        # Guardar reporte
        report_file = self.report_dir / f"dependency_report_{timestamp}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        logger.info(f"Reporte guardado en {report_file}")
        return report_data
    
    def apply_recommendations(self, report: Dict[str, Any]) -> List[str]:
        """
        Aplica las recomendaciones de un reporte
        
        Args:
            report: Reporte generado por generate_report()
            
        Returns:
            Lista de acciones aplicadas
        """
        actions = []
        
        for rec in report.get("recommendations", []):
            if rec["type"] == "npmrc":
                # Crear .npmrc
                npmrc_path = self.project_dir / ".npmrc"
                npmrc_content = """# Configuración para resolver conflictos de dependencias
legacy-peer-deps=true
auto-install-peers=true
strict-peer-deps=false
"""
                with open(npmrc_path, 'w') as f:
                    f.write(npmrc_content)
                actions.append("Created .npmrc with legacy-peer-deps=true")
            
            elif rec["type"] == "downgrade":
                # Downgrade React
                package_data = self._load_package_json()
                updated = False
                
                if "dependencies" in package_data:
                    if "react" in package_data["dependencies"] and "19" in package_data["dependencies"]["react"]:
                        package_data["dependencies"]["react"] = "^18.2.0"
                        updated = True
                    
                    if "react-dom" in package_data["dependencies"] and "19" in package_data["dependencies"]["react-dom"]:
                        package_data["dependencies"]["react-dom"] = "^18.2.0"
                        updated = True
                
                if updated:
                    with open(self.package_path, 'w') as f:
                        json.dump(package_data, f, indent=2)
                    actions.append("Downgraded React to version 18.2.0")
        
        return actions


def main() -> None:
    """Función principal del monitor de dependencias"""
    try:
        logger.info("Iniciando monitor de dependencias...")
        
        monitor = DependencyMonitor()
        
        if monitor.check_for_changes():
            logger.info("Cambios detectados en dependencias, generando reporte...")
            report = monitor.generate_report()
            
            if report["conflicts"]:
                logger.warning(f"Se encontraron {len(report['conflicts'])} conflictos")
                
                # Preguntar si desea aplicar recomendaciones automáticas
                if "--auto-fix" in sys.argv:
                    actions = monitor.apply_recommendations(report)
                    logger.info(f"Se aplicaron {len(actions)} recomendaciones automáticamente")
                    for action in actions:
                        logger.info(f"  - {action}")
            else:
                logger.info("No se encontraron conflictos")
        else:
            logger.info("No hay cambios en dependencias desde la última verificación")
    
    except Exception as e:
        logger.error(f"Error en el monitor: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()