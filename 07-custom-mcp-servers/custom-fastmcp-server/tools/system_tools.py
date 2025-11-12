"""
Herramientas de información del sistema.
"""

import os
import sys
import platform
from typing import Any


class SystemTools:
    """Herramientas para obtener información del sistema."""
    
    @staticmethod
    def get_system_info() -> dict[str, Any]:
        """
        Obtiene información del sistema.
        
        Returns:
            Diccionario con información del sistema
        """
        try:
            import psutil
            
            cpu_count = psutil.cpu_count()
            memory = psutil.virtual_memory()
            
            return {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "cpu_count": cpu_count,
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "percent_used": memory.percent
                }
            }
        except ImportError:
            return {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "note": "Instala psutil para información completa: pip install psutil"
            }
    
    @staticmethod
    def get_environment_info() -> dict[str, Any]:
        """
        Obtiene información sobre variables de entorno relevantes.
        
        Returns:
            Diccionario con variables de entorno
        """
        return {
            "home": os.getenv("HOME", os.getenv("USERPROFILE", "No disponible")),
            "python_executable": sys.executable,
            "working_directory": os.getcwd(),
            "platform": sys.platform,
            "python_version": sys.version.split()[0]
        }
    
    @staticmethod
    def get_python_info() -> dict[str, Any]:
        """
        Obtiene información detallada sobre Python.
        
        Returns:
            Diccionario con información de Python
        """
        return {
            "version": platform.python_version(),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
            "prefix": sys.prefix,
            "version_info": {
                "major": sys.version_info.major,
                "minor": sys.version_info.minor,
                "micro": sys.version_info.micro
            }
        }
