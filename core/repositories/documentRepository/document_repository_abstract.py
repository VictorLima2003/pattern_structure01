from typing import List, Dict, Optional
from abc import ABC, abstractmethod

from core.dto.document_dto import DocumentDTO

class AbstractDocumentRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[DocumentDTO]:
        """Listar registros de Financial Instrument"""
        pass

    @abstractmethod
    def get_by_id(self) -> Optional[DocumentDTO]:
        """Listar registros de Financial Instrument"""
        pass

    @abstractmethod
    def get_by_contract_id(self) -> Optional[DocumentDTO]:
        """Listar registros de Financial Instrument"""
        pass