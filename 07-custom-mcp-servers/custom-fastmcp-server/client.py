"""
Cliente para probar el servidor MCP personalizado.

Este script conecta al servidor FastMCP Cloud o local y prueba todas las herramientas
disponibles. Usa variables de entorno para configuración segura.
"""

import asyncio
import json
import os
from typing import Any, Optional

# Para usar este script, necesitas instalar:
# pip install httpx


def get_server_config() -> tuple[str, Optional[str]]:
    """
    Obtiene la configuración del servidor desde variables de entorno.
    
    Soporta dos modos:
    1. LOCAL: http://localhost:8000 (sin autenticación)
    2. FASTMCP CLOUD: URL de FastMCP Cloud con API Key
    
    Returns:
        tuple: (SERVER_URL, API_KEY o None)
    
    Raises:
        ValueError: Si la configuración es inválida
    """
    # Intentar obtener configuración de FastMCP Cloud
    server_url = os.getenv("FASTMCP_SERVER_URL")
    api_key = os.getenv("FASTMCP_API_KEY")
    
    if server_url:
        # Modo FastMCP Cloud
        if not api_key:
            raise ValueError(
                "❌ FASTMCP_SERVER_URL configurada pero falta FASTMCP_API_KEY\n"
                "   Configúrala con: $env:FASTMCP_API_KEY = \"fmcp_xxxxx\""
            )
        return server_url, api_key
    
    # Modo local (default)
    local_url = "http://localhost:8000"
    return local_url, None


class MCPClient:
    """Cliente para conectar con el servidor MCP (local o FastMCP Cloud)."""
    
    def __init__(
        self,
        server_url: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Inicializa el cliente.
        
        Args:
            server_url: URL del servidor (si None, usa variables de entorno)
            api_key: API Key para autenticación (si None, modo local)
        """
        if server_url is None:
            server_url, api_key = get_server_config()
        
        self.server_url = server_url
        self.api_key = api_key
        self.session = None
        self.is_cloud = api_key is not None
    
    async def connect(self):
        """Conecta con el servidor."""
        try:
            import httpx
            self.session = httpx.AsyncClient()
            
            if self.is_cloud:
                print(f"🌐 Conectado a FastMCP Cloud: {self.server_url}")
                print(f"🔐 API Key: {self.api_key[:20]}...")
            else:
                print(f"✅ Conectado a servidor local: {self.server_url}")
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
            if self.is_cloud:
                # Modo FastMCP Cloud - usar protocolo JSON-RPC
                response = await self.session.post(
                    f"{self.server_url}/mcp",
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
            else:
                # Modo local - protocolo simple HTTP
                response = await self.session.post(
                    f"{self.server_url}/tools/{tool_name}",
                    json=kwargs
                )
                response.raise_for_status()
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
            if self.is_cloud:
                # FastMCP Cloud
                response = await self.session.post(
                    f"{self.server_url}/mcp",
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
            else:
                # Local - devolver herramientas conocidas
                return {
                    "tools": [
                        {"name": "analyze_text", "description": "Analiza estadísticas de un texto"},
                        {"name": "convert_text", "description": "Convierte texto entre formatos"},
                        {"name": "count_character", "description": "Cuenta ocurrencias de un carácter"},
                        {"name": "get_system_info", "description": "Información del sistema"},
                        {"name": "get_environment_info", "description": "Variables de entorno"},
                        {"name": "read_file", "description": "Lee archivos"},
                        {"name": "list_directory", "description": "Lista directorios"},
                        {"name": "generate_sample_data", "description": "Genera datos de muestra"}
                    ]
                }
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
    
    try:
        # Crear cliente con configuración automática
        client = MCPClient()
        
        print(f"\n🔧 Configuración:")
        print(f"   • Servidor: {client.server_url}")
        print(f"   • Modo: {'FastMCP Cloud' if client.is_cloud else 'Local'}")
        
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
