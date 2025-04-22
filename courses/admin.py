from django.contrib import admin
from .models import JobListing, SavedJob

# Register your models here.
admin.site.register(JobListing)
admin.site.register(SavedJob)