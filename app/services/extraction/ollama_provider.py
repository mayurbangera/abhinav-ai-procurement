import os
import json
import httpx
from fastapi import HTTPException
from app.schemas.document_extraction import DocumentExtractionPayload
from app.services.extraction.base_provider import BaseExtractionProvider
from app.services.extraction.lenient_parser import lenient_parse_and_validate
from app.services.extraction.prompt_helper import get_extraction_prompt

class OllamaExtractionProvider(BaseExtractionProvider):
    def __init__(self):
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
        self.url = f"{self.host}/api/chat"

    def extract(self, text: str, document_uuid: str) -> DocumentExtractionPayload:
        prompt = get_extraction_prompt(text, self.model, document_uuid)

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "format": "json",
            "stream": False,
            "options": {
                "temperature": 0.1
            }
        }

        try:
            r = httpx.post(self.url, json=payload, timeout=120.0)
            if r.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"Ollama server returned error code {r.status_code}: {r.text}"
                )
            
            resp_json = r.json()
            text_response = resp_json['message']['content'].strip()
            
            # Parse and validate against Pydantic schema using lenient parser
            return lenient_parse_and_validate(text_response, self.model, document_uuid)
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"HTTP connection error to Ollama: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract structured data using Ollama: {str(e)}"
            )
