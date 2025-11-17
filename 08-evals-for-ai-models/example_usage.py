"""
Script de ejemplo mostrando cómo usar los componentes de solution_lab8.py
de forma manual si deseas probar partes específicas.
"""

from solution_lab8 import (
    create_custom_dataset,
    generate_responses_with_llm,
    evaluate_faithfulness,
    evaluate_completeness,
    visualize_results,
    generate_report
)

# ============================================================================
# EJEMPLO 1: Crear dataset y ver su estructura
# ============================================================================

print("=" * 80)
print("EJEMPLO 1: Crear y inspeccionar dataset")
print("=" * 80)

dataset = create_custom_dataset()

print(f"\nTotal de preguntas: {len(dataset['questions'])}")
print(f"Total de contextos: {len(dataset['contexts'])}")
print(f"Total de respuestas referencia: {len(dataset['answers'])}")

print("\n🔍 Detalles del primer par:")
print(f"\nPregunta 1: {dataset['questions'][0]}")
print(f"\nContexto 1: {dataset['contexts'][0][0][:150]}...")
print(f"\nRespuesta de referencia 1: {dataset['answers'][0][:150]}...")


# ============================================================================
# EJEMPLO 2: Usar solo Faithfulness
# ============================================================================

print("\n" + "=" * 80)
print("EJEMPLO 2: Evaluar solo Faithfulness")
print("=" * 80)

# Descomenta la siguiente línea para generar respuestas reales
# generated_responses = generate_responses_with_llm(dataset)

# Para este ejemplo, usamos respuestas simuladas
generated_responses = [
    "La Revolución Industrial transformó la manufactura mediante máquinas, "
    "causando migración de rural a urbano y creación de la clase obrera.",
    
    "La fotosíntesis convierte luz, agua y CO2 en glucosa y oxígeno "
    "en dos fases: reacción luminosa y ciclo de Calvin.",
    
    "El cambio climático es el aumento de temperaturas por emisiones "
    "humanas de gases de efecto invernadero.",
    
    "Ada Lovelace escribió el primer algoritmo para máquinas en 1843, "
    "siendo pionera de la programación.",
    
    "El ejercicio mejora la salud cardiovascular, muscular y mental, "
    "reduciendo enfermedades crónicas."
]

# Descomenta para evaluar (requiere API key):
# faithfulness_df = evaluate_faithfulness(dataset, generated_responses)
# print(faithfulness_df)


# ============================================================================
# EJEMPLO 3: Usar solo Completitud
# ============================================================================

print("\n" + "=" * 80)
print("EJEMPLO 3: Evaluar solo Completitud")
print("=" * 80)

# Descomenta para evaluar (requiere API key):
# completeness_df = evaluate_completeness(dataset, generated_responses)
# print(completeness_df)


# ============================================================================
# EJEMPLO 4: Comparar dos respuestas para la misma pregunta
# ============================================================================

print("\n" + "=" * 80)
print("EJEMPLO 4: Comparar respuestas diferentes")
print("=" * 80)

pregunta = dataset['questions'][0]
contexto = dataset['contexts'][0]
respuesta_ref = dataset['answers'][0]

respuesta_buena = (
    "La Revolución Industrial (1760-1840) fue un período de transformación "
    "económica y social que comenzó en Gran Bretaña. Marcó el cambio de economías "
    "agrícolas a industriales mediante la mecanización de la manufactura. "
    "Provocó la migración masiva de trabajadores rurales a ciudades, creando "
    "la clase obrera moderna. Aunque aumentó la producción de bienes, también "
    "generó condiciones laborales precarias, contaminación ambiental y desigualdad socioeconómica."
)

respuesta_pobre = (
    "La Revolución Industrial fue muy importante. Los industriales ganaban dinero. "
    "También fue importante en la política europea del siglo XIX. "
    "Los trabajadores iban a las fábricas porque querían."
)

print(f"\nPregunta: {pregunta}\n")

print("✅ RESPUESTA BUENA (esperada alta Faithfulness y Completitud):")
print(respuesta_buena)

print("\n❌ RESPUESTA POBRE (esperada baja Faithfulness y Completitud):")
print(respuesta_pobre)

print("\nNota: Las respuestas pobres muestran:")
print("  - Falta de detalles específicos del contexto")
print("  - Información imprecisa o vaga")
print("  - Información sin fundamento en el contexto")


# ============================================================================
# EJEMPLO 5: Ejecutar pipeline completo
# ============================================================================

print("\n" + "=" * 80)
print("EJEMPLO 5: Para ejecutar el pipeline completo")
print("=" * 80)

print("""
Ejecuta en terminal:

    python solution_lab8.py

Esto hará:
    1. Crear dataset con 5 pares
    2. Generar respuestas con LLM
    3. Evaluar Faithfulness
    4. Evaluar Completitud (métrica personalizada)
    5. Crear visualizaciones
    6. Generar reportes en CSV y PNG

Archivos generados:
    - faithfulness_results.csv
    - completeness_results.csv
    - evaluation_results.png
    - evaluation_report.txt
""")


if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("Fin de ejemplos")
    print("=" * 80)
