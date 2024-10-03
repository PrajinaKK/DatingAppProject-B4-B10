from django.urls import path
from . views import *

app_name='userflow'

urlpatterns = [
    
   path('profile/<slug:slug>',ProfileView.as_view(),name="profile"),
   path('edit/<slug:slug>',ProfileEditView.as_view(),name="profile_edit"),
   path('myprofile',ProfileEditView.as_view(),name="profile_edit")


]