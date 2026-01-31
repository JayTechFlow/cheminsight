from django.contrib import admin
from .models import UploadHistory

@admin.register(UploadHistory)
class UploadHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "file_name",
        "uploaded_at",
        "total_equipment",
    )
