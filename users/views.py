from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.forms import PasswordChangeForm
from users.forms import UserModelForm, LogInForm, UserRoleModelForm, GroupModelForm, EditProfileForm, ChangePasswordForm, CustomPasswordResetForm, CustomPasswordConfirmForm
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.tokens import default_token_generator
from users.models import CustomUser
from django.views import View
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView

User = CustomUser

# views
def no_permission(request):
    return render(request, 'no-permission.html')

# group related views
@login_required(login_url='log-in')
@permission_required(perm='group.add_group', login_url='no-permission')
def create_group(request):
    group_form = GroupModelForm()
    if request.method == 'POST':
        group_form = GroupModelForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            messages.success(request, "Group Created Successfully!")
            return redirect('dashboard')
    return render(request, 'create.html', {'group_form':group_form})

@login_required(login_url='sign-url')
@permission_required(perm='group.change_group', login_url='no-permission')
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

@login_required(login_url='group.sign-url')
@permission_required(perm='delete_group', login_url='no-permission')
def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    group.delete()
    messages.success(request, "Group Deleted Successfully!")
    return redirect('dashboard')

@login_required(login_url='log-in')
@permission_required(perm='user.delete_user', login_url='no-permission')
def delete_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    messages.success(request, "User removed successfully!")
    return redirect('dashboard')

@login_required(login_url='log-in')
@permission_required(perm='user.change_user', login_url='no-permission')
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

@login_required(login_url='log-in')
@permission_required(perm='user.view-user', login_url='no-permission')
def user_details(request, user_id):
    user = User.objects.get(id=user_id)
    context = {
        'user': user 
    }
    return render(request, 'user_details.html', context)

# authentications
def sign_up(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # just create an object not save in database
            user.set_password(form.cleaned_data.get('password')) # for proper hasing and set password. its so important
            user.is_active = False
            form.save() # save in database
            return redirect('log-in')
    return render(request, 'sign_up.html', {'form':form})

def active_user(request, user_id, token):
    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect('log-in')
        else:
            return HttpResponse("Invalid token or user id!")
    except:
        return HttpResponse("Something Went Wrong! Try again later.")
    


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

@login_required(login_url='log-in')
def log_out(request):
    logout(request)
    return redirect('log-in')



class ProfileView(LoginRequiredMixin, View):
    login_url = 'log-in'
    def get(self, request):
        user = request.user
        context = {
            'username': user.username,
            'name':f"{user.first_name} {user.last_name}",
            'role':user.groups.first().name,
            'email':user.email,
            'phone':user.phone_number,
            'member_since':user.date_joined,
            'last_login':user.last_login,
            'profile_img':user.profile_img.url if user.profile_img else None,
            'type': 'view_profile'
        }
        return render(request, 'accounts/profile.html', context)
    
class EditProfile(LoginRequiredMixin, UpdateView):
    login_url = 'log-in'
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('user-profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] ='edit_profile'
        return context

    def get_object(self, queryset = None):
        obj = self.request.user
        return obj
    
    def form_valid(self, form):
        messages.success(self.request, "Your profile has been updated successfully!")
        return super().form_valid(form)
    
    
class ChangePassword(LoginRequiredMixin, View):
    login_url = 'log-in'
    def get(self, request):
        form = ChangePasswordForm()
        context = {
            'type': 'change_password',
            'form': form
        }
        return render(request, 'accounts/profile.html', context)
    
    def post(self, request, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')
            
            if not request.user.check_password(old_password):
                messages.error(request, "Your old password is incorrect.")
                return redirect('change-password')

            if new_password != confirm_password:
                messages.error(request, "New password and confirm password do not match.")
                return redirect('change-password')
            
            if old_password == new_password:
                messages.error(request, "New password cannot be the same as the old password.")
                return redirect('change-password')
                

            request.user.set_password(new_password)
            request.user.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, "Your password has been updated successfully!")
            return redirect('user-profile')
        else:
            messages.error(request, "Your Form is invalid!")
            return redirect('change-password')
        

class CustomPasswordReset(PasswordResetView):
    model = User
    template_name = 'registration/form.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('log-in')
    html_email_template_name = 'registration/email_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['protocol'] = 'https' if self.request.is_secure() else 'http'
        context['domain'] = self.request.get_host()
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'A password reset link has been sent to your email address. Please check your inbox to reset your password.')
        return super().form_valid(form)
    

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomPasswordConfirmForm
    template_name = 'registration/form.html'
    success_url = reverse_lazy('log-in')
    
    def form_valid(self, form):
        messages.success(self.request, 'Your password was changed successfully! Now try to log in with new password.')
        return super().form_valid(form)