from langfuse import Langfuse
from openai import OpenAI  # Sin auto-instrumentación para evitar traces duplicados
import os
import re
import json
from dotenv import load_dotenv

load_dotenv()

# Un solo cliente Langfuse
langfuse = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
    base_url=os.environ.get("LANGFUSE_BASE_URL")
)

# Cliente OpenAI sin instrumentación automática
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

TONE_NAMES = {
    "1": ("explicacion_academica", "Académico-formal"),
    "2": ("explicacion_amistosa", "Conversacional-amistoso"),
    "3": ("explicacion_directa", "Directo y pragmático")
}

# Prompt de evaluación independiente
EVALUATION_PROMPT = """Eres un evaluador imparcial de respuestas. Tu tarea es calificar la siguiente respuesta según estos criterios:

1. **Precisión**: ¿La información es correcta y verificable?
2. **Claridad**: ¿La respuesta es fácil de entender?
3. **Completitud**: ¿Responde completamente la pregunta?
4. **Tono**: ¿Mantiene el tono solicitado ({tone})?

PREGUNTA DEL USUARIO:
{question}

RESPUESTA A EVALUAR:
{response}

Responde ÚNICAMENTE con un JSON en este formato exacto:
{{
    "score": <número del 1 al 5>,
    "justificacion": "<breve explicación de la calificación>"
}}

Donde:
- 1 = Muy deficiente
- 2 = Deficiente  
- 3 = Aceptable
- 4 = Buena
- 5 = Excelente
"""

def extract_evaluation(evaluation_text):
    """Extrae el score y justificación del JSON de evaluación."""
    try:
        # Buscar JSON en la respuesta
        json_match = re.search(r'\{[^}]+\}', evaluation_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group())
            score = int(data.get("score", 0))
            justification = data.get("justificacion", "Sin justificación")
            if 1 <= score <= 5:
                return score, justification
    except (json.JSONDecodeError, ValueError):
        pass
    return None, None

def evaluate_response(question, response, tone_name, span):
    """Evalúa la respuesta en una llamada separada e imparcial."""
    
    evaluation_generation = span.start_observation(
        as_type="generation",
        name="response_evaluation",
        model="gpt-4o-mini",
        input={"question": question, "response_to_evaluate": response}
    )
    
    eval_prompt = EVALUATION_PROMPT.format(
        tone=tone_name,
        question=question,
        response=response
    )
    
    eval_response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,  # Determinístico para evaluación consistente
        messages=[
            {"role": "system", "content": "Eres un evaluador imparcial. Responde solo con JSON."},
            {"role": "user", "content": eval_prompt}
        ]
    )
    
    eval_output = eval_response.choices[0].message.content
    score, justification = extract_evaluation(eval_output)
    
    evaluation_generation.update(output=eval_output)
    evaluation_generation.end()
    
    return score, justification

def generate_response(prompt, tone_name, prompt_name, user_input):
    """Genera respuesta usando el prompt seleccionado y registra en Langfuse."""
    
    # Crear span en Langfuse con tags para identificar el prompt usado
    span = langfuse.start_span(
        name="prompt_management_app",
        input=user_input,
        metadata={
            "tags": [f"prompt:{prompt_name}", f"tone:{tone_name}"],
            "tone": tone_name,
            "prompt_name": prompt_name,
            "prompt_version": prompt.version if hasattr(prompt, 'version') else "unknown"
        }
    )
    
    # PASO 1: Generar respuesta (sin auto-calificación)
    generation = span.start_observation(
        as_type="generation",
        name="knowledge_query",
        model="gpt-4o-mini",
        input=user_input
    )
    
    # Remover instrucción de auto-calificación del prompt si existe
    system_message = prompt.prompt
    system_message = re.sub(
        r'(Al final|Incluye|Agrega).*[Cc]alificaci[oó]n.*(\d.*\d|1.*5).*\.?', 
        '', 
        system_message, 
        flags=re.IGNORECASE | re.DOTALL
    ).strip()
    
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]
    
    temperature = prompt.config.get("temperature", 0)
    
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=temperature,
        messages=messages
    )
    
    output = res.choices[0].message.content
    
    # Actualizar generation con output
    generation.update(output=output)
    generation.end()
    
    # PASO 2: Evaluar respuesta en llamada separada (imparcial)
    print("⏳ Evaluando respuesta de forma independiente...")
    score, justification = evaluate_response(user_input, output, tone_name, span)
    
    if score:
        span.score(
            name="independent_evaluation",
            value=score,
            comment=f"Evaluación independiente: {justification}"
        )
    
    span.update(output=output)
    span.end()
    
    return output, score, justification

def main():
    print("\n" + "="*50)
    print("   📚 App de Conocimiento General con Langfuse")
    print("="*50)
    
    # Cargar prompts desde Langfuse
    print("\n⏳ Cargando prompts desde Langfuse...")
    try:
        prompts = {}
        for key, (prompt_name, display_name) in TONE_NAMES.items():
            prompts[key] = langfuse.get_prompt(prompt_name)
        print("✅ Prompts cargados correctamente.\n")
    except Exception as e:
        print(f"❌ Error al cargar prompts: {e}")
        print("💡 Asegúrate de ejecutar primero: python prompt_management/prompt_management_creation.py")
        return
    
    # Selección de tono
    print("=== Selecciona el tono de respuesta ===")
    for key, (_, display_name) in TONE_NAMES.items():
        print(f"{key}. {display_name}")
    
    choice = input("\nIngrese opción (1, 2 o 3): ").strip()
    
    if choice not in prompts:
        print("❌ Opción inválida. Saliendo.")
        return
    
    prompt = prompts[choice]
    tone_name = TONE_NAMES[choice][1]
    prompt_name = TONE_NAMES[choice][0]
    
    # Pregunta del usuario
    user_input = input("\n📝 Escribe tu pregunta de conocimiento general: ").strip()
    
    if not user_input:
        print("❌ No ingresaste ninguna pregunta. Saliendo.")
        return
    
    print(f"\n⏳ Generando respuesta en tono '{tone_name}'...")
    
    # Generar respuesta con evaluación independiente
    output, score, justification = generate_response(prompt, tone_name, prompt_name, user_input)
    
    print("\n" + "="*50)
    print("   🤖 Respuesta del modelo")
    print("="*50 + "\n")
    print(output)
    
    print("\n" + "-"*50)
    print("   📊 Evaluación Independiente")
    print("-"*50)
    if score:
        print(f"   Score: {score}/5")
        print(f"   Justificación: {justification}")
    else:
        print("   ⚠️ No se pudo obtener la evaluación.")
    
    # Asegurar que los datos se envíen a Langfuse
    langfuse.flush()
    
    print("\n✅ Traza enviada a Langfuse correctamente.")
    print("🔗 Revisa tu dashboard en https://cloud.langfuse.com\n")

if __name__ == "__main__":
    main()
