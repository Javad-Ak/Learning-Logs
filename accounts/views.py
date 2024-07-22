from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

from accounts.forms import ProfileForm


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = UserCreationForm()
    else:
        # Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('logs:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def new_profile(request):
    """Create a new profile."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ProfileForm(request.POST, request.FILES)
    else:
        # POST data submitted; process data.
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)
            new_profile.user = request.user
            new_profile.save()
            return redirect('logs:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/new_profile.html', context)
