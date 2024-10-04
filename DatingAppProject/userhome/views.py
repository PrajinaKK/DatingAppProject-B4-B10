from django.views.generic import TemplateView


class BaseView(TemplateView):
    template_name = 'base.html'


class SpinView(TemplateView):
    template_name = 'spin.html'



