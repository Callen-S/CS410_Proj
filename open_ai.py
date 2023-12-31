import asyncio
from openai import OpenAI

def calc_vibes(text, term):
  client = OpenAI()


  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": f"You are a helpful assistant. You will assess text given on how positive is it in regards to {term} and return a score from 1 to 10 in which 10 is good and 1 is bad. Only return a number with not other context"},
      {"role": "user", "content": text},

    ]
  )
  return response.choices[0].message.content