from typing import List, Optional
from core.dto.document_dto import DocumentDTO
from core.repositories.documentRepository.document_repository_abstract import AbstractDocumentRepository
from common.models import Document

class DocumentRepository(AbstractDocumentRepository):
    def _to_dto(self, document: Document) -> DocumentDTO:
        return DocumentDTO(
            id=document.id,
            name=document.name,
            file_extension=document.file_extension,
            type=document.type,
            content=document.content,
            info=document.info
        )

    def get_all(self) -> List[DocumentDTO]:
        docs = Document.objects.all()
        return [self._to_dto(doc) for doc in docs]

    def get_by_id(self, document_id: int) -> Optional[DocumentDTO]:
        doc = Document.objects.filter(id=document_id).first()
        return self._to_dto(doc) if doc else None

    def get_by_contract_id(self, contract_id: int) -> List[DocumentDTO]:
        docs = Document.objects.filter(info__contract_id=contract_id)
        return [self._to_dto(doc) for doc in docs]