from django.shortcuts import render, redirect
from users.forms import UserModelForm, LogInForm, UserRoleModelForm, GroupModelForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required

# views
def no_permission(request):
    return render(request, 'no-permission.html')

# group related views
def create_group(request):
    group_form = GroupModelForm()
    if request.method == 'POST':
        group_form = GroupModelForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            messages.success(request, "Group Created Successfully!")
            return redirect('dashboard')
    return render(request, 'create.html', {'group_form':group_form})

def update_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group_form = GroupModelForm(instance=group)
    if request.method=="POST":
        group_form = GroupModelForm(request.POST, instance=group)
        if group_form.is_valid():
            group_form.save()
            messages.success(request, "Group Updated successfully!")
            return redirect('dashboard')
    return render(request, 'update.html', {'group_form': group_form})

def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    messages.success(request, "Group Deleted Successfully!")
    return redirect('dashboard')

@login_required(login_url='sign-in')
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "User removed successfully!")
    return redirect('dashboard')

@login_required(login_url='sign-in')
def update_user(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user_form = UserRoleModelForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Updated successfully!")
            return redirect('dashboard')
    else:
        user_form = UserRoleModelForm(instance=user)
        context={
            'user_form': user_form,
        }
        return render(request, 'update.html', context)
    
def change_role(request, user_id):
    user = User.objects.get(id=user_id)
    roles = Group.objects.all()
    return render(request,'update_role.html', {'roles':roles})

@login_required(login_url='sign-in')
def user_list(request):
    participants = User.objects.all()
    context = {
        'participants': participants
    }
    return render(request, 'user_list.html', context)

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
