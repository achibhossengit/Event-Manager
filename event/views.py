from django.shortcuts import render, HttpResponse, redirect
from event.forms import EventModelForm, CategoryModelForm, ParticipantModelForm
from event.models import Event, Category, Participant
from datetime import date
from django.db.models import Count, Q
from django.contrib import messages

def homepage(request):
    if request.method=='POST':
        keyword = request.POST.get('keyword')
    else:
        keyword = 'a'
    events = Event.objects.filter(Q(name__icontains=keyword)|Q(description__icontains=keyword)|Q(location__icontains=keyword))
    context = {
        'events': events
    }
    return render(request, 'homepage.html', context)
        

def dashboard(request):
    section_title = "Today's Events"
    events = Event.objects.filter(date=date.today())
    type = request.GET.get('type')
    counts = Event.objects.aggregate(
        total = Count('id'),
        today = Count('id', filter=Q(date=date.today())),
        upcoming = Count('id', filter=Q(date__gt = date.today())),
        past = Count('id', filter=Q(date__lt = date.today()))
    )
    participants = Participant.objects.all()
    total_participants = participants.count()
    if type=='total_events':
        events = Event.objects.all()
        section_title = "Total Events "
    elif type=='today':
        events = Event.objects.filter(date=date.today())
        section_title = "Today's Events "
    elif type=='upcoming':
        events = Event.objects.filter(date__gt=date.today())
        section_title = "Upcoming Events"
    elif type=='past':
        events = Event.objects.filter(date__lt=date.today())
        section_title = "Past Events "

    context = {
        'section_title':section_title,
        'participants':participants,
        'total_participants':total_participants,
        'events':events,
        'counts':counts
    }
    return render(request, 'dashboard.html', context)


def event_details(request, id):
    if request.method=='POST':
        event = Event.objects.get(id=id)
        participants = event.participants.all()
        context = {
            'event':event,
            'participants':participants
        }
        return render( request, 'event_details.html', context)
    
def management(request):
    events = Event.objects.all()
    categories = Category.objects.all()
    participants = Participant.objects.all()
    context ={
        'events':events,
        'categories':categories,
        'participants': participants
    }
    return render(request, 'management.html', context)

def create_event(request):
    if request.method == 'POST':
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event created Successfully!")
            return redirect('management')
    else:
        event_form = EventModelForm()
    context = {
        'event_form': event_form
    }
    return render(request, 'create.html', context)

def delete_event(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_id')
        try:
            event = Event.objects.get(id=event_id)
            event.delete()
            messages.success(request, "Event deleted successfully!")
        except:
            messages.error(request, 'Your ID is invalid! Enter a valid ID please.')
    return redirect('management')

def update_event(request):
    event_id = request.GET.get('event_id')
    try:
        event = Event.objects.get(id=event_id)
        if request.method == 'POST':
                event_form = EventModelForm(request.POST, instance=event)
                if event_form.is_valid():
                    event_form.save()
                    messages.success(request, "Event updated successfully!")
                    return redirect('management')
        else:
            event_form = EventModelForm(instance=event)
            context = {
                'event_form':event_form
            }
            return render(request, 'update.html', context)

    except:
        messages.error(request, "Your ID is invalid! Please enter a valid event ID.")
        return redirect('management')



def create_category(request):
    if request.method == "POST":
        category_form = CategoryModelForm(request.POST)
        category_form.save()
        messages.success(request, "Category Added Successfully!")
        return redirect('management')
    else:
        category_form = CategoryModelForm()
    context = {
        'category_form': category_form
    }
    return render(request, 'create.html', context)

def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        try:
            category = Category.objects.get(id=category_id)
            category.delete()
            messages.success(request, "Category deleted successfully!")
        except:
            messages.error(request, "Your Category ID is invalid! Please Provide a valid ID.")
        return redirect('management')

def update_category(request):
    category_id = request.GET.get('category_id')
    try:
        category = Category.objects.get(id=category_id)
        if request.method == 'POST':
            category_form = CategoryModelForm(request.POST, instance=category)
            if category_form.is_valid():
                category_form.save()
                messages.success(request, "Category Updated successfully!")
                return redirect('management')
        else:
            category_form = CategoryModelForm(instance=category)
            context = {
                'category_form': category_form
            }
            return render(request, 'update.html', context)
    except:
        messages.error(request, "Please Provide a valid ID.")
        return redirect('management')
    
def create_participant(request):
    participant_form = ParticipantModelForm()
    if request.method == 'POST':
        participant_form = ParticipantModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Added successfully!")
            return redirect('management')
    context = {
        'participant_form': participant_form
    }
    return render(request, 'create.html', context)

def delete_participant(request):
    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        try:
            participant = Participant.objects.get(id=participant_id)
            participant.delete()
            messages.success(request, "Participant removed successfully!")
            return redirect('management')
        except:
            messages.error(request, "Invalid ID!")
            return redirect('management')
    
def update_participant(request):
    participant_id = request.GET.get('participant_id')
    try:
        participant = Participant.objects.get(id=participant_id)
        if request.method == 'POST':
            participant_form = ParticipantModelForm(request.POST, instance=participant)
            if participant_form.is_valid():
                participant_form.save()
                messages.success(request, "Updated successfully!")
                return redirect('management')
        else:
            participant_form = ParticipantModelForm(instance=participant)
            context={
                'participant_form': participant_form
            }
            return render(request, 'update.html', context)
    except:
        messages.error(request, "Invalid ID!")
        return redirect('management')



def participant_list(request):
    participants = Participant.objects.all()
    context = {
        'participants': participants
    }
    return render(request, 'participant_list.html', context)