from django.shortcuts import render, redirect
from django. contrib import messages
from django.urls import reverse

from .forms import UserRegisterForm
from django.http import HttpResponse, HttpResponseRedirect

def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Účet úspešne založen pro {username}! Můžeš se přihlásit.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

