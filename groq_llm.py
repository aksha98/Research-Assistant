
import requests
import os
from langchain.llms.base import BaseLLM
from langchain_core.outputs import LLMResult, Generation
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

class GroqLLM(BaseLLM):
    def _generate(self, prompts: List[str], stop: Optional[List[str]] = None) -> LLMResult:
        api_key = os.getenv("GROQ_API_KEY")
        prompt = prompts[0]
        print(f"[GROQ] Prompt:\n{prompt}\n")

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.7
            },
        )

        if response.status_code == 200:
            result = response.json()["choices"][0]["message"]["content"]
            return LLMResult(generations=[[Generation(text=result)]])
        else:
            error_text = f"Error: {response.status_code} - {response.text}"
            return LLMResult(generations=[[Generation(text=error_text)]])

    @property
    def _llm_type(self) -> str:
        return "groq"
