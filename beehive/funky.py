from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


def send_to_haiku(message):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("HAIKU_API_KEY"),
    )
    completion = client.chat.completions.create(
        model="anthropic/claude-3-haiku",
        messages=[
            {
                "role": "system",
                "content": "You are a caring well-being specialist, answer in russian, do not use lists. Your message should be 200 tokens in size.",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
    )
    answer = completion.choices[0].message.content.strip()
    return answer
