from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator,MaxValueValidator



class Location(models.Model):
    id=models.AutoField(primary_key=True)
    CITY_CHOICES = (('KNR','Kannur'),('KH','Kochi'))
    city = models.CharField(max_length=3,choices=CITY_CHOICES)
    def __str__(self):
        return self.city

class Interest(models.Model):
    id=models.AutoField(primary_key=True)
    INTEREST_CHOICES = (('NR','Nature'),('TL','Travel'),('WR','Writing'),('AT','ART'),('PL','People'),('GF','Gym&Fitness'),('MC','Music'))
    interest = models.CharField(max_length=2,choices=INTEREST_CHOICES)
    def __str__(self):
        return self.interest    
    
class Hobbies(models.Model):
    id=models.AutoField(primary_key=True)
    HOBBY_CHOICES = (('CK','Cooking'),('TLG','Traveling'),('RD','Reading'),('DC','Dancing'),('GM','Gaming'))
    hobby = models.CharField(max_length=3,choices=HOBBY_CHOICES)
    def __str__(self):
        return self.hobby
       
class Habbit(models.Model):
    id=models.AutoField(primary_key=True)
    HABBIT_CHOICES = (('R','Regularly'),('O','Occasionally'),('Q','Quitting'),('N','Never'))
    habit=models.CharField(choices=HABBIT_CHOICES,max_length=1) 
    def __str__(self):
        return self.habit   


class Qualification(models.Model):
    id=models.AutoField(primary_key=True)
    QUALIFICATION_CHOICES = (('G','Graduation'),('PG','Post Graduation'),('D','Diploma'))    
    qualification=models.CharField(choices=QUALIFICATION_CHOICES,max_length=3)

    def __str__(self):
        return self.qualification



class User(AbstractUser):
    RELATIONSHIP_CHOICES=(('ST','Short Term Relationship'),('LT','Long Term Relationship'))
    APP_CHOICES =(('D','Dating'),('M','Matrimony'))
    GENDER_CHOICES=(('F','Female'),('M','Male'),('O','Others'))
    EXPERTISELEVEL_CHOICES=(('B','Beginner'),('I','Intermediate'),('E','Expert'))
    JOB_CHOICES = (('ER','Employer'),('EE','Employee'),('JS','Jobseeker'))
    DRINKING_CHOICES = [
        ('', 'Drinking Habit'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    SMOKING_CHOICES = [
        ('', 'Smoking Habit'),
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    age=models.SmallIntegerField(null=True,
                                validators=[MinValueValidator(18),MaxValueValidator(34)])
    dob=models.DateField(null=True)
    phone_number=models.CharField(max_length=10,blank=True)
    dob=models.DateField(null=True)

    gender=models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True)	
    location=models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,related_name="user_location")

    
    
    smoking_habits = models.CharField(max_length=15, choices=DRINKING_CHOICES, blank=True,null=True)
    drinking_habits = models.CharField(max_length=3, choices=SMOKING_CHOICES, blank=True,null=True)
    interest = models.ForeignKey(Interest,on_delete=models.SET_NULL,null=True,related_name="user_interest")
    hobbies = models.ForeignKey(Hobbies,on_delete=models.SET_NULL,null=True,related_name="user_hobbies")
    qualification=models.ForeignKey(Qualification,on_delete=models.SET_NULL,null=True,related_name="user_qualification")
    
    
    job_status = models.CharField(choices=JOB_CHOICES,max_length=2,null=True)
    company_name=models.CharField(null=True,max_length=100)
    designation=models.CharField(null=True,max_length=100)
    work_location=models.ForeignKey(Location,on_delete=models.SET_NULL,null=True,related_name="user_work_location")
    
    jobtitle=models.CharField(null=True,max_length=100)
    expertise_level=models.CharField(choices=EXPERTISELEVEL_CHOICES,max_length=1,null=True)

    profile_pic=models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    short_reel=models.FileField(upload_to='short_reel/',null=True,blank=True)


    relationship_goals=models.CharField(choices=RELATIONSHIP_CHOICES,max_length=2,blank=True,null=True)
    app = models.CharField(choices=APP_CHOICES,max_length=1,blank=True,null=True)

    shortlisted_users = models.ManyToManyField('self', symmetrical=False, related_name='shortlisted_by_users', blank=True)

    
    
    @property
    def is_employer(self):
        return self.company_name is None and self.designation is None
    
    @property
    def is_jobseeker(self):
        return self.jobtitle is None and self.expertise_level is None
    
    @property
    def shortlisted(self):
        return self.shortlisted_users.all()


class Multiple_Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='images', null=True)
    multiple_image = models.ImageField(upload_to='multiple_pic/', null=True, blank=True)

    def __str__(self):
        return self.multiple_image.name if self.multiple_image else "No Image"
