from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django. contrib import messages
from django.urls import reverse
from .models import Profile

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.http import HttpResponse, HttpResponseRedirect

def register(request):
    if request.method =='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            profile = Profile(user = user)
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Účet úspešne založen pro {username}! Můžeš se přihlásit.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required()
def profile(request):
    u_form = UserUpdateForm(request.POST, instance=request.user)
    p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if request.method == 'POST':
        pass
        # u_form = UserUpdateForm(request.POST, instance=request.user)
        # p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

    if u_form.is_valid() and p_form.is_valid():
        u_form.save()
        p_form.save()
        messages.success(request, f'Údaje úspešně změneny')
        return redirect('profile')

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

