import os
import json
import httpx
from fastapi import HTTPException
from app.schemas.document_extraction import DocumentExtractionPayload
from app.services.extraction.base_provider import BaseExtractionProvider
from app.services.extraction.lenient_parser import lenient_parse_and_validate
from app.services.extraction.prompt_helper import get_extraction_prompt

class GroqExtractionProvider(BaseExtractionProvider):
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise HTTPException(
                status_code=500,
                detail="GROQ_API_KEY environment variable not configured."
            )
        self.model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        self.url = "https://api.groq.com/openai/v1/chat/completions"

    def extract(self, text: str, document_uuid: str) -> DocumentExtractionPayload:
        prompt = get_extraction_prompt(text, self.model, document_uuid)

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "response_format": {
                "type": "json_object"
            },
            "temperature": 0.1
        }

        try:
            r = httpx.post(self.url, headers=headers, json=payload, timeout=60.0)
            if r.status_code != 200:
                raise HTTPException(
                    status_code=502,
                    detail=f"Groq API returned error code {r.status_code}: {r.text}"
                )
            
            resp_json = r.json()
            text_response = resp_json['choices'][0]['message']['content'].strip()
            
            # Parse and validate against Pydantic schema using lenient parser
            return lenient_parse_and_validate(text_response, self.model, document_uuid)
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"HTTP connection error to Groq API: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to extract structured data using Groq: {str(e)}"
            )
