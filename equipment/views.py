import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UploadHistory
from .serializers import UploadHistorySerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


@api_view(["POST"])
def upload_csv(request):

    file = request.FILES.get("file")

    if not file:
        return Response({"error": "No file uploaded"}, status=400)

    df = pd.read_csv(file)

    total_equipment = len(df)
    avg_flowrate = df["Flowrate"].mean()
    avg_pressure = df["Pressure"].mean()
    avg_temperature = df["Temperature"].mean()

    type_distribution = df["Type"].value_counts().to_dict()

    history = UploadHistory.objects.create(
        file_name=file.name,
        total_equipment=total_equipment,
        avg_flowrate=avg_flowrate,
        avg_pressure=avg_pressure,
        avg_temperature=avg_temperature,
        type_distribution=type_distribution,
    )

    serializer = UploadHistorySerializer(history)
    return Response(serializer.data)


@api_view(["GET"])
def upload_history(request):

    last_five = UploadHistory.objects.order_by("-uploaded_at")[:5]
    serializer = UploadHistorySerializer(last_five, many=True)
    return Response(serializer.data)
@api_view(["GET"])
def download_pdf_report(request, history_id):
    history = get_object_or_404(UploadHistory, id=history_id)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="{history.file_name}_summary.pdf"'
    )

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    y = height - 50

    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y, "ChemInsight – Equipment Summary Report")
    y -= 30

    p.setFont("Helvetica", 11)
    p.drawString(50, y, f"File Name: {history.file_name}")
    y -= 18
    p.drawString(50, y, f"Uploaded At: {history.uploaded_at}")
    y -= 25

    p.drawString(50, y, f"Total Equipment: {history.total_equipment}")
    y -= 18
    p.drawString(50, y, f"Average Flowrate: {round(history.avg_flowrate, 2)}")
    y -= 18
    p.drawString(50, y, f"Average Pressure: {round(history.avg_pressure, 2)}")
    y -= 18
    p.drawString(50, y, f"Average Temperature: {round(history.avg_temperature, 2)}")
    y -= 25

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, y, "Equipment Type Distribution:")
    y -= 18

    p.setFont("Helvetica", 11)
    for eq_type, count in history.type_distribution.items():
        p.drawString(70, y, f"{eq_type}: {count}")
        y -= 16

    p.showPage()
    p.save()
    return response
