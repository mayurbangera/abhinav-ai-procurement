import os
from app.services.extraction.base_provider import BaseExtractionProvider
from app.services.extraction.gemini_provider import GeminiExtractionProvider
from app.services.extraction.groq_provider import GroqExtractionProvider
from app.services.extraction.ollama_provider import OllamaExtractionProvider

def get_extraction_provider() -> BaseExtractionProvider:
    """
    Factory function to retrieve the configured AI extraction provider.
    Reads the EXTRACTION_PROVIDER environment variable.
    Supported values: 'gemini' (default), 'groq', 'ollama'.
    """
    provider_name = os.getenv("EXTRACTION_PROVIDER", "gemini").lower()
    
    if provider_name == "gemini":
        return GeminiExtractionProvider()
    elif provider_name == "groq":
        return GroqExtractionProvider()
    elif provider_name == "ollama":
        return OllamaExtractionProvider()
    else:
        # Fall back to Gemini if unknown
        return GeminiExtractionProvider()
