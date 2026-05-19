from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from typing import List, Dict
import requests

load_dotenv()

class ExtractorService:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai") # "openai" or "ollama"
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")

    async def _call_llm(self, prompt: str, json_mode: bool = True) -> str:
        if self.provider == "openai":
            response = self.openai_client.chat.completions.create(
                model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" } if json_mode else None
            )
            return response.choices[0].message.content
        else:
            # Ollama implementation
            payload = {
                "model": os.getenv("OLLAMA_MODEL", "llama3"),
                "prompt": prompt,
                "stream": False,
                "format": "json" if json_mode else ""
            }
            resp = requests.post(self.ollama_url, json=payload)
            return resp.json().get("response", "")

    async def extract_facts(self, text: str) -> List[str]:
        """Distills raw text into atomic facts."""
        prompt = f"""
        Extract the atomic facts from the following text. 
        Each fact should be a single, standalone sentence.
        Text: {text}
        
        Example Output:
        {{"facts": ["Nishant is the author of WinOptimizer.", "The project uses Python."]}}
        """
        content = await self._call_llm(prompt)
        data = json.loads(content)
        return data.get("facts", [])

    async def extract_entities(self, text: str) -> List[Dict]:
        """Identifies entities and their relationships."""
        prompt = f"""
        Identify entities and their relationships from the following text.
        Text: {text}
        
        Output JSON format:
        {{
            "entities": [{{ "name": "Nishant", "type": "PERSON" }}],
            "relations": [{{ "source": "Nishant", "target": "WinOptimizer", "type": "OWNS" }}]
        }}
        """
        content = await self._call_llm(prompt)
        return json.loads(content)
        
    async def get_embedding(self, text: str) -> List[float]:
        """Generates embeddings using OpenAI (or local via sentence-transformers if needed)."""
        # For now, sticking with OpenAI embeddings for high quality, 
        # but could be swapped for local.
        response = self.openai_client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
