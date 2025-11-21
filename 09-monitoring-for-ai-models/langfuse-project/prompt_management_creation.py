from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse(
    public_key="",
    secret_key="",
    base_url=""
)

client = openai.OpenAI(api_key="")

langfuse.create_prompt(
    name="story_summarization",
    prompt="Extract the key information from this text and return it in JSON format. Use the following schema: {{json_schema}}",
    config={
        "model":"gpt-4o-mini",
        "temperature": 0,
        "json_schema":{
            "main_character": "string (name of protagonist)",
            "key_content": "string (1 sentence)",
            "keywords": "array of strings",
            "genre": "string (genre of story)",
            "critic_review_comment": "string (write similar to a new york times critic)",
            "critic_score": "number (between 0 bad and 10 exceptional)"
        }
    },
    labels=["production"]
);


langfuse.create_prompt(
    name="explicacion_academica",
    prompt="Responde siempre en un tono académico y formal. Explica los conceptos con precisión, utiliza terminología técnica cuando sea apropiado y estructura la respuesta en secciones claras. Incluye definiciones, ejemplos y, cuando corresponda, comparaciones con conceptos relacionados. Al final de tu respuesta, incluye una sección titulada 'Calificación', donde evalúes la claridad, rigor conceptual y profundidad de tu propia explicación en una escala de 1 a 5.",
    config= {
        "temperature": 0
    },
    labels= ["production"]
);

langfuse.create_prompt(
  name="explicacion_amistosa",
  prompt="Responde de forma cercana, conversacional y sencilla. Usa ejemplos cotidianos y metáforas cuando sea útil. Mantén un tono amable y evita el exceso de tecnicismos salvo que sean necesarios para la claridad. Al final de tu respuesta, incluye una sección llamada 'Calificación', donde evalúes qué tan comprensible, amigable y útil fue tu explicación en una escala de 1 a 5.",
  config= {
    "temperature": 0.3
  },
  labels= ["production"]
);

langfuse.create_prompt(
  name="explicacion_directa",
  prompt="Responde de forma breve, precisa y orientada a la acción. No ofrezcas explicaciones extensas a menos que sean necesarias. Prioriza pasos concretos, buenas prácticas y advertencias relevantes. Al final de tu respuesta, incluye una sección titulada 'Calificación', donde evalúes qué tan eficiente, accionable y clara fue tu respuesta en una escala de 1 a 5.",
  config= {
    "temperature": 0
  },
  labels= ["production"]
);
