"""
Servidor MCP para FastMCP Cloud - Parte 2
Adaptación del servidor local para desplegar en FastMCP Cloud
"""

from fastmcp import FastMCP

# Crear instancia de FastMCP
# Esta es la instancia que FastMCP Cloud buscará automáticamente
mcp = FastMCP("Hello MCP Server")


@mcp.tool()
def say_hello(name: str) -> str:
    """
    Genera un saludo personalizado para una persona.
    
    Args:
        name: El nombre de la persona a saludar
        
    Returns:
        Un mensaje de bienvenida personalizado
    """
    # Validar que el nombre no esté vacío
    if not name or not name.strip():
        raise ValueError("El nombre no puede estar vacío")
    
    # Generar el saludo personalizado
    return f"¡Hola, {name}! Bienvenido al mundo MCP en la nube."


@mcp.resource("echo://static")
def echo_resource() -> str:
    """Recurso estático de ejemplo"""
    return "Echo!"


@mcp.resource("echo://{text}")
def echo_template(text: str) -> str:
    """Echo the input text"""
    return f"Echo: {text}"


@mcp.prompt("echo")
def echo_prompt(text: str) -> str:
    """Prompt de ejemplo"""
    return text


# 🎯 ENTRYPOINT para FastMCP Cloud
# FastMCP Cloud buscará automáticamente una variable llamada 'mcp', 'server', o 'app'
# Ya tenemos 'mcp' definida arriba, así que esto funcionará automáticamente

# Si quieres ejecutar localmente para probar:
if __name__ == "__main__":
    # Esto permite ejecutar el servidor localmente con: python server_fastmcp.py
    mcp.run()