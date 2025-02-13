from django import forms
from event.models import Event, Category, Participant

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'time', 'location', 'category']
