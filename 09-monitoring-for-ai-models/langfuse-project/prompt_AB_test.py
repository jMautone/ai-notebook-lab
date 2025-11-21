import random

from langfuse import Langfuse
from langfuse.openai import openai

langfuse = Langfuse(
    public_key="",
    secret_key="",
    base_url=""
)

client = openai.OpenAI(api_key="")

prompt_a = langfuse.get_prompt("itinerary_planner_experiment", label="prod-a")
prompt_b = langfuse.get_prompt("itinerary_planner_experiment", label="prod-b")
 
for i in range(10):
    selected_prompt = random.choice([prompt_a, prompt_b])

    system_message = selected_prompt.prompt

    messages = [
        {"role":"system","content": system_message},
        {"role":"user","content": "Quiero recomendaciones para mi viaje a Italia"}
    ]
     
     
    res = client.chat.completions.create(
      model = "gpt-4o-mini",
      messages = messages,
      langfuse_prompt = selected_prompt
    )
     
    res = res.choices[0].message.content

    print(f"Run {i+1}: {res}\n")