from django.http import JsonResponse
from django.views.decorators.http import require_GET
from core.factories.document_factory import DocumentFactory

@require_GET
def get_document_view(request, document_id):
    factory = DocumentFactory()
    document_data = factory.execute_get_document_by_contract(document_id)

    if document_data is not None:
        document_data = document_data[1].to_dict()

    return JsonResponse(document_data, safe=False)
