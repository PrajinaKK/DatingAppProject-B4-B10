from django.urls import path
from . views import *

app_name='userflow'

urlpatterns = [
    
   path('profile/<slug:slug>',ProfileView.as_view(),name="profile"),
   path('edit/',editMyProfileView.as_view(),name="myprofile_edit"),
   path('myprofile',myProfileView.as_view(),name="myprofile"),
   path('change-password/',changePasswordView.as_view(),name="change_password"),
   path('settings/',SettingsView.as_view(),name="SettingsView"),
   path('privacy-settings/',PrivacySettingsView.as_view(),name="PrivacySettingsView"),
   path('filter/',FilterProfilesView.as_view(),name="FilterView"),
   path('preference/',PreferenceView.as_view(),name="PreferenceView"),


]