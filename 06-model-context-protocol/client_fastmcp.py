"""
Cliente MCP para FastMCP Cloud - Parte 2
Se conecta a un servidor MCP desplegado en FastMCP Cloud con autenticación
"""

import asyncio
import os
import httpx
from typing import Optional


# 🔧 CONFIGURACIÓN - MODIFICA ESTOS VALORES
# Obtén estos valores después de desplegar en FastMCP Cloud
SERVER_URL = os.getenv("FASTMCP_SERVER_URL", "https://tu-servidor.fastmcp.com")
API_KEY = os.getenv("FASTMCP_API_KEY", "fmcp_xxxxxxxxxxxxx")


async def call_fastmcp_tool(
    server_url: str,
    api_key: str,
    tool_name: str,
    arguments: dict
) -> dict:
    """
    Llama a una herramienta MCP desplegada en FastMCP Cloud.
    
    Args:
        server_url: URL del servidor FastMCP
        api_key: API Key para autenticación
        tool_name: Nombre de la herramienta a llamar
        arguments: Argumentos para la herramienta
        
    Returns:
        Respuesta de la herramienta
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "tool": tool_name,
        "arguments": arguments
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{server_url}/tools/call",
            headers=headers,
            json=payload,
            timeout=30.0
        )
        response.raise_for_status()
        return response.json()


async def main():
    """
    Función principal del cliente FastMCP.
    """
    print("🌐 Cliente FastMCP Cloud")
    print("=" * 60)
    
    # Validar configuración
    if "tu-servidor" in SERVER_URL or "xxxxx" in API_KEY:
        print("❌ ERROR: Debes configurar SERVER_URL y API_KEY")
        print("\nPasos:")
        print("1. Despliega el servidor: fastmcp deploy server_fastmcp.py")
        print("2. Copia la URL y API Key que te dan")
        print("3. Edita este archivo (líneas 13-14) con tus valores")
        print("\nO usa variables de entorno:")
        print("  $env:FASTMCP_SERVER_URL = 'https://...'")
        print("  $env:FASTMCP_API_KEY = 'fmcp_...'")
        return
    
    print(f"🔗 Servidor: {SERVER_URL}")
    print(f"🔐 Autenticación: Bearer Token")
    
    try:
        print("\n" + "=" * 60)
        print("🔧 Probando la herramienta 'say_hello'...")
        print("=" * 60)
        
        # Nombres de prueba
        test_names = ["Nacho", "FastMCP Cloud", "Remote MCP"]
        
        for name in test_names:
            print(f"\n➡️  Llamando say_hello con nombre: '{name}'")
            
            try:
                result = await call_fastmcp_tool(
                    SERVER_URL,
                    API_KEY,
                    "say_hello",
                    {"name": name}
                )
                
                # Extraer el resultado
                if "result" in result:
                    print(f"✨ Respuesta: {result['result']}")
                elif "content" in result:
                    print(f"✨ Respuesta: {result['content']}")
                else:
                    print(f"✨ Respuesta: {result}")
                    
            except httpx.HTTPStatusError as e:
                print(f"❌ Error HTTP {e.response.status_code}: {e.response.text}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)
        print("✅ Todas las pruebas completadas")
        print("=" * 60)
        
    except httpx.ConnectError:
        print(f"\n❌ No se pudo conectar a {SERVER_URL}")
        print("Verifica que:")
        print("  1. La URL del servidor sea correcta")
        print("  2. El servidor esté desplegado y activo")
        print("  3. Tengas conexión a internet")
    except httpx.HTTPStatusError as e:
        print(f"\n❌ Error de autenticación: {e.response.status_code}")
        print("Verifica que:")
        print("  1. La API Key sea correcta")
        print("  2. El token no haya expirado")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
