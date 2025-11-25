import random
from langfuse import Langfuse
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
    base_url=os.environ.get("LANGFUSE_BASE_URL")
)

# Cliente OpenAI sin instrumentación automática
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Cargar los dos prompts separados
print("\n⏳ Cargando prompts desde Langfuse...")
try:
    prompt_a = langfuse.get_prompt("itinerary_planner_concise")
    prompt_b = langfuse.get_prompt("itinerary_planner_detailed")
    print("✅ Prompts cargados correctamente.")
except Exception as e:
    print(f"❌ Error al cargar prompts: {e}")
    print("💡 Ejecuta primero: python prompt_management/prompt_AB_test_creation.py")
    exit(1)

VARIANTS = {
    "A": ("itinerary_planner_concise", prompt_a),
    "B": ("itinerary_planner_detailed", prompt_b)
}

print("\n" + "="*60)
print("   🧪 A/B Testing de Prompts con Langfuse")
print("="*60 + "\n")
 
for i in range(10):
    # Seleccionar variante aleatoriamente
    variant_key = random.choice(["A", "B"])
    prompt_name, selected_prompt = VARIANTS[variant_key]

    system_message = selected_prompt.prompt
    user_input = "Quiero recomendaciones para mi viaje a Italia"

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]
    
    # Crear span con metadata clara del experimento
    span = langfuse.start_span(
        name="ab_test_experiment",
        input=user_input,
        metadata={
            "tags": [f"variant:{variant_key}", "ab-test", f"prompt:{prompt_name}"],
            "experiment": "itinerary_planner_ab_test",
            "variant": variant_key,
            "prompt_name": prompt_name,
            "run_number": i + 1
        }
    )
    
    # Crear generation dentro del span
    generation = span.start_observation(
        as_type="generation",
        name="itinerary_generation",
        model="gpt-4o-mini",
        input=messages
    )
     
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    
    output = res.choices[0].message.content
    
    # Actualizar y cerrar generation y span
    generation.update(output=output)
    generation.end()
    span.update(output=output)
    span.end()

    print(f"Run {i+1} [Variant {variant_key}]: {output[:80]}...\n")

langfuse.flush()

print("\n" + "="*60)
print("   ✅ Experimento A/B completado")
print("="*60)
print("\n📊 En Langfuse puedes filtrar por:")
print("   • variant:A → Respuestas concisas")
print("   • variant:B → Respuestas detalladas")
print("\n🔗 Revisa el dashboard: https://cloud.langfuse.com\n")