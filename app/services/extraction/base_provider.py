from abc import ABC, abstractmethod
from app.schemas.document_extraction import DocumentExtractionPayload

class BaseExtractionProvider(ABC):
    @abstractmethod
    def extract(self, text: str, document_uuid: str) -> DocumentExtractionPayload:
        """
        Extract structured data from the raw text of a quotation.
        
        Args:
            text          : The raw text extracted from the document.
            document_uuid : The ingestion UUID of the document.
            
        Returns:
            DocumentExtractionPayload: Structured payload matching the Gold Standard Schema.
        """
        pass
