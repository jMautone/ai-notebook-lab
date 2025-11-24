from langfuse import get_client
from langfuse.openai import openai
import os
from dotenv import load_dotenv
import time

load_dotenv()

langfuse = get_client()

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run_inefficient_prompt():
    """
    Prompt ineficiente: solicita una receta con instrucciones detalladas
    sin especificar límites ni estructura, lo que genera respuestas largas
    y consume más tokens.
    """
    print("=" * 80)
    print("🔴 EJECUTANDO PROMPT INEFICIENTE")
    print("=" * 80)
    start_time = time.time()
    
    # Prompt original ineficiente del ejercicio
    prompt = "Genera una receta de pasta con instrucciones detalladas."
    
    print(f"\nPrompt: {prompt}")
    print(f"Longitud del prompt: {len(prompt)} caracteres\n")
    
    # Crear span para el experimento
    span = langfuse.start_span(
        name="recipe_optimization_experiment",
        metadata={"tags": ["inefficient"], "prompt_type": "detailed_recipe"}
    )
    
    # Crear generation dentro del span
    generation = span.start_generation(
        name="inefficient_recipe_generation",
        model="gpt-4o-mini",
        input=prompt
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    output = response.choices[0].message.content
    generation.update(output=output)
    generation.end()
    span.end()
    
    end_time = time.time()
    
    print(f"⏱️  Tiempo de ejecución: {end_time - start_time:.2f}s")
    print(f"📝 Longitud de respuesta: {len(output)} caracteres")
    print(f"🔢 Tokens de entrada: {response.usage.prompt_tokens}")
    print(f"🔢 Tokens de salida: {response.usage.completion_tokens}")
    print(f"🔢 Tokens totales: {response.usage.total_tokens}")
    print(f"\n📄 Respuesta generada:")
    print("-" * 80)
    print(output)
    print("-" * 80)
    
    return {
        "output": output,
        "time": end_time - start_time,
        "chars": len(output),
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    }

def run_optimized_prompt():
    """
    Prompt optimizado: aplica múltiples estrategias de optimización:
    1. Reducir longitud innecesaria: solicita formato conciso
    2. Pedir respuestas más breves: especifica límites (máx 150 palabras)
    3. Reestructurar de manera más clara: usa formato JSON estructurado
    4. Instrucciones más directas: especifica exactamente qué campos incluir
    """
    print("\n" + "=" * 80)
    print("🟢 EJECUTANDO PROMPT OPTIMIZADO")
    print("=" * 80)
    start_time = time.time()
    
    # Prompt optimizado con múltiples estrategias
    prompt = """Receta de pasta. JSON: {"nombre": str, "ingredientes": list[str] (máx 6), "pasos": list[str] (máx 4 pasos, cada uno <20 palabras)}. Máx 150 palabras total."""
    
    print(f"\nPrompt: {prompt}")
    print(f"Longitud del prompt: {len(prompt)} caracteres\n")
    
    # Crear span para el experimento
    span = langfuse.start_span(
        name="recipe_optimization_experiment",
        metadata={"tags": ["optimized"], "prompt_type": "structured_recipe"}
    )
    
    # Crear generation dentro del span
    generation = span.start_generation(
        name="optimized_recipe_generation",
        model="gpt-4o-mini",
        input=prompt
    )
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0  # Temperatura 0 para mayor consistencia
    )
    
    output = response.choices[0].message.content
    generation.update(output=output)
    generation.end()
    span.end()
    
    end_time = time.time()
    
    print(f"⏱️  Tiempo de ejecución: {end_time - start_time:.2f}s")
    print(f"📝 Longitud de respuesta: {len(output)} caracteres")
    print(f"🔢 Tokens de entrada: {response.usage.prompt_tokens}")
    print(f"🔢 Tokens de salida: {response.usage.completion_tokens}")
    print(f"🔢 Tokens totales: {response.usage.total_tokens}")
    print(f"\n📄 Respuesta generada:")
    print("-" * 80)
    print(output)
    print("-" * 80)
    
    return {
        "output": output,
        "time": end_time - start_time,
        "chars": len(output),
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens
    }

