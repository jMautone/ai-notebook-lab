"""
Cliente para probar el servidor MCP personalizado.

Este script conecta al servidor FastMCP y prueba todas las herramientas
disponibles.
"""

import asyncio
import json
from typing import Any

# Para usar este script, necesitas instalar:
# pip install httpx


class MCPClient:
    """Cliente para conectar con el servidor MCP."""
    
    def __init__(self, server_url: str = "http://localhost:8000"):
        """
        Inicializa el cliente.
        
        Args:
            server_url: URL del servidor MCP
        """
        self.server_url = server_url
        self.session = None
    
    async def connect(self):
        """Conecta con el servidor."""
        try:
            import httpx
            self.session = httpx.AsyncClient()
            print(f"✅ Conectado a {self.server_url}")
        except ImportError:
            print("❌ httpx no está instalado")
            print("Instálalo con: pip install httpx")
            raise
    
    async def disconnect(self):
        """Desconecta del servidor."""
        if self.session:
            await self.session.aclose()
            print("✅ Desconectado")
    
    async def call_tool(self, tool_name: str, **kwargs) -> dict[str, Any]:
        """
        Llama a una herramienta del servidor.
        
        Args:
            tool_name: Nombre de la herramienta
            **kwargs: Parámetros de la herramienta
            
        Returns:
            Resultado de la herramienta
        """
        if not self.session:
            raise RuntimeError("No conectado al servidor")
        
        try:
            response = await self.session.post(
                f"{self.server_url}/tools/{tool_name}",
                json=kwargs
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


async def test_text_tools(client: MCPClient):
    """Prueba las herramientas de texto."""
    print("\n" + "=" * 60)
    print("🔤 Pruebas de herramientas de TEXTO")
    print("=" * 60)
    
    # Test 1: Analizar texto
    print("\n📊 Prueba 1: analyze_text")
    result = await client.call_tool(
        "analyze_text",
        text="Este es un texto de prueba para el servidor MCP"
    )
    print(f"   Resultado: {json.dumps(result, indent=2)}")
    
    # Test 2: Convertir texto
    print("\n🔄 Prueba 2: convert_text")
    result = await client.call_tool(
        "convert_text",
        text="Hola Mundo",
        format="uppercase"
    )
    print(f"   Resultado: {json.dumps(result, indent=2)}")
    
    # Test 3: Contar caracteres
    print("\n🔢 Prueba 3: count_character")
    result = await client.call_tool(
        "count_character",
        text="Terrarium",
        character="r"
    )
    print(f"   Resultado: {json.dumps(result, indent=2)}")


async def test_system_tools(client: MCPClient):
    """Prueba las herramientas del sistema."""
    print("\n" + "=" * 60)
    print("⚙️ Pruebas de herramientas del SISTEMA")
    print("=" * 60)
    
    # Test 1: Información del sistema
    print("\n💻 Prueba 1: get_system_info")
    result = await client.call_tool("get_system_info")
    print(f"   Resultado: {json.dumps(result, indent=2)}")
    
    # Test 2: Información del entorno
    print("\n🌍 Prueba 2: get_environment_info")
    result = await client.call_tool("get_environment_info")
    print(f"   Resultado: {json.dumps(result, indent=2)}")


async def test_file_tools(client: MCPClient):
    """Prueba las herramientas de archivos."""
    print("\n" + "=" * 60)
    print("📁 Pruebas de herramientas de ARCHIVOS")
    print("=" * 60)
    
    # Test 1: Listar directorio
    print("\n📂 Prueba 1: list_directory")
    result = await client.call_tool(
        "list_directory",
        directory="."
    )
    print(f"   Resultado: {json.dumps(result, indent=2)}")
    
    # Test 2: Leer archivo
    print("\n📖 Prueba 2: read_file (README.md)")
    result = await client.call_tool(
        "read_file",
        file_path="README.md",
        lines=5
    )
    if result.get("success"):
        print(f"   Contenido (primeras líneas):\n{result['content'][:200]}...")
    else:
        print(f"   Error: {result.get('error')}")


async def test_data_generation_tools(client: MCPClient):
    """Prueba las herramientas de generación de datos."""
    print("\n" + "=" * 60)
    print("🎲 Pruebas de herramientas de GENERACIÓN DE DATOS")
    print("=" * 60)
    
    # Test 1: Generar emails
    print("\n📧 Prueba 1: generate_sample_data (emails)")
    result = await client.call_tool(
        "generate_sample_data",
        data_type="emails",
        count=3
    )
    print(f"   Resultado: {json.dumps(result, indent=2)}")
    
    # Test 2: Generar números
    print("\n🔢 Prueba 2: generate_sample_data (numbers)")
    result = await client.call_tool(
        "generate_sample_data",
        data_type="numbers",
        count=5
    )
    print(f"   Resultado: {json.dumps(result, indent=2)}")


async def interactive_mode(client: MCPClient):
    """Modo interactivo para probar herramientas."""
    print("\n" + "=" * 60)
    print("🎮 Modo Interactivo")
    print("=" * 60)
    
    while True:
        print("\nOpciones:")
        print("  1. Contar caracteres 'r' en un texto")
        print("  2. Convertir texto a mayúsculas")
        print("  3. Analizar un texto")
        print("  4. Generar datos de muestra")
        print("  5. Listar un directorio")
        print("  0. Salir")
        
        choice = input("\nSelecciona una opción: ").strip()
        
        if choice == "0":
            break
        elif choice == "1":
            text = input("Ingresa un texto: ")
            result = await client.call_tool("count_character", text=text, character="r")
            print(f"Resultado: {result}")
        elif choice == "2":
            text = input("Ingresa un texto: ")
            result = await client.call_tool("convert_text", text=text, format="uppercase")
            print(f"Resultado: {result}")
        elif choice == "3":
            text = input("Ingresa un texto: ")
            result = await client.call_tool("analyze_text", text=text)
            print(f"Resultado: {result}")
        elif choice == "4":
            data_type = input("Tipo (names/emails/urls/numbers): ")
            count = int(input("Cantidad: "))
            result = await client.call_tool("generate_sample_data", data_type=data_type, count=count)
            print(f"Resultado: {result}")
        elif choice == "5":
            directory = input("Directorio: ")
            result = await client.call_tool("list_directory", directory=directory)
            print(f"Resultado: {result}")


async def main():
    """Función principal."""
    print("=" * 60)
    print("🧪 Cliente de Prueba - Servidor MCP Personalizado")
    print("=" * 60)
    
    client = MCPClient()
    
    try:
        # Conectar
        await client.connect()
        
        # Ejecutar pruebas
        await test_text_tools(client)
        await test_system_tools(client)
        await test_file_tools(client)
        await test_data_generation_tools(client)
        
        # Modo interactivo
        await interactive_mode(client)
        
    except ConnectionError:
        print("\n❌ No se pudo conectar al servidor")
        print("Asegúrate de que el servidor está ejecutándose en http://localhost:8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
