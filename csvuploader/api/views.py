import csv
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from .models import User

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework.parsers import MultiPartParser

class CSVUploadView(APIView):
    parser_classes = [MultiPartParser]
    @swagger_auto_schema(
        operation_description="Upload a CSV file with user data.",
        manual_parameters=[
            openapi.Parameter(
                name="file",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="CSV file to upload"
            )
        ],
        responses={
            200: openapi.Response(
                description="Upload result",
                examples={
                    "application/json": {
                        "saved": 2,
                        "rejected": 1,
                        "errors": [
                            {"row": 3, "errors": {"email": ["Duplicate email, skipped."]}, "data": {"name": "John", "email": "john@example.com", "age": "30"}}
                        ]
                    }
                }
            ),
            400: openapi.Response(description="Bad request")
        }
    )
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)
        if not file.name.lower().endswith('.csv'):
            return Response({"error": "Only .csv files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        saved_count = 0
        rejected_count = 0
        errors = []
        seen_emails = set(User.objects.values_list('email', flat=True))

        for idx, row in enumerate(reader, start=2):  # start=2 to account for header row
            row = {k.strip(): v.strip() for k, v in row.items()}
            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                if email in seen_emails:
                    rejected_count += 1
                    errors.append({
                        'row': idx,
                        'errors': {'email': ['Duplicate email, skipped.']},
                        'data': row
                    })
                else:
                    serializer.save()
                    seen_emails.add(email)
                    saved_count += 1
            else:
                rejected_count += 1
                errors.append({
                    'row': idx,
                    'errors': serializer.errors,
                    'data': row
                })

        return Response({
            'saved': saved_count,
            'rejected': rejected_count,
            'errors': errors
        }, status=status.HTTP_200_OK)
