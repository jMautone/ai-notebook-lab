from langfuse import Langfuse
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
    base_url=os.environ.get("LANGFUSE_BASE_URL")
)

print("\n" + "="*60)
print("   🧪 Creación de Prompts para A/B Testing")
print("="*60 + "\n")

# Prompt A: Versión concisa y estructurada (nombre único)
print("⏳ Creando prompt versión A...")
langfuse.create_prompt(
    name="itinerary_planner_concise",
    prompt="""Eres un asistente de viajes experto. Proporciona recomendaciones concisas y bien estructuradas.

Formato de respuesta:
- Lista los destinos principales (máximo 3)
- Para cada destino: 1 actividad imperdible
- Incluye 1 consejo práctico

Sé breve y directo.""",
    config={
        "model": "gpt-4o-mini",
        "temperature": 0.3
    },
    labels=["production"],
    tags=["ab-test", "variant:A", "style:concise"]
)
print("✅ Prompt 'itinerary_planner_concise' creado.")

# Prompt B: Versión detallada y narrativa (nombre único)
print("⏳ Creando prompt versión B...")
langfuse.create_prompt(
    name="itinerary_planner_detailed",
    prompt="""Eres un guía de viajes apasionado y experimentado. Comparte tus recomendaciones de forma cálida y detallada.

Incluye en tu respuesta:
- Una breve introducción entusiasta sobre el destino
- Recomendaciones detalladas de lugares para visitar
- Tips de cultura local y gastronomía
- Mejores épocas para visitar

Usa un tono conversacional y amigable.""",
    config={
        "model": "gpt-4o-mini",
        "temperature": 0.7
    },
    labels=["production"],
    tags=["ab-test", "variant:B", "style:detailed"]
)
print("✅ Prompt 'itinerary_planner_detailed' creado.")

langfuse.flush()

print("\n" + "="*60)
print("   ✅ Prompts para A/B Testing creados exitosamente")
print("="*60)
print("\n📋 Prompts creados:")
print("   • itinerary_planner_concise  [variant:A] - Versión concisa")
print("   • itinerary_planner_detailed [variant:B] - Versión detallada")
print("\n🔗 Verifica en: https://cloud.langfuse.com → Prompts")
print("\n💡 Siguiente paso: Ejecuta 'python prompt_management/prompt_AB_test.py'")
print("   para iniciar el experimento A/B.\n")
