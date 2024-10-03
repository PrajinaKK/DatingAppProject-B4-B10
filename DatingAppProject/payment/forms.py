from django import forms
from .models import *
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'description', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }