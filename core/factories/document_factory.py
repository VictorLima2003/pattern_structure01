from core.repositories.documentRepository.document_repository_django import DocumentRepository
from core.services.document_service import DocumentService


class DocumentFactory:
    def __init__(self):
        # self.session = next(get_db())
        self.documentRepository = DocumentRepository()

    def execute_get_document(self, document_id: int):
        documentService = DocumentService(self.documentRepository)
        response = documentService.get_document(document_id)
        return response

    def execute_get_document_by_contract(self, contract_id: int):
        documentService = DocumentService(self.documentRepository)
        response = documentService.get_document_contract(contract_id)
        return response
