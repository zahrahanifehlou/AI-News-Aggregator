from ollama import chat
from app.config import model_name, model_temperature, model_context_window


class LLMProvider:

    @staticmethod
    def _call_llm(prompt: str, temperature: float = None) -> str:
        """Internal helper to call Ollama"""
        temp = temperature if temperature is not None else model_temperature

        response = chat(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            options={
                "temperature": temp,
                "num_ctx": model_context_window,
            }
        )
        return response['message']['content'].strip()

    @staticmethod
    def summarize(text: str) -> str:
        """Summarize article content"""
        if not text or not text.strip():
            return ""
        
        from app.prompts.summarizer import SUMMARY_PROMPT
        prompt = SUMMARY_PROMPT.format(text=text)
        return LLMProvider._call_llm(prompt)

    @staticmethod
    def generate(prompt: str, temperature: float = None) -> str:
        """General text generation"""
        if not prompt:
            return ""
        return LLMProvider._call_llm(prompt, temperature)

    @staticmethod
    def classify(prompt: str) -> str:
        """Classification with lower temperature for better JSON output"""
        return LLMProvider._call_llm(prompt, temperature=0.1)