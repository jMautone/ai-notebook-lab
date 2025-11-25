from langfuse import Langfuse
from langfuse.openai import openai
import os
from dotenv import load_dotenv

load_dotenv()

langfuse = Langfuse(
    public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
    secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
    base_url=os.environ.get("LANGFUSE_BASE_URL")
)

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

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

