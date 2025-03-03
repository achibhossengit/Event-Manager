from django.shortcuts import render
from users.forms import UserModelForm

def sign_up(request):
    form = UserModelForm()
    return render(request, 'sign_up.html', {'form':form})