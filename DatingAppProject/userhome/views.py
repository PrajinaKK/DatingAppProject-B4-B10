from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomeView(TemplateView):
    # template_name="shared/sidebars.html"
    template_name = "home.html"

class EntryView(TemplateView):
    # template_name="shared/sidebars.html"
    template_name = "entry.html"
