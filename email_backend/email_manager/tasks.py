# email_manager/tasks.py
import logging
from celery import shared_task
from .utils import send_email_via_sendgrid
from django.conf import settings
from time import sleep

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def send_scheduled_email(self, email_data, template):
    try:
        subject = f"Email to {email_data.company_name}"
        content = generate_email_content(template, email_data.__dict__)
        send_email_via_sendgrid(email_data['email'], 'Subject', content)
        return {"status": "Sent"}
    except Exception as e:
        logger.error(f"Error sending email: {str(e)}")
        raise self.retry(exc=e, countdown=60)  # Retry after 1 minute

@shared_task
def schedule_emails(email_list, template, throttle_rate):
    for email_data in email_list:
        send_scheduled_email.delay(email_data, template)
        sleep(throttle_rate)  # Throttle as per user setting
