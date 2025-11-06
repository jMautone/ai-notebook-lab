"""
Cliente FastMCP Cloud - Usando SDK de FastMCP
Conecta directamente usando el protocolo de FastMCP Cloud
"""

import asyncio
import httpx
import json
import os
from typing import Optional


# 🔧 CONFIGURACIÓN
# Las credenciales se leen desde variables de entorno por seguridad
# Configura las variables antes de ejecutar:
#   $env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.app"
#   $env:FASTMCP_API_KEY = "fmcp_xxxxxxxxxxxxx"

def get_config() -> tuple[str, str]:
    """
    Obtiene la configuración desde variables de entorno.
    
    Returns:
        tuple: (SERVER_URL, API_KEY)
    
    Raises:
        ValueError: Si faltan variables de entorno requeridas
    """
    server_url = os.getenv("FASTMCP_SERVER_URL")
    api_key = os.getenv("FASTMCP_API_KEY")
    
    if not server_url:
        raise ValueError(
            "❌ Variable de entorno FASTMCP_SERVER_URL no configurada.\n"
            "   Configúrala con: $env:FASTMCP_SERVER_URL = \"https://tu-servidor.fastmcp.app\""
        )
    
    if not api_key:
        raise ValueError(
            "❌ Variable de entorno FASTMCP_API_KEY no configurada.\n"
            "   Configúrala con: $env:FASTMCP_API_KEY = \"fmcp_xxxxxxxxxxxxx\""
        )
    
    return server_url, api_key


# Obtener configuración al inicio
try:
    SERVER_URL, API_KEY = get_config()
except ValueError as e:
    print(str(e))
    print("\n💡 Ejemplo de configuración en PowerShell:")
    print('   $env:FASTMCP_SERVER_URL = "https://fun-peach-cattle.fastmcp.app"')
    print('   $env:FASTMCP_API_KEY = "fmcp_XdpnB18jCRHFN02IJI99yDrUbdxxUBhq-IR4BAjN4ZI"')
    print("\nLuego ejecuta nuevamente: python client_fastmcp.py")
    exit(1)


async def list_tools():
    """Lista las herramientas disponibles en el servidor FastMCP"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SERVER_URL}/mcp",
            headers={
                "Authorization": f"Bearer {API_KEY}",
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
        
        # FastMCP puede devolver SSE, intentamos parsear la respuesta
        content = response.text
        print(f"[DEBUG] Response content-type: {response.headers.get('content-type')}")
        print(f"[DEBUG] Response text: {content[:200]}...")
        
        # Si es SSE, extraer los mensajes
        if 'text/event-stream' in response.headers.get('content-type', ''):
            # Parsear eventos SSE
            lines = content.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    data = line[6:]  # Remover 'data: '
                    return json.loads(data)
        else:
            return response.json()


async def call_tool(tool_name: str, arguments: dict):
    """Llama a una herramienta MCP en FastMCP Cloud"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{SERVER_URL}/mcp",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": 2,
                "method": "tools/call",
                "params": {
                    "name": tool_name,
                    "arguments": arguments
                }
            },
            timeout=30.0
        )
        response.raise_for_status()
        
        # FastMCP devuelve SSE, parsear la respuesta
        content = response.text
        if 'text/event-stream' in response.headers.get('content-type', ''):
            # Parsear eventos SSE
            lines = content.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    data = line[6:]  # Remover 'data: '
                    return json.loads(data)
        else:
            return response.json()


async def main():
    print("🌐 Cliente FastMCP Cloud (JSON-RPC)")
    print("=" * 60)
    print(f"🔗 Servidor: {SERVER_URL}")
    print(f"🔐 API Key: {API_KEY[:15]}...")
    print(f"🔌 Protocolo: JSON-RPC 2.0 over HTTP")
    
    try:
        # Listar herramientas
        print("\n📋 Listando herramientas disponibles...")
        tools_response = await list_tools()
        
        if "result" in tools_response:
            tools = tools_response["result"].get("tools", [])
            print(f"\nHerramientas encontradas: {len(tools)}")
            for tool in tools:
                print(f"  - {tool['name']}: {tool.get('description', 'Sin descripción')}")
        else:
            print(f"Respuesta del servidor: {json.dumps(tools_response, indent=2)}")
        
        # Probar say_hello
        print("\n" + "=" * 60)
        print("🔧 Probando la herramienta 'say_hello'...")
        print("=" * 60)
        
        test_names = ["Nacho", "FastMCP Cloud", "Remote MCP"]
        
        for name in test_names:
            print(f"\n➡️  Llamando say_hello con nombre: '{name}'")
            
            try:
                result = await call_tool("say_hello", {"name": name})
                
                if "result" in result:
                    content = result["result"].get("content", [])
                    for item in content:
                        if "text" in item:
                            print(f"✨ Respuesta: {item['text']}")
                elif "error" in result:
                    print(f"❌ Error del servidor: {result['error']['message']}")
                else:
                    print(f"📦 Respuesta completa: {json.dumps(result, indent=2)}")
                    
            except httpx.HTTPStatusError as e:
                print(f"❌ Error HTTP {e.response.status_code}")
                print(f"   Detalles: {e.response.text}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)
        print("✅ Todas las pruebas completadas")
        print("=" * 60)
        
    except httpx.HTTPStatusError as e:
        print(f"\n❌ Error HTTP {e.response.status_code}")
        print(f"URL: {e.request.url}")
        print(f"Respuesta: {e.response.text}")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
