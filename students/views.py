from django.shortcuts import render, redirect

# Create your views here.

from django.contrib.auth.decorators import login_required

from .models import StudentProfile
from .forms import StudentProfileForm


from django.contrib import messages


@login_required
def student_profile(request):
    if request.user.role != 'student':
        return redirect('home')

    profile, created = StudentProfile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':
        form = StudentProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('student_profile')
    else:
        form = StudentProfileForm(instance=profile)

    return render(
        request,
        'students/student_profile.html',
        {'form': form, 'profile': profile}
    )
