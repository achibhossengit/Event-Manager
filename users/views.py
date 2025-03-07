from django.shortcuts import render, redirect
from users.forms import UserModelForm, LogInForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required

# views
def no_permission(request):
    return render(request, 'no-permission.html')

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

@login_required(login_url='sign-in')
@permission_required(perm='event.delete_participants', login_url='no-permission')
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

@login_required(login_url='sign-in')
@permission_required(perm='event.update_participants', login_url='no-permission')
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

@login_required(login_url='sign-in')
@permission_required(perm='event.delete_participants', login_url='no-permission')
def participant_list(request):
    participants = User.objects.all()
    context = {
        'participants': participants
    }
    return render(request, 'participant_list.html', context)

# authentications
def sign_up(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # just create an object not save in database
            user.set_password(form.cleaned_data.get('password')) # for proper hasing and set password. its so important
            form.save() # save in database
            return redirect('homepage')
    return render(request, 'sign_up.html', {'form':form})


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

@login_required(login_url='sign-in')
def log_out(request):
    logout(request)
    return redirect('homepage')
