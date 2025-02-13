from django.shortcuts import render, HttpResponse, redirect
from event.forms import EventModelForm

def create_event(request):
    if request.method == 'POST':
        form = EventModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_creations')
    else:
        form = EventModelForm()

    return render(request, 'create_event.html', {'form': form})