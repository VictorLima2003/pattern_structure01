from django.urls import path
from .views import get_document_view

urlpatterns = [
    path('document/<int:document_id>/', get_document_view, name='get-document'),
]