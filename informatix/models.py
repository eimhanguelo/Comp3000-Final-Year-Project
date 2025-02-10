from operator import mod
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

from django.db import models
import datetime
class Roster(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    supervisor = models.ForeignKey(
        User, related_name='supervised_rosters', on_delete=models.SET_NULL, null=True, blank=True
    )
    month = models.CharField(max_length=9, choices=[
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ], default=datetime.date.today().strftime('%B'))

    class Meta:
        verbose_name_plural = "IT Duty Roster Plan"

    def __str__(self):
        return f'{self.name} ({self.month} {datetime.date.today().year})'

class ShiftPlan(models.Model):
    roster = models.ForeignKey(Roster, related_name='roster', on_delete=models.CASCADE)
    engineer = models.ForeignKey(User, related_name='shift_engineer', on_delete=models.CASCADE)
    DUTY_TYPE = (
        ('G', 'G'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('On-Call', 'On-Call'),
        ('Day-Off', 'Day-Off'),
    )
    sat = MultiSelectField(max_length=20, choices=DUTY_TYPE)
    sun = MultiSelectField(max_length=20, choices=DUTY_TYPE)
    mon = MultiSelectField(max_length=20, choices=DUTY_TYPE)
    tue = MultiSelectField(max_length=20, choices=DUTY_TYPE)
    wed = MultiSelectField(max_length=20, choices=DUTY_TYPE)
    thu = MultiSelectField(max_length=20, choices=DUTY_TYPE)
    fri = MultiSelectField(max_length=20, choices=DUTY_TYPE)

    def __str__(self):
        return f'Roster :{self.roster}---Engineer :{self.engineer}'

