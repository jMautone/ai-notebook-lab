"""
Servidor MCP personalizado usando FastMCP.

Este servidor expone herramientas personalizadas que pueden ser
invocadas desde un IDE o desde modelos de lenguaje.
"""

import asyncio
import os
import sys
from typing import Any

# Importar FastMCP
try:
    from fastmcp import FastMCP, Tool
except ImportError:
    print("❌ Error: FastMCP no está instalado")
    print("Instálalo con: pip install fastmcp")
    sys.exit(1)

# Importar herramientas personalizadas
# from tools.text_tools import TextTools
# from tools.system_tools import SystemTools
# from tools.file_tools import FileTools


# Crear instancia del servidor
mcp = FastMCP(
    name="Lab7-CustomMCP",
    description="Servidor MCP personalizado para el Laboratorio 7"
)


# ============================================================================
# HERRAMIENTAS DE TEXTO
# ============================================================================

@mcp.tool()
def analyze_text(text: str) -> dict[str, Any]:
    """
    Analiza un texto y devuelve estadísticas.
    
    Args:
        text: El texto a analizar
        
    Returns:
        Diccionario con estadísticas del texto
    """
    lines = text.split('\n')
    words = text.split()
    
    avg_word_length = (
        sum(len(word) for word in words) / len(words)
        if words else 0
    )
    
    return {
        "character_count": len(text),
        "word_count": len(words),
        "line_count": len(lines),
        "average_word_length": round(avg_word_length, 2)
    }


@mcp.tool()
def convert_text(text: str, format: str) -> dict[str, Any]:
    """
    Convierte texto entre diferentes formatos.
    
    Args:
        text: Texto a convertir
        format: Formato destino ('uppercase', 'lowercase', 'title', 'reverse')
        
    Returns:
        Diccionario con el texto convertido
    """
    format = format.lower()
    
    if format == "uppercase":
        converted = text.upper()
    elif format == "lowercase":
        converted = text.lower()
    elif format == "title":
        converted = text.title()
    elif format == "reverse":
        converted = text[::-1]
    else:
        raise ValueError(
            f"Formato no soportado: {format}. "
            "Use: uppercase, lowercase, title, reverse"
        )
    
    return {
        "original": text,
        "converted": converted,
        "format_used": format
    }


@mcp.tool()
def count_character(text: str, character: str) -> dict[str, Any]:
    """
    Cuenta las ocurrencias de un carácter en un texto.
    
    Args:
        text: Texto a analizar
        character: Carácter a contar
        
    Returns:
        Diccionario con el conteo
    """
    count = text.lower().count(character.lower())
    
    return {
        "text": text,
        "character": character,
        "count": count,
        "percentage": round(
            (count / len(text) * 100) if text else 0,
            2
        )
    }


# ============================================================================
# HERRAMIENTAS DEL SISTEMA
# ============================================================================

@mcp.tool()
def get_system_info() -> dict[str, Any]:
    """
    Obtiene información del sistema.
    
    Returns:
        Diccionario con información del sistema
    """
    import platform
    import psutil
    
    try:
        # Información de CPU y memoria
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


@mcp.tool()
def get_environment_info() -> dict[str, Any]:
    """
    Obtiene información sobre variables de entorno relevantes.
    
    Returns:
        Diccionario con variables de entorno
    """
    return {
        "path": os.getenv("PATH", "No disponible").split(";")[0],
        "home": os.getenv("HOME", os.getenv("USERPROFILE", "No disponible")),
        "python_executable": sys.executable,
        "working_directory": os.getcwd()
    }


# ============================================================================
# HERRAMIENTAS DE ARCHIVOS
# ============================================================================

@mcp.tool()
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


@mcp.tool()
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


# ============================================================================
# HERRAMIENTAS DE GENERACIÓN DE DATOS
# ============================================================================

@mcp.tool()
def generate_sample_data(data_type: str, count: int) -> dict[str, Any]:
    """
    Genera datos de muestra para testing.
    
    Args:
        data_type: Tipo de datos ('names', 'emails', 'urls', 'numbers')
        count: Cantidad de elementos a generar
        
    Returns:
        Diccionario con los datos generados
    """
    import random
    import string
    
    data_type = data_type.lower()
    count = max(1, min(count, 1000))  # Limitar a 1000 items
    
    if data_type == "names":
        names = ["Juan", "María", "Carlos", "Ana", "Diego", "Laura", 
                 "Pedro", "Sofia", "Miguel", "Elena"]
        items = [random.choice(names) for _ in range(count)]
    
    elif data_type == "emails":
        domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com"]
        items = [
            f"user{i}{random.choice(string.ascii_lowercase)}@{random.choice(domains)}"
            for i in range(count)
        ]
    
    elif data_type == "urls":
        protocols = ["http://", "https://"]
        domains = ["example.com", "test.com", "demo.org", "sample.net"]
        paths = ["page", "api", "data", "resource", "service"]
        items = [
            f"{random.choice(protocols)}www.{random.choice(domains)}/{random.choice(paths)}"
            for _ in range(count)
        ]
    
    elif data_type == "numbers":
        items = [random.randint(1, 1000) for _ in range(count)]
    
    else:
        return {
            "success": False,
            "error": f"Tipo de dato no soportado: {data_type}. "
                    "Use: names, emails, urls, numbers"
        }
    
    return {
        "success": True,
        "data_type": data_type,
        "items": items,
        "count": len(items)
    }


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

async def main():
    """Inicia el servidor."""
    print("=" * 60)
    print("🚀 Servidor MCP Personalizado")
    print("=" * 60)
    print()
    print("📋 Herramientas disponibles:")
    print("  • analyze_text")
    print("  • convert_text")
    print("  • count_character")
    print("  • get_system_info")
    print("  • get_environment_info")
    print("  • read_file")
    print("  • list_directory")
    print("  • generate_sample_data")
    print()
    print("🔗 Iniciando servidor...")
    print("=" * 60)
    
    # Iniciar servidor
    await mcp.run(port=8000)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Servidor detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
