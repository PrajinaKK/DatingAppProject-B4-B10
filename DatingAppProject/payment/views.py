from django.shortcuts import render
from .models import *
from accounts.models import User
from .forms import *
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import JsonResponse
# Create your views here.
class GroupCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('accounts:login')
    template_name = 'group.html'
    form_class = GroupForm
    success_url = reverse_lazy('payment:GroupView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        if user_id:
            context['users'] = User.objects.exclude(id=user_id)  
            context['admin'] = User.objects.get(id=user_id) 
        return context

    def form_valid(self, form):
        group = form.save(commit=False)
        group.created = self.request.user
        group.created_date = timezone.now()
        group.save()
        group.admin.add(self.request.user) 
        return super().form_valid(form)


class GroupView(LoginRequiredMixin,View):
    login_url = reverse_lazy('accounts:login')
    def get(self, request):
        groups = Group.objects.filter(members=request.user)
        return render(request, "group_view.html", {'groups': groups})

    def post(self, request):
        search_group = request.POST.get('searchbox', '')
        query = Group.objects.filter(members=request.user)
        if search_group:
            query = query.filter(name__icontains=search_group)
        html = render_to_string('filter_sorting.html', {'groups': query})
        return JsonResponse({'html': html})
    

class AutocompleteView(View):
    def get(self, request):
        term = request.GET.get('term', '')
        groups = Group.objects.filter(members=request.user, name__icontains=term)
        names = list(groups.values_list('name', flat=True))
        return JsonResponse(names, safe=False)
