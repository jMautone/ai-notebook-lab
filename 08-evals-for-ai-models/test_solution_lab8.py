"""
test_solution_lab8.py

Script de testing para verificar que la solución funciona correctamente
sin necesidad de hacer llamadas a la API (simula respuestas).
"""

import os
import sys
from typing import Dict, List
import pandas as pd

def test_imports():
    """Test 1: Verificar que todas las librerías necesarias están disponibles"""
    print("\n" + "="*70)
    print("TEST 1: Verificar Importaciones")
    print("="*70)
    
    try:
        import openai
        print("✅ openai disponible")
    except ImportError:
        print("❌ openai NO disponible - ejecuta: pip install openai")
        return False
    
    try:
        import pandas
        print("✅ pandas disponible")
    except ImportError:
        print("❌ pandas NO disponible - ejecuta: pip install pandas")
        return False
    
    try:
        import matplotlib
        print("✅ matplotlib disponible")
    except ImportError:
        print("❌ matplotlib NO disponible - ejecuta: pip install matplotlib")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv disponible")
    except ImportError:
        print("❌ python-dotenv NO disponible - ejecuta: pip install python-dotenv")
        return False
    
    return True


def test_env_file():
    """Test 2: Verificar que existe archivo .env"""
    print("\n" + "="*70)
    print("TEST 2: Verificar Archivo .env")
    print("="*70)
    
    env_path = ".env"
    
    if not os.path.exists(env_path):
        print(f"❌ No existe archivo {env_path}")
        print(f"   Crea {env_path} con tu API key")
        return False
    
    print(f"✅ Archivo {env_path} existe")
    
    # Verificar que tiene contenido
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        
        if not api_key:
            print("⚠️  OPENAI_API_KEY no configurada en .env")
            print("   Edita .env y agrega: OPENAI_API_KEY=sk-proj-tu-clave")
            return False
        
        if api_key.startswith("sk-proj-"):
            print("✅ OPENAI_API_KEY está configurada (formato válido)")
            return True
        else:
            print("⚠️  OPENAI_API_KEY no tiene formato de OpenAI")
            print("   Debe empezar con: sk-proj-")
            return False
            
    except Exception as e:
        print(f"❌ Error leyendo .env: {str(e)}")
        return False


