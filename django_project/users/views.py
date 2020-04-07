from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from users.models import extendedUser, User
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            #user.refresh_from_db()
            #user.medic_code = form.cleaned_data.get('medic_code')
            #user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in! Your medic code {user.medic_code}')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    user = request.user
    try:
        userr = extendedUser.objects.get(username=user.username)
    except extendedUser.DoesNotExist:
        userr = user
    return render(request, 'users/profile.html', {'user':userr})
