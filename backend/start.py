#!/usr/bin/env python3
"""
Script de inicio rápido para el backend de gestión de dependencias
"""

import argparse
import os
import sys
import subprocess
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger("DependencyManager")


def install_dependencies():
    """Instalar dependencias de Python"""
    try:
        requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", requirements_path],
            check=True,
        )
        logger.info("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error al instalar dependencias: {e}")
        return False


def run_pre_build():
    """Ejecutar verificaciones pre-build"""
    try:
        pre_build_path = os.path.join(os.path.dirname(__file__), "pre_build.py")
        subprocess.run([sys.executable, pre_build_path], check=True)
        logger.info("✅ Pre-build ejecutado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error en pre-build: {e}")
        return False


def run_monitor(auto_fix=False):
    """Ejecutar monitor de dependencias"""
    try:
        monitor_path = os.path.join(os.path.dirname(__file__), "dependency_monitor.py")
        cmd = [sys.executable, monitor_path]
        if auto_fix:
            cmd.append("--auto-fix")
        subprocess.run(cmd, check=True)
        logger.info("✅ Monitor ejecutado correctamente")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error al ejecutar monitor: {e}")
        return False


def run_api_server(port=5000):
    """Iniciar servidor API"""
    try:
        api_path = os.path.join(os.path.dirname(__file__), "api.py")
        # Configurar variable de entorno para el puerto
        env = os.environ.copy()
        env["PORT"] = str(port)
        logger.info(f"🚀 Iniciando API en puerto {port}...")
        subprocess.run([sys.executable, api_path], env=env)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Error al iniciar API: {e}")
        return False
    except KeyboardInterrupt:
        logger.info("API detenida por el usuario")
        return True


def main():
    """Función principal del gestor de dependencias"""
    parser = argparse.ArgumentParser(
        description="Gestor de dependencias para proyectos Node.js"
    )
    parser.add_argument(
        "action",
        choices=["pre-build", "monitor", "api", "all"],
        help="Acción a realizar",
    )
    parser.add_argument(
        "--auto-fix", action="store_true", help="Aplicar correcciones automáticamente"
    )
    parser.add_argument(
        "--port", type=int, default=5000, help="Puerto para servidor API"
    )

    args = parser.parse_args()

    # Verificar si estamos en el directorio correcto
    if not os.path.exists("dependency_checker.py"):
        logger.warning(
            "⚠️ No se encontró dependency_checker.py en el directorio actual."
        )
        logger.warning("Por favor, ejecute este script desde el directorio 'backend'.")
        if not os.path.exists(
            os.path.join(os.path.dirname(__file__), "dependency_checker.py")
        ):
            logger.error("❌ No se encontraron los archivos necesarios.")
            return False

    # Instalar dependencias primero
    if not install_dependencies():
        return False

    if args.action == "pre-build":
        return run_pre_build()
    elif args.action == "monitor":
        return run_monitor(args.auto_fix)
    elif args.action == "api":
        return run_api_server(args.port)
    elif args.action == "all":
        if not run_pre_build():
            return False
        if not run_monitor(args.auto_fix):
            return False
        return run_api_server(args.port)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
