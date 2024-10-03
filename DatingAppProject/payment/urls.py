from django.urls import path
from .views import *
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'payment'

urlpatterns = [
    
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/callback/', PaymentCallbackView.as_view(), name='payment_callback'),
    path('group/',views.GroupCreateView.as_view(),name="GroupCreateView"),
    path('group-view/',views.GroupView.as_view(),name="GroupView"),
    path('autocomplete/',views.AutocompleteView.as_view(),name="AutocompleteView"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

