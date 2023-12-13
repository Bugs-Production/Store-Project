from celery import shared_task
import uuid
from datetime import timedelta
from django.utils.timezone import now
from .models import EmailVerification, User


@shared_task
def send_verification_email(user_id):
    user = User.objects.get(id=user_id)
    code = uuid.uuid4()
    expiration = timedelta(hours=48) + now()
    record = EmailVerification.objects.create(code=code, user=user, expiration=expiration)
    record.send_verification_email()
