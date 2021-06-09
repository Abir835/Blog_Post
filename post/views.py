from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignUpFrom


# Create your views here.

def signup(request):
    if request.method == "POST":
        form = SignUpFrom(request.POST)
        if form.is_valid():
            user = form.save()
            # username = form.cleaned_data.get('username')
            user.refresh_from_db()  # load the profile instance created by signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user, password=raw_password)
            login(request, user)
            return redirect("/")
    else:
        form = SignUpFrom()

    return render(request, 'signup.html', {'form': form})
