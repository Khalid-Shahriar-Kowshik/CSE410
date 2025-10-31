from .forms import UserProfileForm
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib.auth.models import User

def userprofile(request):
    return render(request, 'userprofile/profile.html')

def edit_profile(request):
    profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'userprofile/edit_profile.html', {'form': form})


def public_profile(request, username):
    """Render a public view of a user's profile by username."""
    user = User.objects.filter(username=username).first()
    if not user:
        return render(request, '404.html', status=404)
    profile = getattr(user, 'userprofile', None)
    return render(request, 'userprofile/profile.html', {'user_profile_user': user, 'profile': profile})
