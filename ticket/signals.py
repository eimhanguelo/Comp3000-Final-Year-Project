from django.db.models.signals import post_save
# from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import EAssign, Eticket, ESolve


# @receiver(post_save, sender=Eticket)
# def create_eassign(sender, instance, created, **kwargs):
#     if created:
#         EAssign.objects.create(eticket_id=instance)
#
#
# @receiver(post_save, sender=Eticket)
# def save_eassign(sender, instance, **kwargs):
#     instance.eticket_id.save()


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()

