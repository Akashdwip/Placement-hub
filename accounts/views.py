
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

from django.views.decorators.http import require_POST

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            if user.role == 'recruiter':
                return redirect('recruiter_dashboard')

            return redirect('student_dashboard')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.role == 'recruiter':
                return redirect('recruiter_dashboard')

            return redirect('student_dashboard')
    else:
        form = AuthenticationForm(request)

    # Apply Bootstrap styling to login fields
    for field in form.fields.values():
        field.widget.attrs['class'] = 'form-control'

    return render(request, 'accounts/login.html', {'form': form})



@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('home')

    from applications.models import Application
    from jobs.models import Job
    from students.models import StudentProfile

    application_count = Application.objects.filter(student=request.user).count()
    active_jobs_count = Job.objects.filter(is_active=True).count()
    profile = getattr(request.user, 'student_profile', None)
    profile_complete = False
    if profile:
        profile_complete = bool(profile.full_name and profile.cgpa and profile.resume)

    return render(
        request,
        'accounts/student_dashboard.html',
        {
            'application_count': application_count,
            'active_jobs_count': active_jobs_count,
            'profile_complete': profile_complete,
            'profile': profile,
        }
    )


@login_required
def recruiter_dashboard(request):
    if request.user.role != 'recruiter':
        return redirect('home')

    from applications.models import Application
    from jobs.models import Company, Job

    companies = Company.objects.filter(recruiter=request.user)
    company_count = companies.count()
    job_count = Job.objects.filter(company__in=companies, is_active=True).count()
    application_count = Application.objects.filter(job__company__in=companies).count()
    pending_count = Application.objects.filter(job__company__in=companies, status='pending').count()

    return render(
        request,
        'accounts/recruiter_dashboard.html',
        {
            'company_count': company_count,
            'job_count': job_count,
            'application_count': application_count,
            'pending_count': pending_count,
        }
    )
