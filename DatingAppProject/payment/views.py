from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views import View
from .models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator
from .models import *
from accounts.models import User
from .forms import *
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.template.loader import render_to_string
from django.http import JsonResponse

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class PaymentView(View):
    def get(self, request):
        amount = 4900  # Amount in paise (₹500.00)
        razorpay_order = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })
        payment = Payment.objects.create(
            user=request.user,
            razorpay_payment_id=razorpay_order['id'],
            amount=amount / 100,
            status='successfull'
        )

        context = {
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'razorpay_order_id': razorpay_order['id'],
            'amount': amount,
            'currency': 'INR',
            'callback_url': '/payment/callback/',
        }
        return render(request, 'payment.html', context)



@method_decorator(csrf_exempt, name='dispatch')  # Exempt CSRF for the entire class
class PaymentCallbackView(View):
    def post(self, request, *args, **kwargs):
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        razorpay_signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        }

        try:
            # Verify the payment signature
            razorpay_client.utility.verify_payment_signature(params_dict)
            # Fetch the corresponding payment entry
            payment = Payment.objects.get(razorpay_payment_id=razorpay_order_id)
            payment.status = 'successful'
            payment.save()
            return JsonResponse({'status': 'Payment successful'})
        except razorpay.errors.SignatureVerificationError:
            return HttpResponseBadRequest('Invalid payment signature')
        except Payment.DoesNotExist:
            return HttpResponseBadRequest('Payment record not found')

        return HttpResponseBadRequest('Invalid request')


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

