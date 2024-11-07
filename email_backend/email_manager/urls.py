from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailDataViewSet, ScheduledEmailViewSet
from .models import EmailLog
router = DefaultRouter()
router.register(r'email_data', EmailDataViewSet)
router.register(r'scheduled_email', ScheduledEmailViewSet)
from .views import AnalyticsView

urlpatterns = [
    path('', include(router.urls)),
    path('analytics/', AnalyticsView.as_view(), name='analytics'),
]
