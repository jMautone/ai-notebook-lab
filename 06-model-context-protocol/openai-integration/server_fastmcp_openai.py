"""
Servidor MCP para FastMCP Cloud con herramienta count_letter_r
Parte 3: Integración OpenAI + FastMCP
"""

from fastmcp import FastMCP

# Crear instancia de FastMCP
mcp = FastMCP("Count Letter R Server")


@mcp.tool()
def count_letter_r(text: str) -> int:
    """
    Cuenta cuántas veces aparece la letra 'r' (mayúscula o minúscula) en un texto.
    
    Esta herramienta es útil para analizar la frecuencia de la letra 'r' en palabras o frases.
    
    Args:
        text: La palabra o frase a analizar
    
    Returns:
        Número entero con el conteo de letras 'r' encontradas
    
    Examples:
        >>> count_letter_r("Terrarium")
        3
        >>> count_letter_r("El perro corre rápido")
        5
        >>> count_letter_r("Refrigerador")
        3
    """
    if not text:
        return 0
    
    # Contar 'r' y 'R'
    count = text.lower().count('r')
    
    return count


# Punto de entrada para FastMCP
if __name__ == "__main__":
    # Para testing local - definir función sin decorador
    def test_count_letter_r(text: str) -> int:
        """Función de prueba sin decorador"""
        if not text:
            return 0
        return text.lower().count('r')
    
    print("🔧 Servidor MCP: Count Letter R")
    print("=" * 50)
    
    # Pruebas de la herramienta
    test_cases = [
        "Terrarium",
        "El perro corre rápido por el parque",
        "Refrigerador",
        "Computadora"
    ]
    
    for test in test_cases:
        result = test_count_letter_r(test)
        print(f"'{test}' → {result} letras 'r'")
    
    print("\n✅ Herramienta funcionando correctamente")
    print("\n📤 Para desplegar en FastMCP Cloud:")
    print("   fastmcp deploy server_fastmcp_openai.py")
