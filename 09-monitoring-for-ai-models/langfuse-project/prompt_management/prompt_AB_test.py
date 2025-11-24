import random
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