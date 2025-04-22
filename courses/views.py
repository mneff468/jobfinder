from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import JobListing, SavedJob

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'courses/login.html', {'error': 'Invalid username or password'})
    return render(request, 'courses/login.html')

def custom_logout(request):
    logout(request)
    return redirect('custom_login')

@login_required
def home(request):
    return render(request, 'courses/home.html')

@login_required
def job_list(request):
    jobs = JobListing.objects.all().order_by('-posted_at')
    # Get saved job IDs for the current user
    saved_jobs = SavedJob.objects.filter(user=request.user).values_list('job_id', flat=True)
    context = {
        'jobs': jobs,
        'saved_jobs': saved_jobs,
    }
    return render(request, 'courses/job_list.html', context)

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    is_saved = SavedJob.objects.filter(user=request.user, job=job).exists()
    context = {
        'job': job,
        'is_saved': is_saved,
    }
    return render(request, 'courses/job_detail.html', context)

@login_required
def save_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    SavedJob.objects.get_or_create(user=request.user, job=job)
    messages.success(request, "Job saved successfully!")
    return redirect('job_detail', job_id=job.id)

@login_required
def unsave_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    SavedJob.objects.filter(user=request.user, job=job).delete()
    messages.success(request, "Job removed from saved list!")
    return redirect('job_detail', job_id=job.id)

@login_required
def post_job(request):
    if not request.user.is_staff:
        messages.error(request, "Only admins can post jobs.")
        return redirect('job_list')
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        description = request.POST.get('description')
        application_link = request.POST.get('application_link')
        if title and company and location and description and application_link:
            JobListing.objects.create(
                title=title,
                company=company,
                location=location,
                description=description,
                application_link=application_link,
                posted_by=request.user
            )
            messages.success(request, "Job posted successfully!")
            return redirect('job_list')
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'courses/post_job.html')

@login_required
def resume_tips(request):
    return render(request, 'courses/resume_tips.html')

@login_required
def job_search(request):
    return render(request, 'courses/job_search.html')

@login_required
def interview_tips(request):
    return render(request, 'courses/interview_tips.html')

@login_required
def profile(request):
    saved_jobs = SavedJob.objects.filter(user=request.user).order_by('-saved_at')
    context = {
        'saved_jobs': saved_jobs,
    }
    return render(request, 'courses/profile.html', context)