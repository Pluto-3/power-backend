from django.urls import path
from .views import IngestReadingView, DeviceStatusView, DeviceHistoryView, DeviceAlertsView

urlpatterns = [
    path('readings/', IngestReadingView.as_view(), name='ingest-reading'),
    path('devices/<uuid:device_id>/status/', DeviceStatusView.as_view(), name='device-status'),
    path('devices/<uuid:device_id>/history/', DeviceHistoryView.as_view(), name='device-history'),
    path('devices/<uuid:device_id>/alerts/', DeviceAlertsView.as_view(), name='device-alerts'),
]