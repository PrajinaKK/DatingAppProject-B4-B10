from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'

urlpatterns=[
    #
    # path('', views.HomeView.as_view(), name='home'),
    # path('signup/', views.SignupView.as_view(), name='signup'),
    # path('login/', views.LoginView.as_view(), name='login'),
    # path('details', views.DetailsView.as_view(), name='details'),
    # path('personaldetails/', views.PersonalDetailsView.as_view(), name='personaldetails'),
    # path('job_status', views.JobStatusView.as_view(), name='job_status'),
    # path('job_details', views.JobDetailsView.as_view(), name='job_details'),
    # path('info/',UserJobRelationshipView.as_view(),name="userjobrelationinfo"),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


