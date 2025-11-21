from langfuse import Langfuse
from langfuse.openai import openai
import json

langfuse = Langfuse(
    public_key="",
    secret_key="",
    base_url=""
)

client = openai.OpenAI(api_key="")

prompt = langfuse.get_prompt("story_summarization")

#print(prompt.prompt)
#print(prompt.config)

json_schema_str = ', '.join([f"'{key}': {value}" for key, value in prompt.config["json_schema"].items()])
 
system_message = prompt.compile(json_schema=json_schema_str)

story = """
In a bustling city where the nighttime glittered with neon signs and the rush never calmed, lived a lonely cat named Whisper. Amidst the ceaseless clatter, Whisper discovered an abandoned hat one day. To her enigmatic surprise, this was no ordinary accessory; it had the unusual power to make her invisible to any onlooker.
Whisper, now carrying a peculiar power, started a journey that was unexpected. She became a benevolent spirit to the less fortunate, the homeless people who equally shared the cold nights with her. Nights that were once barren turned miraculous as warm meals mysteriously appeared to those who needed them most. No one could see her, yet her actions spoke volumes, turning her into an unsung hero in the hidden corners of the city.
As she carried on with her mysterious deed, she found an unanticipated reward. Joy started to kindle in her heart, born not from the invisibility, but from the result of her actions; the growing smiles on the faces of those she surreptitiously helped. Whisper might have remained unnoticed to the world, but amidst her secret kindness, she discovered her true happiness.
"""

messages = [
    {"role":"system","content": system_message},
    {"role":"user","content": story}
]
 
model = prompt.config["model"]
temperature = prompt.config["temperature"]
 
res = client.chat.completions.create(
  model = model,
  temperature = temperature,
  messages = messages,
  response_format = { "type": "json_object" },
  langfuse_prompt = prompt
)
 
res = json.loads(res.choices[0].message.content)

print(res)