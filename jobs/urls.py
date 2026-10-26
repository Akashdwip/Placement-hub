
from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.company_list, name='company_list'),
    path('companies/create/', views.create_company, name='create_company'),   
    path('jobs/create/', views.create_job, name='create_job'),
    path('jobs/my-jobs/', views.job_list, name='job_list'),
    path('browse/', views.browse_jobs, name='browse_jobs'),
    path('jobs/<int:job_id>/apply/', views.apply_for_job, name='apply_for_job'),
    path('my-applications/', views.my_applications, name='my_applications'),   
    path('applications/', views.recruiter_applications, name='recruiter_applications'),  
    path('applications/<int:application_id>/update/', views.update_application_status, name='update_application_status'),
    path('jobs/<int:job_id>/toggle/', views.toggle_job_status, name='toggle_job_status'),
]
