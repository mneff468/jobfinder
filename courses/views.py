import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import JobListing, SavedJob, Tutorial, SavedTutorial

def custom_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        print(f"Form type: {form_type}")

        if form_type == 'login':
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(f"Login attempt - Username: {username}")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return render(request, 'courses/login.html', {'error': 'Invalid username or password'})

        elif form_type == 'register':
            print("Registration form submitted")
            username = request.POST.get('reg_username')
            email = request.POST.get('reg_email')
            password = request.POST.get('reg_password')
            password_confirm = request.POST.get('reg_password_confirm')
            print(f"Registration attempt - Username: {username}, Email: {email}")

            if password != password_confirm:
                print("Validation failed: Passwords do not match")
                messages.error(request, "Passwords do not match.")
                return redirect('custom_login')

            if len(password) < 8:
                print("Validation failed: Password too short")
                messages.error(request, "Password must be at least 8 characters long.")
                return redirect('custom_login')

            if not re.search(r'\d', password):
                print("Validation failed: No number in password")
                messages.error(request, "Password must contain at least one number.")
                return redirect('custom_login')

            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                print("Validation failed: No special character in password")
                messages.error(request, "Password must contain at least one special character.")
                return redirect('custom_login')

            if User.objects.filter(username=username).exists():
                print("Validation failed: Username exists")
                messages.error(request, "Username already exists.")
                return redirect('custom_login')

            if User.objects.filter(email=email).exists():
                print("Validation failed: Email exists")
                messages.error(request, "Email already exists.")
                return redirect('custom_login')

            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                print(f"User created: {username}")
            except Exception as e:
                print(f"Error creating user: {e}")
                messages.error(request, "An error occurred while creating your account. Please try again.")
                return redirect('custom_login')

            login(request, user)
            messages.success(request, "Registration successful! Welcome to JobFinder.")
            return redirect('home')

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
def delete_job(request, job_id):
    job = get_object_or_404(JobListing, id=job_id)
    if request.user != job.posted_by:
        messages.error(request, "You can only delete jobs you created.")
        return redirect('job_list')
    if request.method == 'POST':
        job.delete()
        messages.success(request, "Job deleted successfully!")
        return redirect('job_list')
    return render(request, 'courses/confirm_delete_job.html', {'job': job})

@login_required
def tutorial_list(request):
    tutorials = Tutorial.objects.all().order_by('-posted_at')
    saved_tutorials = SavedTutorial.objects.filter(user=request.user).values_list('tutorial_id', flat=True)
    context = {
        'tutorials': tutorials,
        'saved_tutorials': saved_tutorials,
    }
    return render(request, 'courses/tutorial_list.html', context)

@login_required
def post_tutorial(request):
    if not request.user.is_staff:
        messages.error(request, "Only admins can post tutorials.")
        return redirect('tutorial_list')
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        description = request.POST.get('description')
        link = request.POST.get('link')
        if title and company and description and link:
            Tutorial.objects.create(
                title=title,
                company=company,
                description=description,
                link=link,
                posted_by=request.user
            )
            messages.success(request, "Tutorial posted successfully!")
            return redirect('tutorial_list')
        else:
            messages.error(request, "All fields are required.")
    return render(request, 'courses/post_tutorial.html')

@login_required
def save_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    SavedTutorial.objects.get_or_create(user=request.user, tutorial=tutorial)
    messages.success(request, "Tutorial saved successfully!")
    return redirect('tutorial_list')

@login_required
def unsave_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    SavedTutorial.objects.filter(user=request.user, tutorial=tutorial).delete()
    messages.success(request, "Tutorial removed from saved list!")
    return redirect('tutorial_list')

@login_required
def delete_tutorial(request, tutorial_id):
    tutorial = get_object_or_404(Tutorial, id=tutorial_id)
    if request.user != tutorial.posted_by:
        messages.error(request, "You can only delete tutorials you created.")
        return redirect('tutorial_list')
    if request.method == 'POST':
        tutorial.delete()
        messages.success(request, "Tutorial deleted successfully!")
        return redirect('tutorial_list')
    return render(request, 'courses/confirm_delete_tutorial.html', {'tutorial': tutorial})

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
    saved_tutorials = SavedTutorial.objects.filter(user=request.user).order_by('-saved_at')
    context = {
        'saved_jobs': saved_jobs,
        'saved_tutorials': saved_tutorials,
    }
    return render(request, 'courses/profile.html', context)