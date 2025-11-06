"""
Cliente OpenAI con integración MCP
Parte 3: Integración OpenAI + FastMCP

Este cliente permite a GPT-4o-mini usar herramientas MCP desplegadas en FastMCP Cloud.
"""

import asyncio
import httpx
import json
import os
from openai import OpenAI
from typing import Optional, Dict, Any, List


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
    print("\n💡 Ver .env.example para más detalles")
    exit(1)


# Cliente OpenAI
openai_client = OpenAI(api_key=OPENAI_API_KEY)


async def list_mcp_tools() -> List[Dict[str, Any]]:
    """Lista las herramientas disponibles en el servidor MCP"""
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
                "id": 1,
                "method": "tools/list",
                "params": {}
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
                    return result.get("result", {}).get("tools", [])
        
        return response.json().get("result", {}).get("tools", [])


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


def mcp_tools_to_openai_format(mcp_tools: List[Dict]) -> List[Dict]:
    """
    Convierte herramientas MCP al formato de OpenAI Function Calling.
    
    Args:
        mcp_tools: Lista de herramientas en formato MCP
    
    Returns:
        Lista de herramientas en formato OpenAI
    """
    openai_tools = []
    
    for tool in mcp_tools:
        openai_tool = {
            "type": "function",
            "function": {
                "name": tool["name"],
                "description": tool.get("description", ""),
                "parameters": tool.get("inputSchema", {
                    "type": "object",
                    "properties": {},
                    "required": []
                })
            }
        }
        openai_tools.append(openai_tool)
    
    return openai_tools


async def chat_with_tools(user_message: str) -> str:
    """
    Envía un mensaje a GPT-4o-mini con acceso a herramientas MCP.
    
    Args:
        user_message: Mensaje del usuario
    
    Returns:
        Respuesta del modelo
    """
    print(f"\n💬 Usuario: {user_message}")
    
    # Obtener herramientas MCP disponibles
    print("🔍 Obteniendo herramientas MCP...")
    mcp_tools = await list_mcp_tools()
    
    if not mcp_tools:
        return "❌ No hay herramientas MCP disponibles"
    
    print(f"✅ Herramientas encontradas: {', '.join([t['name'] for t in mcp_tools])}")
    
    # Convertir a formato OpenAI
    openai_tools = mcp_tools_to_openai_format(mcp_tools)
    
    # Primera llamada a OpenAI
    messages = [
        {"role": "system", "content": "Eres un asistente útil que puede usar herramientas para responder preguntas. Cuando uses una herramienta, explica claramente qué estás haciendo y los resultados obtenidos."},
        {"role": "user", "content": user_message}
    ]
    
    print("🤖 Consultando a GPT-4o-mini...")
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=openai_tools,
        tool_choice="auto"
    )
    
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    # Si no hay llamadas a herramientas, retornar respuesta directa
    if not tool_calls:
        return response_message.content
    
    # Procesar llamadas a herramientas
    messages.append(response_message)
    
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        print(f"\n🔧 Llamando a herramienta MCP: {function_name}")
        print(f"   Argumentos: {function_args}")
        
        # Llamar a la herramienta MCP
        function_response = await call_mcp_tool(function_name, function_args)
        
        print(f"   ✅ Resultado: {function_response}")
        
        # Agregar respuesta de la herramienta al contexto
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": function_name,
            "content": str(function_response)
        })
    
    # Segunda llamada a OpenAI con los resultados
    print("\n🤖 Generando respuesta final...")
    final_response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    return final_response.choices[0].message.content


async def main():
    """Función principal - Pruebas de integración"""
    print("=" * 70)
    print("🚀 Integración OpenAI + FastMCP")
    print("=" * 70)
    print(f"🤖 Modelo: gpt-4o-mini")
    print(f"🔗 Servidor MCP: {FASTMCP_SERVER_URL}")
    print(f"🔑 OpenAI API Key: {OPENAI_API_KEY[:20]}...")
    print("=" * 70)
    
    # Pruebas según el enunciado
    test_queries = [
        "¿Cuántas letras 'r' hay en la palabra 'Terrarium'?",
        "Cuenta las 'r' en: 'El perro corre rápido por el parque'",
        "¿Hay más letras 'r' en 'Refrigerador' o en 'Computadora'?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'=' * 70}")
        print(f"📝 Prueba {i}/{len(test_queries)}")
        print(f"{'=' * 70}")
        
        try:
            answer = await chat_with_tools(query)
            print(f"\n✨ Respuesta de GPT-4o-mini:\n{answer}")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
        
        if i < len(test_queries):
            print("\n⏳ Esperando antes de la siguiente prueba...")
            await asyncio.sleep(2)
    
    print(f"\n{'=' * 70}")
    print("✅ Todas las pruebas completadas")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())
