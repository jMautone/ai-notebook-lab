"""
Servidor MCP básico - Parte 1
Expone una herramienta llamada 'say_hello' que recibe un nombre y devuelve un saludo personalizado.
"""

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Crear instancia del servidor MCP
app = Server("hello-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Lista las herramientas disponibles en este servidor MCP.
    
    Decisión: Definir la herramienta con un esquema JSON claro que especifica:
    - Nombre descriptivo de la función
    - Descripción clara de su propósito
    - Esquema de parámetros de entrada con tipos y descripciones
    """
    return [
        Tool(
            name="say_hello",
            description="Genera un saludo personalizado para una persona. Recibe un nombre y devuelve un mensaje de bienvenida.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "El nombre de la persona a saludar"
                    }
                },
                "required": ["name"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """
    Ejecuta la herramienta solicitada.
    
    Decisión: 
    - Validar que la herramienta existe antes de ejecutarla
    - Validar que los parámetros requeridos están presentes
    - Manejar errores de forma descriptiva
    - Retornar el resultado en formato TextContent según el protocolo MCP
    """
    if name != "say_hello":
        raise ValueError(f"Herramienta desconocida: {name}")
    
    # Validar que el parámetro 'name' está presente
    if "name" not in arguments:
        raise ValueError("El parámetro 'name' es requerido")
    
    person_name = arguments["name"]
    
    # Validar que el nombre no esté vacío
    if not person_name or not person_name.strip():
        raise ValueError("El nombre no puede estar vacío")
    
    # Generar el saludo personalizado
    greeting = f"¡Hola, {person_name}! Bienvenido al mundo MCP."
    
    # Retornar el resultado en el formato esperado por MCP
    return [
        TextContent(
            type="text",
            text=greeting
        )
    ]


async def main():
    """
    Función principal que inicia el servidor MCP.
    
    Decisión: Usar stdio_server para comunicación a través de entrada/salida estándar.
    Esto es el método estándar para servidores MCP locales y permite comunicación
    mediante pipes entre procesos.
    """
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    # Ejecutar el servidor
    asyncio.run(main())
