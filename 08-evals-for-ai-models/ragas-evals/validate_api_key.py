"""
validate_api_key.py

Valida que tu OpenAI API key funciona correctamente
"""

import os
import sys
from dotenv import load_dotenv

def validate_api_key():
    """
    Valida la configuración de la OpenAI API key
    Busca en: 1) Variable de entorno, 2) Archivo .env
    """
    
    print("\n" + "="*70)
    print("🔐 VALIDACIÓN DE OPENAI API KEY")
    print("="*70)
    
    # Intentar cargar desde variable de entorno primero
    print("\n1️⃣  Buscando OPENAI_API_KEY...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    source = "Variable de entorno"
    
    if api_key:
        print(f"   ✅ Encontrada en variable de entorno")
    else:
        print("   ℹ️  No encontrada en variable de entorno")
        print("   🔍 Buscando en archivo .env...")
        
        # Intentar cargar desde .env
        if os.path.exists(".env"):
            load_dotenv()
            api_key = os.getenv("OPENAI_API_KEY")
            source = "Archivo .env"
            
            if api_key:
                print("   ✅ Encontrada en archivo .env")
            else:
                print("   ❌ Archivo .env existe pero no contiene OPENAI_API_KEY")
        else:
            print("   ℹ️  Archivo .env no existe (es opcional)")
    
    if not api_key:
        print("\n" + "-"*70)
        print("\n   📝 Configura tu API key con una de estas opciones:\n")
        print("   OPCIÓN 1 - Variable de entorno (RECOMENDADO):")
        print("   " + "-"*50)
        print("   PowerShell:")
        print("      $env:OPENAI_API_KEY = 'sk-proj-tu-clave'")
        print("      python validate_api_key.py")
        print()
        print("   Bash/Linux/Mac:")
        print("      export OPENAI_API_KEY='sk-proj-tu-clave'")
        print("      python validate_api_key.py")
        print()
        print("   OPCIÓN 2 - Archivo .env (Desarrollo local):")
        print("   " + "-"*50)
        print("   1. Copia: cp .env.example .env")
        print("   2. Edita: .env con tu clave real")
        print("   3. Ejecuta: python validate_api_key.py")
        print()
        print("   Obtén tu clave en:")
        print("   https://platform.openai.com/api-keys")
        print()
        return False
    
    if api_key == "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx":
        print("\n   ❌ OPENAI_API_KEY aún tiene valor de ejemplo")
        print("\n   📝 Reemplaza con tu clave real")
        return False
    
    if not api_key.startswith("sk-proj-"):
        print("\n   ❌ OPENAI_API_KEY no tiene formato correcto")
        print("   Debe empezar con: sk-proj-")
        print(f"   Actual: {api_key[:20]}...")
        return False
    
    print(f"\n   ✅ OPENAI_API_KEY válida (fuente: {source})")
    print(f"   Formato: {api_key[:20]}...\n")
    
    # Probar conexión
    print("2️⃣  Probando conexión con OpenAI API...")
    
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=api_key)
        
        # Hacer una prueba simple
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": "Responde con una palabra: funciona"
                }
            ],
            max_tokens=10,
            temperature=0.7
        )
        
        print("   ✅ Conexión exitosa con OpenAI API")
        print(f"   Modelo: gpt-4o-mini")
        print(f"   Respuesta: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"   ❌ Error conectando a OpenAI: {str(e)}")
        
        if "401" in str(e) or "authentication" in str(e).lower():
            print("\n   📝 Parece que tu API key es inválida:")
            print("   1. Verifica que copiaste correctamente desde OpenAI")
            print("   2. Revisa que no haya espacios en blanco")
            print("   3. Genera una nueva clave si es necesario")
        
        if "429" in str(e) or "rate limit" in str(e).lower():
            print("\n   ⏳ Has excedido el rate limit de OpenAI")
            print("   Espera unos minutos e intenta de nuevo")
        
        return False
    
    return True


def main():
    """Ejecutar validación"""
    
    success = validate_api_key()
    
    print("\n" + "="*70)
    if success:
        print("✨ ¡API KEY VALIDADA CORRECTAMENTE! ✨")
        print("="*70)
        print("\n🚀 Ya puedes ejecutar: python evals.py")
        return 0
    else:
        print("⚠️  CONFIGURACIÓN INCOMPLETA")
        print("="*70)
        print("\n⚙️  Pasos para resolver:")
        print("   1. Usa la variable de entorno: $env:OPENAI_API_KEY = '...'")
        print("   2. O copia .env.example a .env y edítalo")
        print("   3. Ejecuta nuevamente este script para validar")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
