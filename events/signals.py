from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Event
from .seat_generator import generate_seats_for_event


@receiver(post_save, sender=Event)
def create_seats_after_event_created(sender, instance, created, **kwargs):
    if created:
        generate_seats_for_event(instance)