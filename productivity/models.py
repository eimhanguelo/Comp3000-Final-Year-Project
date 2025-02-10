from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class OpportunityTag(models.Model):
    author = models.ForeignKey(User, related_name='opportunity_tag_author', on_delete=models.CASCADE)
    idea_giver = models.ForeignKey(User, related_name='opportunity_tag_idea_giver',  on_delete=models.CASCADE)
    supervisor = models.ForeignKey(User, related_name='opportunity_tag_supervisor', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=253)
    description = models.TextField()
    benefits = models.TextField()
    attachment = models.FileField(upload_to='productivity', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'OPP_TAG-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('opportunity-tag-detail', kwargs={'pk': self.pk})


class OpportunityTagAdmin(models.Model):
    opportunity_tag = models.OneToOneField(OpportunityTag, related_name='opportunity_tag', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    OPPORTUNITY_TAG_STATUS = (
        ('On Review', 'On Review'),
        ('Nominated for Presentation', 'Nominated for Presentation'),
        ('Nominated for Award', 'Nominated for Award'),
    )
    status = models.CharField(max_length=50, choices=OPPORTUNITY_TAG_STATUS)
    comments = models.TextField()
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.opportunity_tag} acknowledged by {self.admin}'


class ObservationTag(models.Model):
    author = models.ForeignKey(User, related_name='observation_tag_author', on_delete=models.CASCADE)
    title = models.CharField(max_length=253)
    description = models.TextField()
    observation_date = models.DateField()
    attachment = models.FileField(upload_to='productivity', null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'OBSN_TAG-{self.id}/{self.author.id}/{self.author.profile.emp_id}'

    def get_absolute_url(self):
        return reverse('observation-tag-detail', kwargs={'pk': self.pk})


class ObservationTagAdmin(models.Model):
    observation_tag = models.OneToOneField(ObservationTag, related_name='observation_tag', on_delete=models.CASCADE)
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    OBSERVATION_TAG_STATUS = (
        ('On Review', 'On Review'),
        ('Informed Responsible Person', 'Informed Responsible Person'),
        ('Observation Resolved', 'Observation Resolved'),
    )
    status = models.CharField(max_length=100, choices=OBSERVATION_TAG_STATUS)
    comments = models.TextField()
    date_signed = models.DateTimeField(auto_now_add=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.observation_tag} acknowledged by {self.admin}'
