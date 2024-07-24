from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import login

from .forms import ProfileForm, UserForm
from .models import Profile


def register(request):
    """Register a new user."""
    if request.method != 'POST':
        # Display blank registration form.
        form = UserForm()
    else:
        # Process completed form.
        form = UserForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            login(request, new_user)
            return redirect('logs:index')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html', context)


@login_required
def delete(request):
    if request.method != 'POST':
        raise Http404

    request.user.delete()
    return redirect('logs:index')


@login_required
def edit_profile(request):
    """edit a user's profile."""
    try:
        obj = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        obj = Profile(user=request.user)
        obj.save()

    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = ProfileForm(instance=obj)
    else:
        # POST data submitted; process data.
        form = ProfileForm(data=request.POST, files=request.FILES)
        print(request.FILES)
        if form.is_valid():
            new_profile = form.save(commit=False)

            new_profile.user = request.user
            new_profile.save()
            return redirect('accounts:profile', id=request.user.id)

    # Display a blank or invalid form.
    return render(request, 'registration/edit_profile.html', {'form': form})


def profile(request, id):
    """Show user's profile."""
    user = User.objects.get(id=id)
    try:
        obj = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        obj = Profile(user=user)
        obj.save()

    return render(request, 'registration/profile.html', {'profile': obj})
