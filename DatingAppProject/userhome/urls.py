from django.urls import path
from . views import *

app_name = 'userhome'

urlpatterns = [
    path('home/', HomeView.as_view(),name="home1"),
    path('entry',EntryView.as_view(),name="entry")
   

]