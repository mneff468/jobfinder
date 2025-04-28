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
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('tutorials/', views.tutorial_list, name='tutorial_list'),
    path('post-tutorial/', views.post_tutorial, name='post_tutorial'),
    path('tutorial/<int:tutorial_id>/save/', views.save_tutorial, name='save_tutorial'),
    path('tutorial/<int:tutorial_id>/unsave/', views.unsave_tutorial, name='unsave_tutorial'),
    path('delete-tutorial/<int:tutorial_id>/', views.delete_tutorial, name='delete_tutorial'),
    path('resume-tips/', views.resume_tips, name='resume_tips'),
    path('job-search/', views.job_search, name='job_search'),
    path('interview-tips/', views.interview_tips, name='interview_tips'),
    path('profile/', views.profile, name='profile'),
]