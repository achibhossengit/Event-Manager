from django.shortcuts import render, HttpResponse, redirect
from event.forms import EventModelForm
from event.models import Event, Category, Participant
from datetime import date

def test_view(request):
    return render(request, 'dashboard.html')

def dashboard(request):
    # type = request.GET.get('type')
    # print(type)
    events = Event.objects.all()
    total_participants = Participant.objects.all().count()
    total_events = events.count()
    upcoming_events = Event.objects.filter(date__gte=date.today()).count()
    today_events = Event.objects.filter(date=date.today()).count()
    past_events = Event.objects.filter(date__lt = date.today()).count()
    context = {
        'events':events,
        'total_participants':total_participants,
        'total_events':total_events,
        'upcoming_events':upcoming_events,
        'today_events':today_events,
        'past_events':past_events
    }
    return render(request, 'dashboard.html', context)
