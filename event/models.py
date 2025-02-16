from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=300)
    description = models.CharField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.SET_DEFAULT, default=1, related_name= 'events')

    def __str__(self):
        return self.name

class Participant(models.Model):
    name  = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    events = models.ManyToManyField('Event', related_name= 'participants')
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField()

    def __str__(self):
        return self.name