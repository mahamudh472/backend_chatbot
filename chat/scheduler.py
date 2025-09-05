from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from chat.models import ChatMessage
from datetime import timedelta

def cleanup_old_messages():
    """
    Delete chat messages older than 30 days.
    """
    threshold_date = timezone.now() - timedelta(days=30)
    old_messages = ChatMessage.objects.filter(timestamp__lt=threshold_date)
    count = old_messages.count()
    old_messages.delete()
    print(f"Deleted {count} old chat messages.")

def send_verification_emails():
    """
    Placeholder function to send verification emails.
    """
    print("Sending verification emails to users... (functionality not implemented)")


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Schedule the cleanup job to run daily at midnight
    scheduler.add_job(
        cleanup_old_messages,
        'interval',
        days=1,
        id='cleanup_old_messages',
        replace_existing=True
    )


    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...")