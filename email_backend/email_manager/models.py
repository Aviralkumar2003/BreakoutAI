from django.db import models

class EmailData(models.Model):
    email = models.EmailField()
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    products = models.TextField(null=True, blank=True)

class ScheduledEmail(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Sent', 'Sent'),
        ('Failed', 'Failed'),
    ]
    email_data = models.ForeignKey(EmailData, on_delete=models.CASCADE)
    scheduled_time = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    class Meta:
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['scheduled_time']),
        ]


class EmailLog(models.Model):
    # Fields for the EmailLog model
    subject = models.CharField(max_length=255)
    recipient = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.subject