import os

from dotenv import load_dotenv
from litellm import completion


load_dotenv()


def generate(messages):

    response = completion(
        model=os.getenv("LLM_MODEL"),

        messages=messages,
    )

    return response.choices[0].message.content