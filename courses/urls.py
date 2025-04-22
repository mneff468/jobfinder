from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='custom_login'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('jobs/', views.job_list, name='job_list'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('job/<int:job_id>/save/', views.save_job, name='save_job'),
    path('job/<int:job_id>/unsave/', views.unsave_job, name='unsave_job'),
    path('post-job/', views.post_job, name='post_job'),
    path('resume-tips/', views.resume_tips, name='resume_tips'),
    path('job-search/', views.job_search, name='job_search'),
    path('interview-tips/', views.interview_tips, name='interview_tips'),
    path('profile/', views.profile, name='profile'),
]