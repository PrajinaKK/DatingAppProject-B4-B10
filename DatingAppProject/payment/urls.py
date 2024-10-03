from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'payment'
urlpatterns = [
    
    path('payment/', PaymentView.as_view(), name='payment'),
    path('payment/callback/', PaymentCallbackView.as_view(), name='payment_callback'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)