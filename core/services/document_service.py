from core.dto.document_dto import DocumentDTO
from typing import Optional
from core.repositories.documentRepository.document_repository_abstract import AbstractDocumentRepository

class DocumentService:
    def __init__(self, documentRepository: AbstractDocumentRepository):
        self.documentRepository = documentRepository

    def create_document(self, document):
        pass

    def get_document(self, document_id: int) -> Optional[DocumentDTO]:
        if not document_id:
            return None

        document = self.documentRepository.get_by_id(document_id)

        if not document:
            print('Documento não encontrado.')
            return None

        return document

    def get_document_contract(self, contract_id: int) -> Optional[DocumentDTO]:
        if not contract_id:
            return None

        document = self.documentRepository.get_by_contract_id(contract_id)

        if not document:
            print('Documento não encontrado.')
            return None

        return document