from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(subject, message, recipient_list):
    print(f"[TASK START] Sending email to {recipient_list}")
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=False)
        print("[TASK SUCCESS] Email sent.")
    except Exception as e:
        print(f"[TASK ERROR] {e}")