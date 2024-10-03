from django.shortcuts import render
from django.views.generic import TemplateView,DetailView
from accounts.models import User

# Create your views here.
class ProfileView(DetailView):
    model=User
    template_name='profile.html'
    login_url = '/login/'
    context_object_name="profile"
    slug_field = 'slug'
    slug_url_kwarg= 'slug'


class ProfileEditView(TemplateView):
    template_name='editProfile.html'
