import time

from openai import OpenAI, APIError, APITimeoutError, APIConnectionError

from app.config import OPENAI_API_KEY


client = OpenAI(
    api_key=OPENAI_API_KEY,
    timeout=20.0,
)


def ask_llm(question: str):
    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = client.responses.create(
                model="gpt-5.6-luna",
                input=question,
            )

            return {
                "answer": response.output_text,
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens,
                "total_tokens": response.usage.total_tokens,
            }

        except (APITimeoutError, APIConnectionError, APIError):
            if attempt == max_retries - 1:
                raise

            time.sleep(1 * (attempt + 1))
