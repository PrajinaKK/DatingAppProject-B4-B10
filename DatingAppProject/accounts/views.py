from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.http import HttpResponseRedirect

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import View,FormView,TemplateView

from.forms import *
from .forms import PersonalDetailsForm,JobDetailsForm
from .models import   User
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


from django.forms import BaseModelForm
from django.views.generic import CreateView,FormView,TemplateView,DetailView

from django.contrib.auth.views import LoginView as AuthLoginView
from accounts.forms import EmailOrMobileAuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .forms import *
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView,PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin


# Create your views here.

class HomeView(TemplateView):
    template_name = 'accounts/home.html'
    
class SignupView(FormView):
    model=User
    template_name= 'accounts/signup.html'
    form_class = UserCreationForm
    success_url=reverse_lazy('accounts:details')

    def form_valid(self, form):
    # Validate and clean passwords using the form's validation methods
        password = form.cleaned_data.get('password')
        confirm_password = form.cleaned_data.get('confirm_password')

    # Check if passwords match
        if password and confirm_password and password != confirm_password:
            form.add_error('confirm_password', "Passwords do not match.")
            return self.form_invalid(form)

    # Save the user instance, but don't commit to the database yet
        user = form.save(commit=False)

    # Set the password using set_password to ensure it is hashed
        user.set_password(password)
        user.save()  # Now save the user to the database

    # Specify the custom authentication backend
        backend = 'accounts.backends.EmailOrMobileBackend'
    
    # Log the user in using the custom backend
        login(self.request, user, backend=backend)
    
    # Redirect to the success URL
        return redirect(self.success_url)

class LoginView(AuthLoginView):
    template_name = 'accounts/login.html'
    form_class = EmailOrMobileAuthenticationForm
    success_url = reverse_lazy('accounts:details')

    def form_valid(self, form):
        user = form.get_user()
        backend = 'accounts.backends.EmailOrMobileBackend'
        login(self.request, user, backend=backend)
        return redirect(self.success_url)



class DetailsView(TemplateView):
    template_name = 'accounts/details.html'
       
    
class PersonalDetailsView(FormView):
    form_class = PersonalDetailsForm
    template_name = 'dating/details.html'
    success_url = reverse_lazy('accounts:job_status')

    def get(self, request, *args, **kwargs):
        # Instantiate both forms
        personal_details_form = PersonalDetailsForm(instance=request.user)
        multiple_image_form = Multiple_ImageForm()
        return self.render_to_response({
            'personal_details_form': personal_details_form,
            'multiple_image_form': multiple_image_form,
        })

    def post(self, request, *args, **kwargs):
        personal_details_form = PersonalDetailsForm(request.POST, request.FILES, instance=request.user)
        multiple_image_form = Multiple_ImageForm(request.POST, request.FILES)

    # Check if both forms are valid
        if personal_details_form.is_valid() and multiple_image_form.is_valid():
           personal_details_form.save()  # Save the personal details form

        # Save multiple images
           multiple_images = request.FILES.getlist('multiple_image')
           for image in multiple_images:
              Multiple_Image.objects.create(user=request.user, multiple_image=image)

        # Redirect to success_url after both forms are valid
           return HttpResponseRedirect(self.get_success_url())

    # If forms are invalid, re-render the page with errors
        return self.render_to_response({
          'personal_details_form': personal_details_form,
          'multiple_image_form': multiple_image_form,
    })



    
class JobStatusView(TemplateView):
    template_name = 'dating/job_status.html'
    success_url = reverse_lazy('accounts:job_details')



class JobDetailsView(FormView):
    template_name = 'Dating/job_details.html'
    form_class = JobDetailsForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs.update({
                'instance': self.request.user,
                'data': self.request.POST or None,
            })
        else:
            kwargs.update({
                'data': self.request.POST or None,
            })
        return kwargs

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.save()
        return super().form_valid(form)













