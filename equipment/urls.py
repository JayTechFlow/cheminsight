from django.urls import path
from .views import UploadCSV, DatasetHistory

urlpatterns = [
    path('upload/', UploadCSV.as_view(), name='upload-csv'),
    path('history/', DatasetHistory.as_view(), name='dataset-history'),
]