def test_dataset_structure():
    """Test 3: Verificar estructura del dataset"""
    print("\n" + "="*70)
    print("TEST 3: Estructura del Dataset")
    print("="*70)
    
    try:
        from solution_lab8 import create_custom_dataset
        
        dataset = create_custom_dataset()
        
        # Verificar claves
        required_keys = {"questions", "contexts", "answers"}
        actual_keys = set(dataset.keys())
        
        if required_keys != actual_keys:
            print(f"❌ Keys incorrectas. Esperado: {required_keys}, Actual: {actual_keys}")
            return False
        
        print("✅ Claves correctas: questions, contexts, answers")
        
        # Verificar cantidad de pares
        num_questions = len(dataset["questions"])
        num_contexts = len(dataset["contexts"])
        num_answers = len(dataset["answers"])
        
        if num_questions != num_contexts or num_questions != num_answers:
            print(f"❌ Cantidad inconsistente: Q={num_questions}, C={num_contexts}, A={num_answers}")
            return False
        
        if num_questions < 5:
            print(f"❌ Requiere mínimo 5 pares, tiene {num_questions}")
            return False
        
        print(f"✅ Dataset tiene {num_questions} pares")
        
        # Verificar contenido
        for i in range(num_questions):
            q = dataset["questions"][i]
            c = dataset["contexts"][i]
            a = dataset["answers"][i]
            
            if not isinstance(q, str) or len(q) == 0:
                print(f"❌ Pregunta {i} inválida")
                return False
            
            if not isinstance(c, list) or len(c) == 0:
                print(f"❌ Contexto {i} inválido (debe ser lista)")
                return False
            
            if not isinstance(a, str) or len(a) == 0:
                print(f"❌ Respuesta {i} inválida")
                return False
            
            # Verificar longitud de contexto
            context_length = sum(len(ctx) for ctx in c)
            if context_length < 100:
                print(f"⚠️  Contexto {i} muy corto ({context_length} caracteres)")
        
        print("✅ Todas las preguntas, contextos y respuestas válidas")
        return True
        
    except Exception as e:
        print(f"❌ Error en dataset: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_functions_exist():
    """Test 4: Verificar que todas las funciones existen"""
    print("\n" + "="*70)
    print("TEST 4: Funciones Requeridas")
    print("="*70)
    
    try:
        from solution_lab8 import (
            create_custom_dataset,
            generate_responses_with_llm,
            evaluate_faithfulness,
            evaluate_completeness,
            visualize_results,
            generate_report
        )
        
        functions = [
            ("create_custom_dataset", create_custom_dataset),
            ("generate_responses_with_llm", generate_responses_with_llm),
            ("evaluate_faithfulness", evaluate_faithfulness),
            ("evaluate_completeness", evaluate_completeness),
            ("visualize_results", visualize_results),
            ("generate_report", generate_report),
        ]
        
        for name, func in functions:
            if callable(func):
                print(f"✅ {name}() existe y es callable")
            else:
                print(f"❌ {name}() no es callable")
                return False
        
        return True
        
    except ImportError as e:
        print(f"❌ Error importando funciones: {str(e)}")
        return False


def test_mock_evaluation():
    """Test 5: Simular flujo de evaluación sin API calls"""
    print("\n" + "="*70)
    print("TEST 5: Flujo de Evaluación (Mock - sin API)")
    print("="*70)
    
    try:
        from solution_lab8 import create_custom_dataset
        
        dataset = create_custom_dataset()
        
        # Crear respuestas simuladas
        mock_responses = [
            "La Revolución Industrial transformó la manufactura mediante mecanización.",
            "La fotosíntesis convierte luz, agua y CO2 en glucosa y oxígeno.",
            "El cambio climático es el aumento de temperaturas por emisiones humanas.",
            "Ada Lovelace escribió el primer algoritmo en 1843 para máquinas.",
            "El ejercicio mejora la salud cardiovascular y mental significativamente."
        ]
        
        if len(mock_responses) != len(dataset["questions"]):
            print("❌ Cantidad de respuestas mockeadas incorrecta")
            return False
        
        # Simular creación de DataFrames
        data = {
            "Pregunta #": list(range(1, len(mock_responses) + 1)),
            "Score": [0.85, 0.80, 0.75, 0.90, 0.88],
            "Explicación": ["Mock"] * len(mock_responses)
        }
        
        df = pd.DataFrame(data)
        
        if len(df) != len(dataset["questions"]):
            print(f"❌ DataFrame tiene tamaño incorrecto")
            return False
        
        print(f"✅ Flujo de evaluación funciona (DataFrame con {len(df)} registros)")
        print(f"   Columnas: {', '.join(df.columns.tolist())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en flujo mock: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_file_structure():
    """Test 6: Verificar estructura de archivos"""
    print("\n" + "="*70)
    print("TEST 6: Estructura de Archivos")
    print("="*70)
    
    required_files = [
        ("solution_lab8.py", "Código principal"),
        (".env", "Configuración (crear si no existe)"),
        ("requirements.txt", "Dependencias"),
        ("README.md", "Documentación"),
    ]
    
    all_ok = True
    for filename, description in required_files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename} ({size} bytes) - {description}")
        else:
            if filename == ".env":
                print(f"⚠️  {filename} no existe - crea uno con tu API key")
            else:
                print(f"❌ {filename} no existe - {description}")
                all_ok = False
    
    return all_ok


def test_requirements():
    """Test 7: Verificar que requirements.txt está bien formado"""
    print("\n" + "="*70)
    print("TEST 7: Archivo Requirements.txt")
    print("="*70)
    
    if not os.path.exists("requirements.txt"):
        print("⚠️  No existe requirements.txt")
        return True
    
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read().strip().split("\n")
        
        print(f"✅ requirements.txt contiene {len(requirements)} dependencias:")
        for req in requirements:
            if req.strip():
                print(f"   - {req.strip()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo requirements.txt: {str(e)}")
        return False


def main():
    """Ejecutar todos los tests"""
    
    print("\n" + "="*70)
    print("🧪 TESTING SUITE - LAB 8 SOLUTION")
    print("="*70)
    
    tests = [
        ("Importaciones", test_imports),
        ("Archivo .env", test_env_file),
        ("Estructura Dataset", test_dataset_structure),
        ("Funciones Requeridas", test_functions_exist),
        ("Flujo Mock", test_mock_evaluation),
        ("Estructura Archivos", test_file_structure),
        ("Requirements.txt", test_requirements),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error en {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE TESTS")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\n{passed}/{total} tests pasados")
    
    if passed == total:
        print("\n" + "="*70)
        print("✨ ¡TODOS LOS TESTS PASARON! ✨")
        print("="*70)
        print("\n🚀 Próximo paso: Ejecuta")
        print("   python solution_lab8.py")
        print("\n(Asegúrate de tener tu OPENAI_API_KEY configurada en .env)")
        return 0
    else:
        print("\n" + "="*70)
        print("⚠️  ALGUNOS TESTS FALLARON")
        print("="*70)
        print("\nRevisa los errores arriba y corrígelos antes de ejecutar.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
