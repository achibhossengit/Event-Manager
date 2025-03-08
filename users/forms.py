from django.contrib.auth.models import User, Group
from django.forms import ModelForm
from event.forms import StyledFormMixin
from django import forms
from django.contrib.auth.forms import AuthenticationForm

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