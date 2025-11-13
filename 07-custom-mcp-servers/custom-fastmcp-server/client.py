"""Cliente para probar el servidor MCP personalizado.

Este script conecta al servidor FastMCP Cloud. Usa variables de entorno para configuración segura.
"""

import asyncio
import json
import os
from typing import Any, Optional


def get_server_config() -> tuple[str, str]:
    """
    Obtiene la configuración del servidor FastMCP Cloud desde variables de entorno.
    
    Returns:
        tuple: (SERVER_URL, API_KEY)
    
    Raises:
        ValueError: Si la configuración es inválida
    """
    server_url = os.getenv("FASTMCP_SERVER_URL")
    api_key = os.getenv("FASTMCP_API_KEY")
    
    if not server_url or not api_key:
        raise ValueError(
            "❌ Variables de entorno no configuradas\n"
            "   Configúralas con:\n"
            "   $env:FASTMCP_SERVER_URL = \"https://...\"\n"
            "   $env:FASTMCP_API_KEY = \"fmcp_xxxxx\""
        )
    
    return server_url, api_key


class MCPClient:
    """Cliente para conectar con el servidor MCP FastMCP Cloud."""
    
    def __init__(
        self,
        server_url: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Inicializa el cliente.
        
        Args:
            server_url: URL del servidor (si None, usa variables de entorno)
            api_key: API Key para autenticación (si None, lo obtiene de variables de entorno)
        """
        if server_url is None:
            server_url, api_key = get_server_config()
        
        self.server_url = server_url
        self.api_key = api_key
        self.session = None
    
    async def connect(self):
        """Conecta con el servidor FastMCP Cloud."""
        try:
            import httpx
            self.session = httpx.AsyncClient()
            
            print(f"🌐 Conectado a FastMCP Cloud: {self.server_url}")
            print(f"🔐 API Key: {self.api_key[:20]}...")
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
            # FastMCP Cloud - usar protocolo JSON-RPC
            url = self.server_url
            if not url.endswith("/mcp"):
                url = f"{url}/mcp"
            
            response = await self.session.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                },
                json={
                    "jsonrpc": "2.0",
                    "id": 2,
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": kwargs
                    }
                },
                timeout=30.0
            )
            response.raise_for_status()
            
            # Parsear respuesta SSE
            content = response.text
            if 'text/event-stream' in response.headers.get('content-type', ''):
                lines = content.strip().split('\n')
                for line in lines:
                    if line.startswith('data: '):
                        data = line[6:]
                        result = json.loads(data)
                        # Extraer el contenido de texto
                        if "result" in result:
                            content_list = result["result"].get("content", [])
                            if content_list and "text" in content_list[0]:
                                return {"success": True, "text": content_list[0]["text"]}
                        return result
            else:
                return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def list_tools(self) -> list[dict]:
        """
        Lista las herramientas disponibles en el servidor.
        
        Returns:
            Lista de herramientas disponibles
        """
        if not self.session:
            raise RuntimeError("No conectado al servidor")
        
        try:
            # FastMCP Cloud
            url = self.server_url
            if not url.endswith("/mcp"):
                url = f"{url}/mcp"
            
            response = await self.session.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "Accept": "application/json, text/event-stream"
                },
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/list",
                    "params": {}
                },
                timeout=30.0
            )
            response.raise_for_status()
            
            content = response.text
            if 'text/event-stream' in response.headers.get('content-type', ''):
                lines = content.strip().split('\n')
                for line in lines:
                    if line.startswith('data: '):
                        data = line[6:]
                        return json.loads(data)
            else:
                return response.json()
        except Exception as e:
            print(f"Error al listar herramientas: {e}")
            return []


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
    # read_file retorna el contenido como string en la clave "text"
    if "error" in result:
        print(f"   Error: {result['error']}")
    elif "text" in result:
        content = result["text"][:200]
        print(f"   Contenido (primeras líneas):\n{content}...")
    else:
        print(f"   Resultado: {json.dumps(result, indent=2)}")


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
    
    try:
        # Crear cliente con configuración automática
        client = MCPClient()
        
        print(f"\n🔧 Configuración:")
        print(f"   • Servidor: {client.server_url}")
        
        # Conectar
        print()
        await client.connect()
        
        # Ejecutar pruebas
        await test_text_tools(client)
        await test_system_tools(client)
        await test_file_tools(client)
        await test_data_generation_tools(client)
        
        # Modo interactivo
        await interactive_mode(client)
        
    except ConnectionError:
        print("\n❌ No se pudo conectar al servidor FastMCP Cloud")
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
