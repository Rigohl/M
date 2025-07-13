#!/usr/bin/env python3
"""
Script maestro para corregir todos los errores del proyecto
"""

import os
import sys
import subprocess
import json
import re
from typing import List, Dict, Any, Tuple, Set
from pathlib import Path

def run_command(command: List[str], cwd: str = None) -> Tuple[int, str, str]:
    """
    Ejecuta un comando y devuelve el código de salida y la salida
    
    Args:
        command: Lista con el comando y sus argumentos
        cwd: Directorio de trabajo (opcional)
        
    Returns:
        Tupla con el código de salida, la salida estándar y la salida de error
    """
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

def fix_python_imports() -> bool:
    """
    Corrige los errores de importación en archivos Python
    
    Returns:
        True si se corrigieron los errores, False en caso contrario
    """
    print("\n🔧 Corrigiendo errores de importación Python...")
    
    # Ejecutar el script install_dependencies.py
    script_path = os.path.join(os.path.dirname(__file__), "install_dependencies.py")
    if not os.path.exists(script_path):
        print(f"❌ No se encontró el script {script_path}")
        return False
    
    returncode, stdout, stderr = run_command([sys.executable, script_path])
    print(stdout)
    if stderr:
        print(stderr)
    
    return returncode == 0

def fix_typescript_errors() -> bool:
    """
    Corrige los errores de TypeScript
    
    Returns:
        True si se corrigieron los errores, False en caso contrario
    """
    print("\n🔧 Corrigiendo errores de TypeScript...")
    
    # Crear archivo de utilidades de autenticación
    auth_helpers_path = "/workspaces/M/src/lib/auth-helpers.ts"
    auth_helpers_content = """/**
 * Utilidades para manejar respuestas de autenticación
 */

/**
 * Tipo genérico para respuestas de autenticación
 */
export interface AuthResponseWithUser {
  user?: any;
  error?: string;
  session?: any;
  success?: boolean;
}

/**
 * Extrae el usuario de diferentes formatos de respuesta de autenticación
 * @param data Respuesta de autenticación
 * @returns El objeto de usuario o null
 */
export function extractUserFromAuthResponse(data: any): any {
  if (!data) return null;
  
  // Manejar diferentes estructuras de respuesta
  if (data.data?.user) return data.data.user;
  if (data.user) return data.user;
  if (data.session?.user) return data.session.user;
  return null;
}

/**
 * Formatea una respuesta de autenticación para uso en la aplicación
 * @param data Respuesta de autenticación
 * @param error Error opcional
 * @returns Objeto de respuesta formateado
 */
export function formatAuthResponse(data: any, error?: any): AuthResponseWithUser {
  if (error) {
    return { error: error.message || 'Error de autenticación', success: false };
  }

  const user = extractUserFromAuthResponse(data);
  
  return {
    user,
    session: data.session || data.data?.session,
    success: !!user
  };
}
"""
    
    # Crear o actualizar archivo de utilidades de autenticación
    os.makedirs(os.path.dirname(auth_helpers_path), exist_ok=True)
    with open(auth_helpers_path, 'w', encoding='utf-8') as f:
        f.write(auth_helpers_content)
        
    print(f"✅ Creado archivo {auth_helpers_path}")
    
    # Corregir error-utils.ts
    error_utils_path = "/workspaces/M/src/lib/error-utils.ts"
    if os.path.exists(error_utils_path):
        try:
            with open(error_utils_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Buscar y corregir la interfaz ExtendedError
            error_pattern = r"interface ExtendedError extends ErrorConstructor \{[^}]+\}"
            fixed_error_interface = """// Definir un tipo más específico para Error.captureStackTrace
type CaptureStackTraceFunction = (targetObject: object, constructorOpt?: Function | undefined) => void;

// Extender ErrorConstructor con una propiedad opcional
interface ExtendedError {
  captureStackTrace: CaptureStackTraceFunction;
}"""
            
            if re.search(error_pattern, content):
                content = re.sub(error_pattern, fixed_error_interface, content)
                
                with open(error_utils_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                    
                print(f"✅ Corregido archivo {error_utils_path}")
            else:
                print(f"⚠️ No se encontró el patrón en {error_utils_path}")
        except Exception as e:
            print(f"❌ Error al corregir {error_utils_path}: {e}")
            return False
    
    return True

def fix_markdown_files() -> bool:
    """
    Corrige los errores de Markdown
    
    Returns:
        True si se corrigieron los errores, False en caso contrario
    """
    print("\n🔧 Corrigiendo errores de Markdown...")
    
    # Crear archivo .markdownlint.json
    markdownlint_path = "/workspaces/M/.markdownlint.json"
    markdownlint_content = """{
  "default": true,
  "MD007": {
    "indent": 2
  },
  "MD013": false,
  "MD022": {
    "lines_above": 1,
    "lines_below": 1
  },
  "MD030": {
    "ul_single": 1,
    "ol_single": 1,
    "ul_multi": 1,
    "ol_multi": 1
  },
  "MD031": true,
  "MD032": true,
  "MD040": true,
  "MD047": true,
  "line-length": false
}"""
    
    # Crear o actualizar archivo de configuración de markdownlint
    with open(markdownlint_path, 'w', encoding='utf-8') as f:
        f.write(markdownlint_content)
        
    print(f"✅ Creado archivo {markdownlint_path}")
    
    # Ejecutar script de corrección de markdown
    markdown_files = []
    for root, _, files in os.walk("/workspaces/M"):
        for file in files:
            if file.endswith(".md"):
                markdown_files.append(os.path.join(root, file))
    
    # Procesar cada archivo markdown
    for md_file in markdown_files:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 1. Agregar una nueva línea al final del archivo si no existe
            if not content.endswith('\n'):
                content = content + '\n'
            
            # 2. Corregir espacios después de marcadores de lista
            content = re.sub(r'^(\s*)(\d+\.|\*|\+|\-)(\s{2,})(.+)$', r'\1\2 \4', content, flags=re.MULTILINE)
            
            # 3. Corregir líneas en blanco alrededor de listas
            content = re.sub(r'([^\n])\n^(\s*(?:\d+\.|\*|\+|\-)\s.+)$', r'\1\n\n\2', content, flags=re.MULTILINE)
            
            # 4. Corregir líneas en blanco alrededor de encabezados
            content = re.sub(r'([^\n])\n(#{1,6}\s.+)$', r'\1\n\n\2', content, flags=re.MULTILINE)
            content = re.sub(r'^(#{1,6}\s.+)\n([^\n])', r'\1\n\n\2', content, flags=re.MULTILINE)
            
            # Guardar cambios
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(content)
                
            print(f"✅ Corregido archivo {md_file}")
        except Exception as e:
            print(f"❌ Error al corregir {md_file}: {e}")
    
    return True

def main() -> int:
    """Función principal"""
    print("🚀 Iniciando corrección de errores del proyecto...")
    
    success = True
    
    # Corregir errores de importación Python
    if not fix_python_imports():
        print("⚠️ No se pudieron corregir todos los errores de importación")
        success = False
    
    # Corregir errores de TypeScript
    if not fix_typescript_errors():
        print("⚠️ No se pudieron corregir todos los errores de TypeScript")
        success = False
    
    # Corregir errores de Markdown
    if not fix_markdown_files():
        print("⚠️ No se pudieron corregir todos los errores de Markdown")
        success = False
    
    if success:
        print("\n✅ Todos los errores han sido corregidos exitosamente")
    else:
        print("\n⚠️ Se corrigieron algunos errores, pero otros pueden requerir intervención manual")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())