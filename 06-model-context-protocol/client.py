"""
Cliente MCP básico - Parte 1
Se conecta al servidor MCP local y llama a la herramienta 'say_hello'.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    """
    Función principal del cliente MCP.
    
    Decisión de arquitectura:
    1. Usar StdioServerParameters para conectar con un servidor local
    2. Especificar el comando Python y la ruta al servidor
    3. Usar ClientSession para gestionar la comunicación
    4. Seguir el patrón async/await para operaciones no bloqueantes
    """
    
    # Configurar los parámetros del servidor
    # Decisión: Usar 'python' como comando base (funciona en la mayoría de entornos)
    # Si falla, se puede cambiar a 'python3' o 'py' según el sistema
    server_params = StdioServerParameters(
        command="python",
        args=["server.py"],
        env=None
    )
    
    print("🚀 Iniciando cliente MCP...")
    print("=" * 60)
    
    # Conectar con el servidor usando stdio_client
    # Decisión: Usar context manager para asegurar limpieza de recursos
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # Inicializar la sesión
            # Decisión: Inicializar con información básica del cliente
            await session.initialize()
            print("✅ Conexión establecida con el servidor MCP")
            
            # Listar las herramientas disponibles
            # Decisión: Primero verificar qué herramientas ofrece el servidor
            # Esto es buena práctica antes de llamar a una herramienta
            print("\n📋 Listando herramientas disponibles...")
            tools = await session.list_tools()
            
            print(f"\nHerramientas encontradas: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            
            # Llamar a la herramienta say_hello
            # Decisión: Probar con diferentes nombres para validar funcionalidad
            print("\n" + "=" * 60)
            print("🔧 Probando la herramienta 'say_hello'...")
            print("=" * 60)
            
            # 🔧 PERSONALIZA AQUÍ: Modifica esta lista con los nombres que quieras probar
            test_names = ["Juan", "María", "ChatGPT"]
            
            for name in test_names:
                print(f"\n➡️  Llamando say_hello con nombre: '{name}'")
                
                # Decisión: Estructurar los argumentos según el esquema definido
                result = await session.call_tool(
                    "say_hello",
                    arguments={"name": name}
                )
                
                # Extraer y mostrar el resultado
                # Decisión: Iterar sobre todos los contenidos de la respuesta
                # (aunque esperamos solo uno en este caso)
                for content in result.content:
                    if hasattr(content, 'text'):
                        print(f"✨ Respuesta: {content.text}")
            
            print("\n" + "=" * 60)
            print("✅ Todas las pruebas completadas exitosamente")
            print("=" * 60)


if __name__ == "__main__":
    try:
        # Ejecutar el cliente
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Cliente interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
