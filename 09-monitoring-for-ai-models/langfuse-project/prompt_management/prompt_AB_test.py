import random
from langfuse import Langfuse
from openai import OpenAI  # Sin auto-instrumentación para evitar traces duplicados
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

prompt_a = langfuse.get_prompt("itinerary_planner_experiment", label="prod-a")
prompt_b = langfuse.get_prompt("itinerary_planner_experiment", label="prod-b")

print("\n" + "="*60)
print("   🧪 A/B Testing de Prompts con Langfuse")
print("="*60 + "\n")
 
for i in range(10):
    selected_prompt = random.choice([prompt_a, prompt_b])
    prompt_label = "prod-a" if selected_prompt == prompt_a else "prod-b"

    system_message = selected_prompt.prompt

    messages = [
        {"role":"system","content": system_message},
        {"role":"user","content": "Quiero recomendaciones para mi viaje a Italia"}
    ]
    
    # Crear trace manual para el experimento A/B
    span = langfuse.start_span(
        name="ab_test_experiment",
        input="Quiero recomendaciones para mi viaje a Italia",
        metadata={
            "prompt_label": prompt_label,
            "prompt_name": "itinerary_planner_experiment",
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
      model = "gpt-4o-mini",
      messages = messages
    )
    
    output = res.choices[0].message.content
    
    # Actualizar y cerrar generation y span
    generation.update(output=output)
    generation.end()
    span.update(output=output)
    span.end()

    print(f"Run {i+1} [{prompt_label}]: {output[:100]}...\n")

langfuse.flush()
print("\n✅ Trazas enviadas a Langfuse. Revisa el dashboard para analizar el A/B test.")