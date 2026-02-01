from django.urls import path
from .views import upload_csv, upload_history, download_pdf_report

urlpatterns = [
    path("upload/", upload_csv),
    path("history/", upload_history),
path("report/pdf/<int:history_id>/", download_pdf_report),

]
