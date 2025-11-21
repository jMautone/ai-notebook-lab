from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse(
    public_key="",
    secret_key="",
    base_url=""
)

client = openai.OpenAI(api_key="")

prompts = [
    "Explica RAG en dos frases.",
    "Genera una receta de pasta con instrucciones detalladas.",
    "¿Cuál es la capital de Uruguay?",
    "¿Qué es un embedding?",
    "Escribe un poema corto.",
    "¿Quién gana el clásico?"
    #"¿Cuánto oro se necesitaría para recubrir la Estatua de la Libertad con una capa de 1 mm?"
]

for p in prompts:
    
    result = client.responses.create(
        model="gpt-4o-mini",
        input=p,
    )

    #result = client.responses.create(
    #    model="gpt-5.1",
    #    input=p,
    #    reasoning={ "effort": "medium" },
    #)
    print(result.output_text)

