from django.urls import path
from . views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'userhome'

urlpatterns = [
    path('home/', HomeView.as_view(),name="home1"),
    path('entry',EntryView.as_view(),name="entry"),
    path('story/<slug:slug>/',StoryView.as_view(),name="story")
]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)