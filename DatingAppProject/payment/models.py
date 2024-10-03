from django.db import models
from accounts.models import *


# Create your models here.


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_payment_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.razorpay_payment_id
      
class Group(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='group/', null=True, blank=True)
    members = models.ManyToManyField("accounts.User", related_name='group_members')
    admin = models.ManyToManyField("accounts.User", related_name='admin_groups')
    created = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    created_date = models.DateTimeField(null=True, blank=True)

