from typing import List, Optional
from sqlalchemy.orm import Session
from common.database.sql_alchemy.models import Document  # Modelo SQLAlchemy
from core.dto.document_dto import DocumentDTO
from core.repositories.documentRepository.document_repository_abstract import AbstractDocumentRepository

class DocumentRepository(AbstractDocumentRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[DocumentDTO]:
        documents = self.session.query(Document).all()
        return [
            DocumentDTO(
                id=doc.id,
                name=doc.name,
                file_extension=doc.file_extension,
                type=doc.type.value,
                content=doc.content,
                info=doc.info,
            )
            for doc in documents
        ]

    def get_by_id(self, document_id: int) -> Optional[DocumentDTO]:
        document = self.session.query(Document).filter(Document.id == document_id).first()
        if not document:
            return None
        return DocumentDTO(
            id=document.id,
            name=document.name,
            file_extension=document.file_extension,
            type=document.type.value,
            content=document.content,
            info=document.info,
        )

    def get_by_contract_id(self, contract_id: str) -> Optional[DocumentDTO]:
        document = self.session.query(Document).filter(Document.info['contract_id'].astext == contract_id).first()
        if not document:
            return None
        return DocumentDTO(
            id=document.id,
            name=document.name,
            file_extension=document.file_extension,
            type=document.type.value,
            content=document.content,
            info=document.info,
        )