def print_comparison(inefficient_results, optimized_results):
    """Imprime una comparación detallada de las métricas"""
    print("\n" + "=" * 80)
    print("📊 COMPARACIÓN DE RESULTADOS")
    print("=" * 80)
    
    # Calcular mejoras
    time_reduction = ((inefficient_results["time"] - optimized_results["time"]) / inefficient_results["time"]) * 100
    chars_reduction = ((inefficient_results["chars"] - optimized_results["chars"]) / inefficient_results["chars"]) * 100
    tokens_reduction = ((inefficient_results["total_tokens"] - optimized_results["total_tokens"]) / inefficient_results["total_tokens"]) * 100
    
    print(f"\n⏱️  LATENCIA:")
    print(f"   Ineficiente: {inefficient_results['time']:.2f}s")
    print(f"   Optimizado:  {optimized_results['time']:.2f}s")
    print(f"   Mejora:      {time_reduction:+.1f}% {'✅' if time_reduction > 0 else '⚠️'}")
    
    print(f"\n📝 LONGITUD DE RESPUESTA:")
    print(f"   Ineficiente: {inefficient_results['chars']} caracteres")
    print(f"   Optimizado:  {optimized_results['chars']} caracteres")
    print(f"   Reducción:   {chars_reduction:+.1f}% {'✅' if chars_reduction > 0 else '⚠️'}")
    
    print(f"\n🔢 TOKENS:")
    print(f"   Ineficiente:")
    print(f"      - Entrada:  {inefficient_results['prompt_tokens']}")
    print(f"      - Salida:   {inefficient_results['completion_tokens']}")
    print(f"      - Total:    {inefficient_results['total_tokens']}")
    print(f"   Optimizado:")
    print(f"      - Entrada:  {optimized_results['prompt_tokens']}")
    print(f"      - Salida:   {optimized_results['completion_tokens']}")
    print(f"      - Total:    {optimized_results['total_tokens']}")
    print(f"   Reducción:   {tokens_reduction:+.1f}% {'✅' if tokens_reduction > 0 else '⚠️'}")
    
    # Estimación de costos (GPT-4o-mini pricing aproximado)
    # Input: $0.150 / 1M tokens, Output: $0.600 / 1M tokens
    cost_inefficient = (inefficient_results['prompt_tokens'] * 0.150 + inefficient_results['completion_tokens'] * 0.600) / 1_000_000
    cost_optimized = (optimized_results['prompt_tokens'] * 0.150 + optimized_results['completion_tokens'] * 0.600) / 1_000_000
    cost_reduction = ((cost_inefficient - cost_optimized) / cost_inefficient) * 100
    
    print(f"\n💰 COSTO ESTIMADO (GPT-4o-mini):")
    print(f"   Ineficiente: ${cost_inefficient:.6f}")
    print(f"   Optimizado:  ${cost_optimized:.6f}")
    print(f"   Ahorro:      {cost_reduction:+.1f}% {'✅' if cost_reduction > 0 else '⚠️'}")
    
    print("\n" + "=" * 80)
    print("✅ CONCLUSIÓN:")
    if tokens_reduction > 0 and time_reduction > 0:
        print("   La optimización fue EFECTIVA en reducir tokens y latencia.")
    elif tokens_reduction > 0:
        print("   La optimización redujo tokens pero no mejoró significativamente la latencia.")
    else:
        print("   ⚠️  La optimización no fue efectiva. Revisar estrategia.")
    print("=" * 80)

if __name__ == "__main__":
    print("\n🚀 INICIANDO EXPERIMENTO DE OPTIMIZACIÓN DE PROMPTS")
    print("📋 Ejercicio 4: Optimización - Lab 9 Monitoring\n")
    
    # Ejecutar ambos prompts
    inefficient_results = run_inefficient_prompt()
    optimized_results = run_optimized_prompt()
    
    # Comparar resultados
    print_comparison(inefficient_results, optimized_results)
    
    # Flush Langfuse
    langfuse.flush()
    print("\n✅ Trazas enviadas a Langfuse. Revisa el dashboard para análisis detallado.")

