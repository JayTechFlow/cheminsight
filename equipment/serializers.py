from rest_framework import serializers
from .models import UploadHistory

class UploadHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadHistory
        fields = [
            "id",
            "file_name",
            "uploaded_at",
            "total_equipment",
            "avg_flowrate",
            "avg_pressure",
            "avg_temperature",
            "type_distribution",
        ]
