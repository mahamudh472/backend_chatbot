from django.core.signals import request_started
from django.dispatch import receiver

schaduler_started = False

@receiver(request_started)
def start_scheduler(sender, **kwargs):
    global schaduler_started
    if not schaduler_started:
        from . import scheduler
        scheduler.start()
        schaduler_started = True