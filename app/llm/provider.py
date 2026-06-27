from ollama import chat
from app.config import model_name , model_temperature , model_context_window
from app.prompts.summarizer import SUMMARY_PROMPT

class LLMProvider:

    @staticmethod
    def summarize(text: str):

        prompt = SUMMARY_PROMPT.format(text=text)

        response = chat(
            model=model_name,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            options={
                "temperature": model_temperature,
                "num_ctx": model_context_window,
            }
        )

        return response['message']['content']