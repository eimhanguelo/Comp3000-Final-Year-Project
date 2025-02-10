from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import datetime
from simple_history.models import HistoricalRecords


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique names for departments
    history = HistoricalRecords()
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default


class Position(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique names for positions
    history = HistoricalRecords()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique names for locations
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default


class Floor(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Ensure unique names for floors
    history = HistoricalRecords()

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['id']  # Orders by id in ascending order by default


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    emp_id = models.CharField(max_length=20, null=True, blank=True, unique=True)  # Ensure unique employee IDs
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    floor = models.ForeignKey(Floor, on_delete=models.SET_NULL, null=True, blank=True)
    emp_join_date = models.DateField(default=datetime.date.today)
    phone = models.CharField(max_length=100, null=True, blank=True, unique=True)  # Ensure unique phone numbers
    ext = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics/', null=True, blank=True)
    is_hr = models.BooleanField(default=False)
    is_accountant = models.BooleanField(default=False)
    is_verifier_it = models.BooleanField(default=False)
    is_hod_it = models.BooleanField(default=False)
    is_productivity_admin = models.BooleanField(default=False)
    recom_permission_departments = models.ManyToManyField(Department, related_name='recom_profiles', blank=True)
    recom_permission_locations = models.ManyToManyField(Location, related_name='recom_profiles', blank=True)
    hod_permission_departments = models.ManyToManyField(Department, related_name='hod_profiles', blank=True)
    hod_permission_locations = models.ManyToManyField(Location, related_name='hod_profiles', blank=True)

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        """
        Overrides the default save method to resize the image to a max of 300x300 pixels if needed.
        """
        super().save(*args, **kwargs)  # Save the instance first to access the image path
        
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except IOError:
                # Handle the case where the image file does not exist or is unreadable
                pass
