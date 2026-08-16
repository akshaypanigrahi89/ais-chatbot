from typing import Optional
from google.generativeai import GenerativeModel
from openai import OpenAI

from backend.config.settings import settings


class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL

    def get_llm(self):
        if self.provider == "gemini":
            return self._get_gemini_llm()
        else:
            return self._get_openai_llm()

    def _get_gemini_llm(self):
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=settings.GEMINI_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_output_tokens=settings.LLM_MAX_TOKENS
        )

    def _get_openai_llm(self):
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=self.model,
            api_key=settings.OPENAI_API_KEY,
            temperature=settings.LLM_TEMPERATURE,
            max_tokens=settings.LLM_MAX_TOKENS
        )

    async def generate(self, prompt: str, context: str = "") -> str:
        llm = self.get_llm()

        full_prompt = f"""Answer the following question based on the provided context.

Context:
{context}

Question: {prompt}

Answer:"""

        response = llm.invoke([full_prompt])
        return response.content


llm_service = LLMService()
