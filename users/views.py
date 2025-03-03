from django.shortcuts import render, redirect
from users.forms import UserModelForm, LogInForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

def sign_up(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    return render(request, 'sign_up.html', {'form':form})

def create_participant(request):
    participant_form = UserModelForm()
    if request.method == 'POST':
        participant_form = UserModelForm(request.POST)
        if participant_form.is_valid():
            participant_form.save()
            messages.success(request, "Added successfully!")
            return redirect('management-participants')
    context = {
        'participant_form': participant_form
    }
    return render(request, 'create.html', context)

def delete_participant(request):
    if request.method == 'POST':
        participant_id = request.POST.get('participant_id')
        try:
            participant = User.objects.get(id=participant_id)
            participant.delete()
            messages.success(request, "User removed successfully!")
            return redirect('management-participants')
        except:
            messages.error(request, "Invalid ID!")
            return redirect('management-participants')
    
def update_participant(request):
    participant_id = request.GET.get('participant_id')
    try:
        participant = User.objects.get(id=participant_id)
        if request.method == 'POST':
            participant_form = UserModelForm(request.POST, instance=participant)
            if participant_form.is_valid():
                participant_form.save()
                messages.success(request, "Updated successfully!")
                return redirect('management-participants')
        else:
            participant_form = UserModelForm(instance=participant)
            context={
                'participant_form': participant_form
            }
            return render(request, 'update.html', context)
    except:
        messages.error(request, "Invalid ID!")
        return redirect('management-participants')

def participant_list(request):
    participants = User.objects.all()
    context = {
        'participants': participants
    }
    return render(request, 'participant_list.html', context)

# authentications
def log_in(request):
    form = LogInForm()
    if request.method == 'POST':
        form = LogInForm(data = request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            user = User.objects.get(username=username)
            login(request, user)
            return redirect('homepage')

    return render(request, 'log_in.html', {'form':form})

@login_required
def log_out(request):
    logout(request)
    return redirect('homepage')
