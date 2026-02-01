import pandas as pd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UploadHistory
from .serializers import UploadHistorySerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def upload_history(request):

    last_five = UploadHistory.objects.order_by("-uploaded_at")[:5]
    serializer = UploadHistorySerializer(last_five, many=True)
    return Response(serializer.data)
