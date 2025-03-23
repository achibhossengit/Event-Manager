from django.contrib.auth.models import Group
from django.forms import ModelForm
from event.forms import StyledFormMixin
from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from users.models import CustomUser
User = CustomUser

class UserModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        
class UserRoleModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ['groups']
        widgets ={
            'groups':forms.CheckboxSelectMultiple
        }
        labels = {
            'groups': 'User Role'
        }
        help_texts = {
            'groups': ''
        }

class EditProfileForm(StyledFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'profile_img')

class LogInForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class GroupModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets ={
            'permissions': forms.CheckboxSelectMultiple
        }

class ChangePasswordForm(StyledFormMixin, forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput(), label='Old Password')
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New Password')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

class CustomPasswordResetForm(StyledFormMixin, PasswordResetForm):
    pass

class CustomPasswordConfirmForm(StyledFormMixin, SetPasswordForm):
    pass
