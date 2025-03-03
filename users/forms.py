from django.contrib.auth.models import User
from django.forms import ModelForm
from event.forms import StyledFormMixin

class UserModelForm(StyledFormMixin, ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        # widgets={
        #     'events': forms.CheckboxSelectMultiple,
        # }
        