"""
Ejemplos de uso del servidor MCP personalizado.

Este archivo contiene ejemplos prácticos de cómo usar
cada herramienta disponible en el servidor.
"""

import asyncio
from client import MCPClient


async def example_1_count_letters():
    """Ejemplo 1: Contar letras 'r' en un texto (Lab 6)"""
    print("\n" + "="*60)
    print("Ejemplo 1: Contar letras 'r'")
    print("="*60)
    
    client = MCPClient()
    await client.connect()
    
    # Prueba 1: Terrarium
    print("\n📌 Prueba 1: 'Terrarium'")
    result = await client.call_tool(
        "count_character",
        text="Terrarium",
        character="r"
    )
    print(f"   Texto: Terrarium")
    print(f"   Letras 'r': {result['count']}")
    print(f"   Porcentaje: {result['percentage']}%")
    
    # Prueba 2: Frase
    print("\n📌 Prueba 2: 'El perro corre rápido'")
    result = await client.call_tool(
        "count_character",
        text="El perro corre rápido",
        character="r"
    )
    print(f"   Texto: El perro corre rápido")
    print(f"   Letras 'r': {result['count']}")
    
    # Prueba 3: Comparación
    print("\n📌 Prueba 3: Comparación")
    result1 = await client.call_tool(
        "count_character",
        text="Refrigerador",
        character="r"
    )
    result2 = await client.call_tool(
        "count_character",
        text="Computadora",
        character="r"
    )
    print(f"   'Refrigerador': {result1['count']} letras 'r'")
    print(f"   'Computadora': {result2['count']} letras 'r'")
    print(f"   ¿Hay más en Refrigerador? {result1['count'] > result2['count']}")
    
    await client.disconnect()


async def example_2_text_analysis():
    """Ejemplo 2: Análisis de texto"""
    print("\n" + "="*60)
    print("Ejemplo 2: Análisis de texto")
    print("="*60)
    
    client = MCPClient()
    await client.connect()
    
    text = "Python es un lenguaje de programación versátil y poderoso"
    
    print(f"\n📝 Analizando: '{text}'")
    result = await client.call_tool(
        "analyze_text",
        text=text
    )
    
    print(f"\n   📊 Estadísticas:")
    print(f"      • Caracteres: {result['character_count']}")
    print(f"      • Palabras: {result['word_count']}")
    print(f"      • Líneas: {result['line_count']}")
    print(f"      • Longitud promedio de palabras: {result['average_word_length']}")
    
    await client.disconnect()


async def example_3_text_conversion():
    """Ejemplo 3: Conversión de texto"""
    print("\n" + "="*60)
    print("Ejemplo 3: Conversión de texto")
    print("="*60)
    
    client = MCPClient()
    await client.connect()
    
    text = "Hola Mundo"
    formats = ["uppercase", "lowercase", "title", "reverse"]
    
    print(f"\n🔄 Conversiones de '{text}':")
    
    for format in formats:
        result = await client.call_tool(
            "convert_text",
            text=text,
            format=format
        )
        print(f"   • {format.upper()}: {result['converted']}")
    
    await client.disconnect()


async def example_4_system_info():
    """Ejemplo 4: Obtener información del sistema"""
    print("\n" + "="*60)
    print("Ejemplo 4: Información del sistema")
    print("="*60)
    
    client = MCPClient()
    await client.connect()
    
    result = await client.call_tool("get_system_info")
    
    print(f"\n💻 Información del sistema:")
    print(f"   • SO: {result.get('platform', 'N/A')}")
    print(f"   • Python: {result.get('python_version', 'N/A')}")
    print(f"   • CPUs: {result.get('cpu_count', 'N/A')}")
    
    if 'memory' in result:
        memory = result['memory']
        print(f"   • Memoria total: {memory.get('total_gb', 'N/A')} GB")
        print(f"   • Memoria disponible: {memory.get('available_gb', 'N/A')} GB")
        print(f"   • Uso: {memory.get('percent_used', 'N/A')}%")
    
    await client.disconnect()


