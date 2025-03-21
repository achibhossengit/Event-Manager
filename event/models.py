from django.db import models
from users.models import CustomUser

class Event(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default=1, related_name= 'events')
    media = models.ImageField(upload_to='event_media', blank=True, null=True)
    participants = models.ManyToManyField(CustomUser, related_name='rsvp_events')

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField()

    def __str__(self):
        return self.name