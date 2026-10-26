from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from applications.models import Application
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Company, Job
from .forms import CompanyForm, JobForm


@login_required
def create_company(request):
    # Only recruiters can create companies
    if request.user.role != 'recruiter':
        return redirect('home')

    if request.method == 'POST':
        form = CompanyForm(request.POST)

        if form.is_valid():
            # Save the company without committing yet
            company = form.save(commit=False)

            # Associate it with the logged-in recruiter
            company.recruiter = request.user

            # Save the company to the database
            company.save()

            return redirect('company_list')
    else:
        form = CompanyForm()

    return render(
        request,
        'jobs/create_company.html',
        {'form': form}
    )


@login_required
def company_list(request):
    # Only recruiters can view their company list
    if request.user.role != 'recruiter':
        return redirect('home')

    companies = Company.objects.filter(
        recruiter=request.user
    )

    return render(
        request,
        'jobs/company_list.html',
        {'companies': companies}
    )

@login_required
def create_job(request):
    if request.user.role != 'recruiter':
        return redirect('home')

    form = JobForm()

    # Show only companies owned by this recruiter.
    form.fields['company'].queryset = Company.objects.filter(
        recruiter=request.user
    )

    if request.method == 'POST':
        form = JobForm(request.POST)

        # Restrict company choices on submitted data too.
        form.fields['company'].queryset = Company.objects.filter(
            recruiter=request.user
        )

        if form.is_valid():
            form.save()
            return redirect('job_list')

    return render(
        request,
        'jobs/create_job.html',
        {'form': form}
    )

@login_required
def job_list(request):
    if request.user.role != 'recruiter':
        return redirect('home')

    jobs = Job.objects.filter(
        company__recruiter=request.user
    ).select_related('company').order_by('-created_at')

    return render(
        request,
        'jobs/job_list.html',
        {'jobs': jobs}
    )


from django.db.models import Q


@login_required
def browse_jobs(request):
    if request.user.role != 'student':
        return redirect('home')

    jobs = Job.objects.filter(is_active=True).select_related('company')

    q = request.GET.get('q', '').strip()
    if q:
        jobs = jobs.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(required_skills__icontains=q) |
            Q(company__name__icontains=q)
        )

    location = request.GET.get('location', '').strip()
    if location:
        jobs = jobs.filter(location__icontains=location)

    cgpa = request.GET.get('cgpa', '').strip()
    if cgpa:
        try:
            cgpa_val = float(cgpa)
            jobs = jobs.filter(minimum_cgpa__lte=cgpa_val)
        except ValueError:
            pass

    jobs = jobs.order_by('-created_at')

    applied_job_ids = set(
        Application.objects.filter(student=request.user).values_list('job_id', flat=True)
    )

    profile = getattr(request.user, 'student_profile', None)

    return render(
        request,
        'jobs/browse_jobs.html',
        {
            'jobs': jobs,
            'applied_job_ids': applied_job_ids,
            'profile': profile,
        }
    )

@login_required
@require_POST
def apply_for_job(request, job_id):
    if request.user.role != 'student':
        return redirect('home')

    job = get_object_or_404(Job, id=job_id, is_active=True)

    # Check minimum CGPA eligibility if student profile exists
    profile = getattr(request.user, 'student_profile', None)
    if profile and profile.cgpa is not None and job.minimum_cgpa:
        if profile.cgpa < job.minimum_cgpa:
            messages.error(
                request,
                f"Your CGPA ({profile.cgpa}) is lower than the minimum requirement ({job.minimum_cgpa}) for {job.title}."
            )
            return redirect('browse_jobs')

    application, created = Application.objects.get_or_create(
        student=request.user,
        job=job
    )

    if created:
        messages.success(request, f'You have successfully applied for {job.title}!')
    else:
        messages.warning(request, f'You have already applied for {job.title}.')

    return redirect('browse_jobs')


@login_required
def my_applications(request):
    if request.user.role != 'student':
        return redirect('home')

    applications = Application.objects.filter(
        student=request.user
    ).select_related(
        'job',
        'job__company'
    ).order_by('-applied_at')

    return render(
        request,
        'jobs/my_applications.html',
        {'applications': applications}
    )

@login_required
def recruiter_applications(request):
    if request.user.role != 'recruiter':
        return redirect('home')

    applications = Application.objects.filter(
        job__company__recruiter=request.user
    ).select_related(
        'student',
        'student__student_profile',
        'job',
        'job__company'
    )

    recruiter_jobs = Job.objects.filter(company__recruiter=request.user).order_by('title')
    job_id = request.GET.get('job', '').strip()
    if job_id.isdigit():
        applications = applications.filter(job_id=int(job_id))

    status_filter = request.GET.get('status', '').strip()
    if status_filter in ['pending', 'shortlisted', 'rejected', 'selected']:
        applications = applications.filter(status=status_filter)

    q = request.GET.get('q', '').strip()
    if q:
        applications = applications.filter(
            Q(student__username__icontains=q) |
            Q(student__email__icontains=q) |
            Q(student__student_profile__full_name__icontains=q) |
            Q(student__student_profile__department__icontains=q) |
            Q(student__student_profile__skills__icontains=q)
        )

    # Calculate status counts for filtering badges
    base_apps = Application.objects.filter(job__company__recruiter=request.user)
    if job_id.isdigit():
        base_apps = base_apps.filter(job_id=int(job_id))
    total_count = base_apps.count()
    pending_count = base_apps.filter(status='pending').count()
    shortlisted_count = base_apps.filter(status='shortlisted').count()
    selected_count = base_apps.filter(status='selected').count()
    rejected_count = base_apps.filter(status='rejected').count()

    applications = applications.order_by('-applied_at')

    return render(
        request,
        'jobs/recruiter_applications.html',
        {
            'applications': applications,
            'recruiter_jobs': recruiter_jobs,
            'selected_job': job_id,
            'status_filter': status_filter,
            'search_query': q,
            'total_count': total_count,
            'pending_count': pending_count,
            'shortlisted_count': shortlisted_count,
            'selected_count': selected_count,
            'rejected_count': rejected_count,
        }
    )

@login_required
@require_POST
def update_application_status(request, application_id):
    if request.user.role != 'recruiter':
        return redirect('home')

    application = get_object_or_404(
        Application,
        id=application_id,
        job__company__recruiter=request.user
    )

    new_status = request.POST.get('status')
    allowed_statuses = ['pending', 'shortlisted', 'rejected', 'selected']

    if new_status in allowed_statuses:
        application.status = new_status
        application.save(update_fields=['status'])
        messages.success(request, f'Status for {application.student.username} updated to {new_status.title()}.')
    else:
        messages.error(request, 'Invalid application status.')

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('recruiter_applications')


@login_required
@require_POST
def toggle_job_status(request, job_id):
    if request.user.role != 'recruiter':
        return redirect('home')

    job = get_object_or_404(Job, id=job_id, company__recruiter=request.user)
    job.is_active = not job.is_active
    job.save(update_fields=['is_active'])
    status_label = "active" if job.is_active else "inactive"
    messages.success(request, f'"{job.title}" is now marked as {status_label}.')
    return redirect('job_list')
