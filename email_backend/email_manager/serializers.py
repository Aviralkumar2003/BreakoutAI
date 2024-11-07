# email_manager/serializers.py
from rest_framework import serializers
from .models import EmailData, ScheduledEmail

class EmailDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailData
        fields = '__all__'

class ScheduledEmailSerializer(serializers.ModelSerializer):
    email_data = EmailDataSerializer(read_only=True)

    class Meta:
        model = ScheduledEmail
        fields = '__all__'
