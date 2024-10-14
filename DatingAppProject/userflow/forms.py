from django import forms
from accounts.models import User
from userhome.models import UserPreference

from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password

class UserEditForm(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type' : 'text'}))
    
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','type' : 'email'}))
    phone_number=forms.IntegerField(validators=[RegexValidator(r'^\+?1?\d{9,15}$', 'Enter a valid phone number (up to 10 digits)')],widget=forms.NumberInput(attrs={'class':'form-control','type' : ''}))
   
    bio=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','type' : 'text'}))
    short_reel = forms.FileField(widget= forms.FileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username','email','phone_number','bio','profile_pic','short_reel']




class PreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['prefered_age_min', 'prefered_age_max', 'preferred_gender', 'education','location', 'interests_hobbies', 'relationship', 'height_min', 'height_max', 'weight_min', 'weight_max', 'lifestyle', 'religion', 'occupation']
    def __init__(self, *args, **kwargs):
        super(PreferenceForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True 


