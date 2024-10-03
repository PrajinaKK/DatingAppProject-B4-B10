from django.db import models
from accounts.models import User
# Create your models here.

class UserPreference(models.Model):
    PREFFERED_GENDER_CHOICES=(('F','Female'),('M','Male'),('B','Both'))
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,related_name="user_preferred_gender")
    preferred_gender = models.CharField(choices=PREFFERED_GENDER_CHOICES,max_length=1)

