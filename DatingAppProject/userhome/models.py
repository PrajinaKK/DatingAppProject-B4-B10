from django.db import models
from accounts.models import User
# Create your models here.

class UserPreference(models.Model):
    PREFFERED_GENDER_CHOICES=(('F','Female'),('M','Male'),('B','Both'))
    user=models.OneToOneField(User,on_delete=models.SET_NULL,null=True,related_name="user_preferred_gender")
    preferred_gender = models.CharField(choices=PREFFERED_GENDER_CHOICES,max_length=1)

    prefered_age_min = models.CharField(max_length=50,blank=True)
    prefered_age_max = models.CharField(max_length=50,blank=True)
    location = models.ManyToManyField("accounts.Location")
    interests_hobbies = models.ManyToManyField("accounts.Interest")
    relationship = models.CharField(max_length=50,blank=True)
    education = models.CharField(max_length=50,blank=True)
    height_min = models.CharField(max_length=50,blank=True)
    height_max = models.CharField(max_length=50,blank=True)
    weight_min = models.CharField(max_length=50,blank=True)
    weight_max = models.CharField(max_length=50,blank=True)
    lifestyle = models.CharField(max_length=50,blank=True)
    religion = models.CharField(max_length=50,blank=True)
    occupation = models.CharField(max_length=50,blank=True)