async def example_5_file_operations():
    """Ejemplo 5: Operaciones con archivos"""
    print("\n" + "="*60)
    print("Ejemplo 5: Operaciones con archivos")
    print("="*60)
    
    client = MCPClient()
    await client.connect()
    
    # Listar directorio actual
    print("\n📂 Contenido del directorio actual:")
    result = await client.call_tool(
        "list_directory",
        directory="."
    )
    
    if result.get('success'):
        print(f"   • Archivos: {len(result['files'])}")
        for file in result['files'][:5]:  # Mostrar primeros 5
            print(f"      - {file}")
        if len(result['files']) > 5:
            print(f"      ... y {len(result['files']) - 5} más")
        
        print(f"\n   • Directorios: {len(result['directories'])}")
        for dir in result['directories'][:5]:
            print(f"      - {dir}/")
        if len(result['directories']) > 5:
            print(f"      ... y {len(result['directories']) - 5} más")
    
    await client.disconnect()


async def example_6_data_generation():
    """Ejemplo 6: Generación de datos"""
    print("\n" + "="*60)
    print("Ejemplo 6: Generación de datos de muestra")
    print("="*60)
    
    client = MCPClient()
    await client.connect()
    
    # Generar emails
    print("\n📧 Emails generados:")
    result = await client.call_tool(
        "generate_sample_data",
        data_type="emails",
        count=3
    )
    for email in result['items']:
        print(f"   • {email}")
    
    # Generar nombres
    print("\n👤 Nombres generados:")
    result = await client.call_tool(
        "generate_sample_data",
        data_type="names",
        count=3
    )
    for name in result['items']:
        print(f"   • {name}")
    
    # Generar URLs
    print("\n🌐 URLs generadas:")
    result = await client.call_tool(
        "generate_sample_data",
        data_type="urls",
        count=3
    )
    for url in result['items']:
        print(f"   • {url}")
    
    # Generar números
    print("\n🔢 Números generados:")
    result = await client.call_tool(
        "generate_sample_data",
        data_type="numbers",
        count=5
    )
    print(f"   • {', '.join(map(str, result['items']))}")
    
    await client.disconnect()


async def example_7_combined():
    """Ejemplo 7: Caso de uso combinado"""
    print("\n" + "="*60)
    print("Ejemplo 7: Caso de uso combinado - Procesamiento de texto")
    print("="*60)
    
    client = MCPClient()
    await client.connect()
    
    # Texto original
    text = "Model Context Protocol es fundamental para la IA"
    print(f"\n📝 Texto original: '{text}'")
    
    # 1. Analizar
    print("\n1️⃣ Análisis:")
    analysis = await client.call_tool("analyze_text", text=text)
    print(f"   Palabras: {analysis['word_count']}, Caracteres: {analysis['character_count']}")
    
    # 2. Convertir a mayúsculas
    print("\n2️⃣ Conversión a mayúsculas:")
    upper = await client.call_tool("convert_text", text=text, format="uppercase")
    print(f"   {upper['converted']}")
    
    # 3. Contar 'a'
    print("\n3️⃣ Contar letra 'a':")
    count = await client.call_tool("count_character", text=text, character="a")
    print(f"   Total: {count['count']} (Porcentaje: {count['percentage']}%)")
    
    # 4. Invertir
    print("\n4️⃣ Texto invertido:")
    reverse = await client.call_tool("convert_text", text=text, format="reverse")
    print(f"   {reverse['converted']}")
    
    await client.disconnect()


async def main():
    """Ejecuta todos los ejemplos"""
    print("🧪 Ejemplos de uso del Servidor MCP")
    
    try:
        await example_1_count_letters()
        await example_2_text_analysis()
        await example_3_text_conversion()
        await example_4_system_info()
        await example_5_file_operations()
        await example_6_data_generation()
        await example_7_combined()
        
        print("\n" + "="*60)
        print("✅ Todos los ejemplos completados exitosamente")
        print("="*60)
        
    except ConnectionError:
        print("\n❌ No se pudo conectar al servidor")
        print("Asegúrate de ejecutar 'python server.py' en otra terminal")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
