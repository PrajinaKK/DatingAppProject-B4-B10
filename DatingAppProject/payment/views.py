from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views import View
from .models import Payment
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.utils.decorators import method_decorator

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
