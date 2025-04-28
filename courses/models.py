from django.db import models
from django.contrib.auth.models import User

class JobListing(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    description = models.TextField()
    application_link = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class SavedJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"

class Tutorial(models.Model):
    title = models.CharField(max_length=200)
    company = models.CharField(max_length=100)
    description = models.TextField()
    link = models.URLField()
    posted_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class SavedTutorial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tutorial = models.ForeignKey(Tutorial, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tutorial')

    def __str__(self):
        return f"{self.user.username} saved {self.tutorial.title}"