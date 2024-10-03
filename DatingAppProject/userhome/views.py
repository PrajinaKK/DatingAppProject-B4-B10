from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView
from django.urls import reverse_lazy
from . models import UserPreference
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class StoryView(LoginRequiredMixin,DetailView):
    model=User
    template_name = "story.html"
    login_url = '/login/'
    context_object_name="story"
    slug_field = 'slug'
    slug_url_kwarg= 'slug'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user = self.request.user
    #     print('current user: ',user)
    #     context['story'] = User.objects.get(username=user)
    #     return context
    

class HomeView(LoginRequiredMixin,ListView):
    model=User
    template_name = "home.html"
    login_url = '/login/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['all_user'] = User.objects.filter(is_superuser=False)
        context['profiles'] = User.objects.filter(location=user.location.id)[1:3]
        context['designation_profiles'] = User.objects.filter(designation=user.designation)[1:3]
        context['qualification_profiles'] = User.objects.filter(qualification=user.qualification)[1:3]
        
        return context

        
    
class EntryView(TemplateView):
    # template_name="shared/sidebars.html"
    template_name = "entry.html"
    success_url = reverse_lazy('userhome:home1')
    def post(self, request, *args, **kwargs):
        print(request.POST)
        # Get or create the UserPreference instance for the logged-in user
        user_pref, created = UserPreference.objects.get_or_create(user=request.user)
        
        # Check which button was clicked and update preferred gender
        if 'women' in request.POST:
            user_pref.preferred_gender = 'F'
        elif 'men' in request.POST:
            user_pref.preferred_gender = 'M'
        elif 'both' in request.POST:
            user_pref.preferred_gender = 'B'
        
        # Save the updated preference
        user_pref.save()
        
        # Redirect to a success or the same page to prevent resubmission
        return redirect(self.success_url) 
       