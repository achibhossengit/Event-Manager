from django.shortcuts import render, HttpResponse, redirect
from event.forms import EventModelForm

def test_view(request):
    return render(request, 'dashboard.html')
