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
    """
    
    print("\n" + "="*70)
    print("🔐 VALIDACIÓN DE OPENAI API KEY")
    print("="*70)
    
    # Cargar .env
    print("\n1️⃣  Cargando archivo .env...")
    
    if not os.path.exists(".env"):
        print("   ❌ No existe archivo .env")
        print("\n   📝 Crea un archivo .env con el siguiente contenido:")
        print("   " + "-"*50)
        print("   OPENAI_API_KEY=sk-proj-tu-clave-aqui")
        print("   " + "-"*50)
        print("\n   Obtén tu clave en: https://platform.openai.com/api-keys")
        return False
    
    load_dotenv()
    
    print("   ✅ Archivo .env encontrado")
    
    # Verificar que existe la variable
    print("\n2️⃣  Verificando OPENAI_API_KEY...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("   ❌ OPENAI_API_KEY no está configurada")
        print("\n   📝 Asegúrate que en .env tienes:")
        print("   OPENAI_API_KEY=sk-proj-tu-clave-real")
        return False
    
    if api_key == "sk-proj-tu-clave-aqui":
        print("   ❌ OPENAI_API_KEY aún tiene valor de ejemplo")
        print("\n   📝 Reemplaza con tu clave real:")
        print("   OPENAI_API_KEY=sk-proj-tu-clave-real")
        return False
    
    if not api_key.startswith("sk-proj-"):
        print("   ❌ OPENAI_API_KEY no tiene formato correcto")
        print("   Debe empezar con: sk-proj-")
        print(f"   Actual: {api_key[:20]}...")
        return False
    
    print("   ✅ OPENAI_API_KEY está configurada")
    print(f"   Formato: {api_key[:20]}...")
    
    # Probar conexión
    print("\n3️⃣  Probando conexión con OpenAI API...")
    
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
        print("\n🚀 Ya puedes ejecutar: python solution_lab8.py")
        return 0
    else:
        print("⚠️  CONFIGURACIÓN INCOMPLETA")
        print("="*70)
        print("\n⚙️  Pasos para resolver:")
        print("   1. Edita el archivo .env")
        print("   2. Asegúrate de tener una clave válida de OpenAI")
        print("   3. Ejecuta nuevamente este script para validar")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
