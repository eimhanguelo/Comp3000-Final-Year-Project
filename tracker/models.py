# models.py
from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords
from simple_history.utils import update_change_reason
from django.db.models.signals import post_save, post_delete  # Import post_delete here
from django.dispatch import receiver

class Tracker(models.Model):
    category = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tracker')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Tracker: {self.category}"

# Define a post-save signal for adding the change reason (for create and update)
@receiver(post_save, sender=Tracker)
def update_tracker_change_reason(sender, instance, created, **kwargs):
    if created:
        update_change_reason(instance, 'Tracker created')
    else:
        update_change_reason(instance, 'Tracker updated')

# Define a post-delete signal for adding the change reason (after delete)
@receiver(post_delete, sender=Tracker)
def update_tracker_delete_reason(sender, instance, **kwargs):
    # Log the change reason after the deletion
    update_change_reason(instance, 'Tracker deleted')
