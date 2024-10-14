from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic import TemplateView,DetailView,UpdateView
from accounts.models import User
from accounts.forms import UserForm, Multiple_ImageForm
from userflow.forms import UserEditForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import PreferenceForm
from accounts.models import Interest, Location
from django.http import HttpResponseRedirect
from django.urls import reverse

from profile import Profile
from django.shortcuts import render
from django.views.generic import TemplateView



# Create your views here.
class ProfileView(DetailView):
    model=User
    template_name='profile.html'
    login_url = '/login/'
    context_object_name="profile"
    slug_field = 'slug'
    slug_url_kwarg= 'slug'


class myProfileView(TemplateView):
    model=User
    login_url = '/login/'
    # context_object_name="profile"
    template_name='myProfile.html'

    def get(self,request, *args, **kwargs):
       
        user = get_object_or_404(User, pk=self.request.user.pk)
        return self.render_to_response({'profile':user})    

class editMyProfileView(TemplateView):
    model = User
    form_class = UserEditForm
    # fields = ["username","email","phone_number","bio","profile_pic","short_reel"]
    template_name='editMyProfile.html'  
    success_url = reverse_lazy('userflow:myprofile')
    def get_object(self, queryset=None):
        # This sets self.object whenever get_object is called
        self.object = get_object_or_404(User, pk=self.request.user.pk)
        
        return self.object
    def get(self,request, *args, **kwargs):
        profile_info_form = UserEditForm(instance=request.user)
        multiple_image_form = Multiple_ImageForm()
        user = get_object_or_404(User, pk=self.request.user.pk)
        return self.render_to_response({'form':profile_info_form,'image_form':multiple_image_form,'user':user})
    
    def post(self, request, *args, **kwargs):
        print("posted")
        user = self.get_object()
        print('user: ',user)

       
        profile_info_form = UserEditForm(request.POST, request.FILES, instance=user)
        multiple_image_form = Multiple_ImageForm(request.POST, request.FILES)

        if profile_info_form.is_valid() or multiple_image_form.is_valid():
            print("valid")
            
            
            user.username = self.request.POST.get('username')
            user.email = self.request.POST.get('email')
            user.phone_number = self.request.POST.get('phone_number')
            # user.short_reel = self.request.POST.get('short_reel')
            user.bio = self.request.POST.get('bio')
            user.save()
            
            images = multiple_image_form.save(commit=False)  
            
            images.user = user 
            images.save()
            return self.success_url
          

        else:
            print(profile_info_form.errors)
            print(multiple_image_form.errors)
            # If forms are invalid, render the page with errors
            return self.render_to_response({
                'form': profile_info_form,
                'image_form': multiple_image_form,
                'user': user
            })
    def form_invalid(self, form):
        print("invalid")
        return super().form_invalid(form)    

class changePasswordView(TemplateView):
    template_name='changePassword.html'    


class SettingsView(TemplateView):
    template_name = "Settings.html"


class PrivacySettingsView(TemplateView):
    template_name="Privacy.html"



class FilterView(TemplateView):
    template_name = "filter.html"


class PreferenceView(CreateView):
    template_name = "Preference.html"
    form_class = PreferenceForm
    success_url = reverse_lazy('userflow:FilterView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["interest"] = Interest.objects.all()
        context["location"] = Location.objects.all()
        return context
    def form_valid(self, form):
        user_preference = form.save(commit=False)
        user_preference.user = self.request.user 
        user_preference.save()
        
        form.cleaned_data['location'] = self.request.POST.getlist('location')
        form.cleaned_data['interests_hobbies'] = self.request.POST.getlist('interests_hobbies')

        user_preference.location.set(form.cleaned_data['location'])
        user_preference.interests_hobbies.set(form.cleaned_data['interests_hobbies'])

        return super().form_valid(form)
    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)    
    




class FilterProfilesView(TemplateView):
    template_name = 'filter.html'  # This is the template for rendering the form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add initial data to the context if needed, like available filter options
        return context

    def post(self, request, *args, **kwargs):
        sort_by = request.POST.get('sort_by')
        gender = request.POST.get('gender')
        location = request.POST.get('location')
        interests = request.POST.get('interests')
        languages = request.POST.get('languages')
        relationship_goals = request.POST.get('relationship_goals')

        # Get all profiles initially
        profiles = User.objects.all()

        # Apply sort by condition
        if sort_by == 'newest':
            profiles = profiles.order_by('-created_at')
        elif sort_by == 'last_active':
            profiles = profiles.order_by('-last_active')
        elif sort_by == 'distance':
            profiles = profiles.order_by('distance_from_user')  # Custom distance logic
        elif sort_by == 'popularity':
            profiles = profiles.order_by('-popularity')
        elif sort_by == 'age':
            profiles = profiles.order_by('age')

        # Apply filters
        if gender:
            profiles = profiles.filter(gender=gender)
        if location:
            profiles = profiles.filter(location__icontains=location)
        if interests:
            profiles = profiles.filter(interests__icontains=interests)
        if languages:
            profiles = profiles.filter(languages_spoken__icontains=languages)
        if relationship_goals:
            profiles = profiles.filter(relationship_goals=relationship_goals)

        # Render the filtered result
        context = self.get_context_data()
        context['profiles'] = profiles
        return self.render_to_response(context)

# Reset Filter View (Optional)

class ResetFilterView(TemplateView):
    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('filter_profiles'))    
