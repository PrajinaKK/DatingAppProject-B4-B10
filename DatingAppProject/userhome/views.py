from django.shortcuts import render,redirect
from django.views.generic import TemplateView,ListView,DetailView
from django.urls import reverse_lazy
from . models import UserPreference
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

# Create your views here.
class SpinView(TemplateView):
    template_name = 'spin.html'

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
        context['profiles'] = User.objects.filter(location=user.location.id,is_superuser=False)
        context['designation_profiles'] = User.objects.filter(designation=user.designation,is_superuser=False)[1:3]
        context['qualification_profiles'] = User.objects.filter(qualification=user.qualification,is_superuser=False)[1:3]
        
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
       
class yourMatchesView(TemplateView):
    template_name='yourMatches.html'    

class MatchesView(ListView):
    model = User
    # template_name = 'right_menu/myprofile.html'
    template_name='yourMatches.html'
    context_object_name = 'matched_users'
    
    def get_queryset(self):
        current_user = self.request.user
        queryset = User.objects.filter(
            ~Q(id=current_user.id),  # Exclude the current user
            ~Q(is_superuser=True),# Excludin the super user
            gender=current_user.gender,  # Optional: to match based on gender
            app=current_user.app  # Optional: only show users in the same app (Dating or Matrimony)
        )

        # Filter based on the matching fields
        queryset = queryset.filter(
            Q(location=current_user.location) | 
            Q(interest=current_user.interest) |
            Q(hobbies=current_user.hobbies) |
            Q(drinking_habits=current_user.drinking_habits) |
            Q(smoking_habits=current_user.smoking_habits)
        )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_user = self.request.user
        print('current user: ',current_user)
        matches = []
        match_count=0

        for user in context['matched_users']:
            # Calculate match percentage
            match_score = 0
            total_criteria = 5  # We're comparing 5 fields

            if user.location == current_user.location:
                match_score += 1
            if user.interest == current_user.interest:
                match_score += 1
            if user.hobbies == current_user.hobbies:
                match_score += 1
            if user.drinking_habits == current_user.drinking_habits:
                match_score += 1
            if user.smoking_habits == current_user.smoking_habits:
                match_score += 1

            match_percentage = (match_score / total_criteria) * 100
            
            matches.append({
                'user': user,
                'match_percentage': match_percentage
            })
        match_count = len(matches)
        context['matches'] = matches
        context['match_count'] = match_count 
        return context    
