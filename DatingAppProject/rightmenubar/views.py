from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, UpdateView, FormView, TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib import messages



# Create your views here.


# sent request.
class SentRequestView(LoginRequiredMixin, View):
    template_name = 'right_menu/sent_request.html'

    def get(self, request, *args, **kwargs):
        # Get the list of users to whom the logged-in user has sent connection requests
        sent_requests = ConnectionRequest.objects.filter(
            sender=request.user,
            status=ConnectionRequest.SENDER
        ).select_related('receiver')

        # Prepare context data
        context = {
            'sent_requests': sent_requests
        }

        return render(request, self.template_name, context)


# accept request.
class AcceptRequestView(LoginRequiredMixin, View):
    template_name = 'right_menu/accept_request.html'  # Update with your correct template path

    def get(self, request, *args, **kwargs):
        # Filter the connection requests where the logged-in user is the sender and the receiver has accepted
        accepted_requests = ConnectionRequest.objects.filter(
            sender=request.user,
            status=ConnectionRequest.ACCEPTED
        ).select_related('receiver')

        context = {
            'accepted_requests': accepted_requests
        }

        return render(request, self.template_name, context)
    


# reject request.
class RejectRequestView(View):
    template_name = 'right_menu/reject_request.html'  # Correct path to your template

    def get(self, request, *args, **kwargs):
        declined_requests = ConnectionRequest.objects.filter(
            sender=request.user,
            status=ConnectionRequest.DECLINED  # Adjust this to match your model's status for declined requests
        ).select_related('receiver')

        context = {
            'declined_requests': declined_requests
        }

        return render(request, self.template_name, context)


# recived request.
class ReceivedRequestView(View):
    template_name = 'right_menu/recived_request.html'  # Path to your template

    def get(self, request, *args, **kwargs):
        # Filter connection requests where the logged-in user is the receiver
        received_requests = ConnectionRequest.objects.filter(
            receiver=request.user,
            status=ConnectionRequest.SENDER  # Adjust this if needed based on your status field
        ).select_related('sender')  # To optimize database access for sender data

        context = {
            'received_requests': received_requests
        }

        return render(request, self.template_name, context)


# contacted.
class ContactedView(TemplateView):
    template_name = 'right_menu/contacted.html'


# viewed my profile.
class ViewedProfileView(TemplateView):
    template_name = 'right_menu/viewed_profile.html'



# send and cancel the friend request.   
class SendConnectionRequestView(View):
    def post(self, request, user_id):
        receiver = get_object_or_404(User, id=user_id)

        # Check if a connection request already exists
        existing_request = ConnectionRequest.objects.filter(sender=request.user, receiver=receiver).first()

        if existing_request:
            if existing_request.status == ConnectionRequest.ACCEPTED:
                messages.info(request, "You are already friends.")
            else:
                # Cancel the request if it already exists and is not accepted
                existing_request.delete()
                messages.success(request, "Connection request canceled.")
        else:
            # Create a new connection request if no request exists
            ConnectionRequest.objects.create(
                sender=request.user,
                receiver=receiver,
                status=ConnectionRequest.SENDER
            )
            messages.success(request, "Connection request sent.")

        return redirect('rightmenubar:home')


# accept the request in received page.
class AcceptConnectionRequestView(View):
    def get(self, request, request_id):
        connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)
        connection_request.accept()
        messages.success(request, "Connection request accepted.")
        return redirect('rightmenubar:recived_request')


# decline the request in received page.
class DeclineConnectionRequestView(View):
    def get(self, request, request_id):
        connection_request = get_object_or_404(ConnectionRequest, id=request_id, receiver=request.user)
        connection_request.decline()
        messages.success(request, "Connection request declined.")
        return redirect('rightmenubar:recived_request')
    

# shortlisted page.
class ShortListedView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'right_menu/shortlist.html'
    context_object_name = 'shortlisted_users'

    def get_queryset(self):
        # Get all users that the logged-in user has shortlisted
        return self.request.user.shortlisted.all()


# remove the shortlisted user.
class RemoveShortlistedUserView(LoginRequiredMixin, View):
    def post(self, request, pk):
        user_to_remove = get_object_or_404(User, pk=pk)
        request.user.shortlisted_users.remove(user_to_remove)
        return redirect('rightmenubar:shortlist')
    

# # function for shortlist a user.
# class ShortlistUserView(LoginRequiredMixin, View):
#     def post(self, request, pk):
#         user_to_shortlist = get_object_or_404(User, pk=pk)
#         if user_to_shortlist != request.user:  # Ensure users cannot shortlist themselves
#             request.user.shortlisted_users.add(user_to_shortlist)
#         return redirect('dating:home')


# shortlisted by users page.
class ShortListedByView(LoginRequiredMixin, View):
    template_name = 'right_menu/shortlisted_by.html'  # Make sure the template matches your template file name

    def get(self, request, *args, **kwargs):
        # Get all users who have shortlisted the currently logged-in user
        shortlisted_by_users = User.objects.filter(shortlisted_users=request.user)

        context = {
            'shortlisted_by_users': shortlisted_by_users,
        }

        return render(request, self.template_name, context)