"""
Cliente MCP - Gestión de ideas de proyectos
-------------------------------------------
Este cliente:
1. Se conecta a un MCP Server desplegado en FastMCP Cloud.
2. Usa tools para agregar y listar ideas.
3. Usa resources (guías, ejemplos).
4. Usa prompts para generar análisis con GPT-4o-mini.

Variables de entorno requeridas:
- OPENAI_API_KEY: API Key de OpenAI
- FASTMCP_SERVER_URL: URL del servidor MCP desplegado
- FASTMCP_API_KEY: API Key de FastMCP Cloud
"""

import os
import asyncio
import httpx
import json
from openai import OpenAI
from typing import Dict, Any, List


# 🔧 CONFIGURACIÓN
def get_config() -> tuple[str, str, str]:
    """
    Obtiene la configuración desde variables de entorno.
    
    Returns:
        tuple: (OPENAI_API_KEY, FASTMCP_SERVER_URL, FASTMCP_API_KEY)
    
    Raises:
        ValueError: Si faltan variables de entorno requeridas
    """
    openai_key = os.getenv("OPENAI_API_KEY")
    server_url = os.getenv("FASTMCP_SERVER_URL")
    fastmcp_key = os.getenv("FASTMCP_API_KEY")
    
    missing = []
    if not openai_key:
        missing.append("OPENAI_API_KEY")
    if not server_url:
        missing.append("FASTMCP_SERVER_URL")
    if not fastmcp_key:
        missing.append("FASTMCP_API_KEY")
    
    if missing:
        raise ValueError(
            f"❌ Variables de entorno no configuradas: {', '.join(missing)}\n\n"
            "Configúralas con:\n"
            '  $env:OPENAI_API_KEY = "sk-..."\n'
            '  $env:FASTMCP_SERVER_URL = "https://tu-servidor.fastmcp.app"\n'
            '  $env:FASTMCP_API_KEY = "fmcp_..."\n'
        )
    
    return openai_key, server_url, fastmcp_key


# Obtener configuración
try:
    OPENAI_API_KEY, FASTMCP_SERVER_URL, FASTMCP_API_KEY = get_config()
except ValueError as e:
    print(str(e))
    print("\n💡 Usa las mismas credenciales de openai-integration")
    exit(1)


OPENAI_MODEL = "gpt-4o-mini"


# Cliente OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)


async def call_mcp_tool(tool_name: str, arguments: dict) -> Any:
    """Llama a una herramienta MCP en FastMCP Cloud"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FASTMCP_SERVER_URL}/mcp",
            headers={
                "Authorization": f"Bearer {FASTMCP_API_KEY}",
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
        
        # Parsear respuesta SSE
        content = response.text
        if 'text/event-stream' in response.headers.get('content-type', ''):
            lines = content.strip().split('\n')
            for line in lines:
                if line.startswith('data: '):
                    data = line[6:]
                    result = json.loads(data)
                    if "result" in result:
                        # Extraer el contenido de la respuesta MCP
                        content_items = result["result"].get("content", [])
                        for item in content_items:
                            if "text" in item:
                                return item["text"]
                    return result
        
        return response.json()


async def read_mcp_resource(uri: str) -> str:
    """Lee un recurso MCP"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FASTMCP_SERVER_URL}/mcp",
            headers={
                "Authorization": f"Bearer {FASTMCP_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": 3,
                "method": "resources/read",
                "params": {
                    "uri": uri
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
                    if "result" in result:
                        contents = result["result"].get("contents", [])
                        if contents:
                            return contents[0].get("text", "")
                    return str(result)
        
        return response.text


async def get_mcp_prompt(prompt_name: str, arguments: dict = None) -> str:
    """Obtiene un prompt MCP"""
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{FASTMCP_SERVER_URL}/mcp",
            headers={
                "Authorization": f"Bearer {FASTMCP_API_KEY}",
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            json={
                "jsonrpc": "2.0",
                "id": 4,
                "method": "prompts/get",
                "params": {
                    "name": prompt_name,
                    "arguments": arguments or {}
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
                    if "result" in result:
                        messages = result["result"].get("messages", [])
                        if messages:
                            return messages[0].get("content", {}).get("text", "")
                    return str(result)
        
        return response.text


async def main():
    """Función principal - Demo de gestión de ideas con MCP"""
    print("=" * 70)
    print("🚀 Cliente MCP - Gestión de Ideas de Proyectos")
    print("=" * 70)
    print(f"🤖 Modelo OpenAI: {OPENAI_MODEL}")
    print(f"🔗 Servidor MCP: {FASTMCP_SERVER_URL}")
    print(f"🔑 OpenAI API Key: {OPENAI_API_KEY[:20]}...")
    print("=" * 70)
    
    try:
        # 1. Agregar una idea usando la tool `add_idea`
        print("\n📝 Agregando una nueva idea de proyecto...")
        response_add = await call_mcp_tool(
            "add_idea",
            {
                "title": "App Verde",
                "description": "Una app que incentiva el reciclaje con recompensas.",
                "author": "Nacho"
            }
        )
        print(f"✅ {response_add}\n")
        
        # 2. Listar ideas registradas
        print("📋 Listando todas las ideas registradas...")
        ideas = await call_mcp_tool("list_ideas", {})
        print(f"Ideas: {ideas}\n")
        
        # 3. Obtener recurso: Guía de evaluación
        print("📘 Obteniendo guía para evaluar ideas...")
        guide = await read_mcp_resource("ideas://guide")
        print(f"Guía:\n{guide}\n")
        
        # 4. Obtener recurso: Ejemplos inspiradores
        print("💡 Obteniendo ejemplos de proyectos...")
        examples = await read_mcp_resource("ideas://examples")
        print(f"Ejemplos:\n{examples}\n")
        
        # 5. Obtener prompt para análisis
        print("🧩 Obteniendo prompt de análisis...")
        idea_description = (
            "Una aplicación móvil que conecta turistas con guías locales "
            "según sus intereses culturales y gastronómicos."
        )
        
        prompt_text = await get_mcp_prompt(
            "analyze_idea",
            {"idea_description": idea_description}
        )
        
        print(f"Prompt generado:\n{prompt_text}\n")
        
        # 6. Usar GPT-4o-mini para analizar la idea
        print("🧠 Analizando idea con GPT-4o-mini...")
        response = openai_client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Eres un experto evaluador de proyectos innovadores."},
                {"role": "user", "content": prompt_text}
            ]
        )
        
        analysis = response.choices[0].message.content
        
        print("\n" + "=" * 70)
        print("💬 Análisis generado por GPT-4o-mini:")
        print("=" * 70)
        print(analysis)
        print("=" * 70)
        
        print("\n✅ Demo completada exitosamente")
        
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