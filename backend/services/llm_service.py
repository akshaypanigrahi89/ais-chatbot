from typing import Optional
from backend.config.settings import settings


class LLMService:
    def __init__(self):
        self._llm = None

    def get_llm(self):
        if self._llm is not None:
            return self._llm

        if settings.LLM_PROVIDER == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI
            self._llm = ChatGoogleGenerativeAI(
                model=settings.LLM_MODEL,
                google_api_key=settings.GEMINI_API_KEY,
                temperature=settings.LLM_TEMPERATURE,
                max_output_tokens=settings.LLM_MAX_TOKENS
            )
        else:
            from langchain_openai import ChatOpenAI
            self._llm = ChatOpenAI(
                model=settings.LLM_MODEL,
                api_key=settings.OPENAI_API_KEY,
                temperature=settings.LLM_TEMPERATURE,
                max_tokens=settings.LLM_MAX_TOKENS
            )

        return self._llm

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
