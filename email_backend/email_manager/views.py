# email_manager/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
import pandas as pd
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import EmailLog
from rest_framework import viewsets
from .models import EmailData
from .serializers import EmailDataSerializer
from .models import ScheduledEmail
from .serializers import ScheduledEmailSerializer

class DataUploadView(APIView):
    def post(self, request):
        try:
            # Handle CSV file upload
            csv_file = request.FILES['file']
            df = pd.read_csv(csv_file)
            # Validate CSV format, headers, etc.
            if not all(column in df.columns for column in ['email', 'company_name', 'location']):
                raise ValidationError("Missing required columns")
            # Further data processing logic here
            return Response({"columns": df.columns.tolist()}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# email_manager/views.py


class DataUploadView(APIView):
    def get(self, request):
        try:
            credentials = Credentials.from_service_account_file('path/to/credentials.json')
            sheet_service = build('sheets', 'v4', credentials=credentials)
            # Fetch the spreadsheet data (for example, to display a list of emails)
            sheet = sheet_service.spreadsheets()
            result = sheet.values().get(spreadsheetId='your_spreadsheet_id', range='Sheet1!A1:D10').execute()
            values = result.get('values', [])
            return Response(values, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# email_manager/views.py


class OAuth2CallbackView(APIView):
    def get(self, request):
        # Handle the OAuth2 callback and save credentials to the database
        try:
            flow = Flow.from_client_secrets_file(
                'path/to/client_secret.json',
                scopes=['https://www.googleapis.com/auth/gmail.send'],
                redirect_uri='http://localhost:8000/api/oauth2callback'
            )
            credentials = flow.fetch_token(authorization_response=request.build_absolute_uri())
            # Store credentials in the database for future use
            return Response({"message": "Email account connected."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class AnalyticsView(APIView):
    def get(self, request):
        # Fetch the required data from the database
        total_sent = EmailLog.objects.count()  # Total number of emails sent
        emails_failed = EmailLog.objects.filter(status='failed').count()  # Emails failed to send
        emails_delivered = EmailLog.objects.filter(status='delivered').count()  # Emails successfully delivered
        emails_opened = EmailLog.objects.filter(status='opened').count()  # Emails that have been opened
        
        # Calculate response rate
        response_rate = emails_delivered / total_sent if total_sent else 0

        # Return the dynamically fetched data
        stats = {
            "total_sent": total_sent,
            "emails_failed": emails_failed,
            "emails_delivered": emails_delivered,
            "emails_opened": emails_opened,
            "response_rate": response_rate,
        }
        return Response(stats)

class EmailDataViewSet(viewsets.ModelViewSet):
    queryset = EmailData.objects.all()
    serializer_class = EmailDataSerializer

class ScheduledEmailViewSet(viewsets.ModelViewSet):
    queryset = ScheduledEmail.objects.all()
    serializer_class = ScheduledEmailSerializer