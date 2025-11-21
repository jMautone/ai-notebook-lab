from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse(
    public_key="",
    secret_key="",
    base_url=""
)

client = openai.OpenAI(api_key="")

prompt_academico = langfuse.get_prompt("explicacion_academica")
prompt_amistoso = langfuse.get_prompt("explicacion_amistosa")
prompt_directo = langfuse.get_prompt("explicacion_directa")

PROMPTS = {
    "1": prompt_academico,
    "2": prompt_amistoso,
    "3": prompt_directo
}

print("=== Selecciona el tono de respuesta ===")
print("1. Académico-formal")
print("2. Conversacional-amistoso")
print("3. Directo y pragmático")

choice = input("Ingrese opción (1, 2 o 3): ").strip()

if choice not in PROMPTS:
    print("Opción inválida. Saliendo.")
    exit()

prompt = PROMPTS[choice]

system_message = prompt.prompt

user_input = input("\nEscribe tu pregunta: ")

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_input}
]

temperature = prompt.config.get("temperature", 0)

res = client.chat.completions.create(
    model="gpt-4o-mini",
    temperature=temperature,
    messages=messages,
    langfuse_prompt=prompt
)

output = res.choices[0].message.content

print("\n=== Respuesta del modelo ===\n")
print(output)
