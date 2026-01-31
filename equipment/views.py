import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Dataset

class UploadCSV(APIView):
    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {"error": "No file uploaded"},
                status=status.HTTP_400_BAD_REQUEST
            )

        file = request.FILES['file']

        try:
            df = pd.read_csv(file)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        summary = {
            "total_equipment": int(len(df)),
            "avg_flowrate": float(df["Flowrate"].mean()),
            "avg_pressure": float(df["Pressure"].mean()),
            "avg_temperature": float(df["Temperature"].mean()),
            "type_distribution": df["Type"].value_counts().to_dict()
        }

        Dataset.objects.create(
            total_equipment=summary["total_equipment"],
            avg_flowrate=summary["avg_flowrate"],
            avg_pressure=summary["avg_pressure"],
            avg_temperature=summary["avg_temperature"]
        )

        # Keep only last 5 datasets
        if Dataset.objects.count() > 5:
            Dataset.objects.order_by('uploaded_at').first().delete()

        return Response(summary, status=status.HTTP_200_OK)
