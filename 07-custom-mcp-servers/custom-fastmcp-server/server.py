"""Servidor MCP personalizado usando FastMCP.

Este servidor expone herramientas personalizadas que pueden ser
invocadas desde FastMCP Cloud.
"""

import os
import sys

# Importar FastMCP
from fastmcp import FastMCP

# Crear instancia del servidor
mcp = FastMCP("Lab7 Custom MCP Server")


# ============================================================================
# HERRAMIENTAS DE TEXTO
# ============================================================================

@mcp.tool()
def analyze_text(text: str) -> str:
    """
    Analiza un texto y devuelve estadísticas.
    
    Args:
        text: El texto a analizar
        
    Returns:
        String con las estadísticas del texto
    """
    lines = text.split('\n')
    words = text.split()
    
    avg_word_length = (
        sum(len(word) for word in words) / len(words)
        if words else 0
    )
    
    return f"Caracteres: {len(text)}, Palabras: {len(words)}, Líneas: {len(lines)}, Longitud promedio: {avg_word_length:.2f}"


@mcp.tool()
def convert_text(text: str, format: str) -> str:
    """
    Convierte texto entre diferentes formatos.
    
    Args:
        text: Texto a convertir
        format: Formato destino ('uppercase', 'lowercase', 'title', 'reverse')
        
    Returns:
        Texto convertido
    """
    format = format.lower()
    
    if format == "uppercase":
        return text.upper()
    elif format == "lowercase":
        return text.lower()
    elif format == "title":
        return text.title()
    elif format == "reverse":
        return text[::-1]
    else:
        return f"Error: Formato no soportado: {format}. Use: uppercase, lowercase, title, reverse"


@mcp.tool()
def count_character(text: str, character: str) -> int:
    """
    Cuenta las ocurrencias de un carácter en un texto.
    
    Args:
        text: Texto a analizar
        character: Carácter a contar
        
    Returns:
        Número de ocurrencias del carácter
    """
    return text.lower().count(character.lower())


# ============================================================================
# HERRAMIENTAS DEL SISTEMA
# ============================================================================

@mcp.tool()
def get_system_info() -> str:
    """
    Obtiene información del sistema.
    
    Returns:
        String con información del sistema
    """
    import platform
    
    try:
        import psutil
        cpu_count = psutil.cpu_count()
        memory = psutil.virtual_memory()
        return f"SO: {platform.platform()}, Python: {platform.python_version()}, CPUs: {cpu_count}, Memoria: {round(memory.total / (1024**3), 2)}GB"
    except ImportError:
        return f"SO: {platform.platform()}, Python: {platform.python_version()}"


@mcp.tool()
def get_environment_info() -> str:
    """
    Obtiene información sobre variables de entorno relevantes.
    
    Returns:
        String con información del entorno
    """
    import platform
    return f"Home: {os.getenv('HOME', os.getenv('USERPROFILE', 'N/A'))}, Python: {sys.executable}, Dir: {os.getcwd()}"


# ============================================================================
# HERRAMIENTAS DE ARCHIVOS
# ============================================================================

@mcp.tool()
def read_file(file_path: str, lines: int = 0) -> str:
    """
    Lee el contenido de un archivo.
    
    Args:
        file_path: Ruta del archivo
        lines: Número de líneas a leer (0 = todas)
        
    Returns:
        Contenido del archivo como string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            if lines > 0:
                content = ''.join(f.readlines()[:lines])
            else:
                content = f.read()
        return content
    except FileNotFoundError:
        return f"Error: Archivo no encontrado: {file_path}"
    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
def list_directory(directory: str) -> str:
    """
    Lista los archivos en un directorio.
    
    Args:
        directory: Ruta del directorio
        
    Returns:
        String con la lista de archivos
    """
    try:
        if not os.path.isdir(directory):
            return f"Error: No es un directorio: {directory}"
        
        items = os.listdir(directory)
        files = [f for f in items if os.path.isfile(os.path.join(directory, f))]
        dirs = [d for d in items if os.path.isdir(os.path.join(directory, d))]
        
        result = f"Archivos ({len(files)}): {', '.join(files[:5])}"
        if len(files) > 5:
            result += f" ... y {len(files) - 5} más"
        result += f"\nDirectorios ({len(dirs)}): {', '.join(dirs[:5])}"
        if len(dirs) > 5:
            result += f" ... y {len(dirs) - 5} más"
        return result
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# HERRAMIENTAS DE GENERACIÓN DE DATOS
# ============================================================================

@mcp.tool()
def generate_sample_data(data_type: str, count: int) -> str:
    """
    Genera datos de muestra para testing.
    
    Args:
        data_type: Tipo de datos ('names', 'emails', 'urls', 'numbers')
        count: Cantidad de elementos a generar
        
    Returns:
        String con los datos generados
    """
    import random
    import string
    
    data_type = data_type.lower()
    count = max(1, min(count, 100))  # Limitar a 100 items
    
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
        items = [str(random.randint(1, 1000)) for _ in range(count)]
    
    else:
        return f"Error: Tipo de dato no soportado: {data_type}. Use: names, emails, urls, numbers"
    
    return ", ".join(items[:10]) + (f" ... y {len(items) - 10} más" if len(items) > 10 else "")


# ============================================================================
# PUNTO DE ENTRADA - FASTMCP CLOUD
# ============================================================================

# FastMCP Cloud ejecuta el servidor automáticamente
