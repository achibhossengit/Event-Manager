from django.shortcuts import render, redirect
from users.forms import UserModelForm

def sign_up(request):
    form = UserModelForm()
    if request.method == 'POST':
        form = UserModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
    return render(request, 'sign_up.html', {'form':form})