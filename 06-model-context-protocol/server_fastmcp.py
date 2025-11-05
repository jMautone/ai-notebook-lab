"""
Servidor MCP para FastMCP Cloud - Parte 2
Adaptación del servidor local para desplegar en FastMCP Cloud
"""

from fastmcp import FastMCP

# Crear instancia de FastMCP
mcp = FastMCP("Hello MCP Server")


@mcp.tool()
def say_hello(name: str) -> str:
    """
    Genera un saludo personalizado para una persona.
    
    Args:
        name: El nombre de la persona a saludar
        
    Returns:
        Un mensaje de bienvenida personalizado
        
    Raises:
        ValueError: Si el nombre está vacío o solo contiene espacios
    """
    # Validar que el nombre no esté vacío
    if not name or not name.strip():
        raise ValueError("El nombre no puede estar vacío")
    
    # Generar el saludo personalizado
    return f"¡Hola, {name}! Bienvenido al mundo MCP en la nube."


# Para desarrollo local
if __name__ == "__main__":
    # Ejecutar servidor en modo desarrollo
    mcp.run()
