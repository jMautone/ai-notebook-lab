"""
Herramientas para manipulación de archivos.
"""

import os
from typing import Any


class FileTools:
    """Herramientas para operaciones con archivos."""
    
    @staticmethod
    def read_file(file_path: str, lines: int = 0) -> dict[str, Any]:
        """
        Lee el contenido de un archivo.
        
        Args:
            file_path: Ruta del archivo
            lines: Número de líneas a leer (0 = todas)
            
        Returns:
            Diccionario con el contenido del archivo
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                if lines > 0:
                    content = ''.join(f.readlines()[:lines])
                else:
                    content = f.read()
            
            file_lines = len(content.split('\n'))
            
            return {
                "success": True,
                "file_path": file_path,
                "content": content,
                "line_count": file_lines,
                "encoding": "utf-8"
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": f"Archivo no encontrado: {file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def list_directory(directory: str) -> dict[str, Any]:
        """
        Lista los archivos en un directorio.
        
        Args:
            directory: Ruta del directorio
            
        Returns:
            Diccionario con la lista de archivos
        """
        try:
            if not os.path.isdir(directory):
                return {
                    "success": False,
                    "error": f"No es un directorio: {directory}"
                }
            
            items = os.listdir(directory)
            files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
            dirs = [d for d in items if os.path.isdir(os.path.join(directory, d))]
            
            return {
                "success": True,
                "directory": directory,
                "files": files,
                "directories": dirs,
                "total_items": len(items)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def get_file_info(file_path: str) -> dict[str, Any]:
        """
        Obtiene información sobre un archivo.
        
        Args:
            file_path: Ruta del archivo
            
        Returns:
            Diccionario con información del archivo
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "error": f"Archivo no existe: {file_path}"
                }
            
            stat_info = os.stat(file_path)
            
            return {
                "success": True,
                "file_path": file_path,
                "size_bytes": stat_info.st_size,
                "size_kb": round(stat_info.st_size / 1024, 2),
                "is_file": os.path.isfile(file_path),
                "is_dir": os.path.isdir(file_path),
                "modified_timestamp": stat_info.st_mtime,
                "created_timestamp": stat_info.st_ctime
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
