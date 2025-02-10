from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LanInstrument, LanInstrumentIT

#
# @receiver(post_save, sender=LanInstrument)
# def create_laninstrumentit(sender, instance, created, **kwargs):
#     if created:
#         LanInstrumentIT.objects.create(laninstrument=instance)
#
#
# @receiver(post_save, sender=LanInstrument)
# def save_laninstrumentit(sender, instance, **kwargs):
#     instance.laninstrumentit.save()