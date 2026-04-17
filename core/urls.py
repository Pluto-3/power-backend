from django.urls import path
from .views import IngestReadingView

urlpatterns = [
    path('readings/', IngestReadingView.as_view(), name='ingest-reading'),
]