from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


def send_to_haiku(message, conversation_history): # функция отправки сообщения в API и получения ответа
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("HAIKU_API_KEY"), #ключ API из .env
    )
    completion = client.chat.completions.create(
        model="anthropic/claude-3-haiku", #модель, которую мы используем
        messages=[ #сообщения, которые мы отправляем
            {
                "role": "system", #Системное сообщение с промптом для бота
                "content": "You are a caring well-being specialist, answer in russian, do not use lists. Answer shortly if there is not much to say.",
            },
            *conversation_history, # добавляем историю сообщений
            {  # добавляем сообщение пользователя
                "role": "user",
                "content": message,
            },
        ],
    )
    answer = completion.choices[0].message.content.strip()
    return answer
