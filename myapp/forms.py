from django import forms
from django.contrib.auth.models import User
from .models import Habit,HabitCategory,profile

class SignupForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model=User
        fields=['username','password']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class AddHabitForm(forms.ModelForm):

    class Meta:
        model=Habit
        fields=['title','category']


class categoryForm(forms.ModelForm):

    class Meta:
        model=HabitCategory
        fields=['name']
    

class profileForm(forms.ModelForm):
    class Meta:
        model=profile
        fields=['gender','ph_no','picture']

    def clean_ph_no(self):
        phone = self.cleaned_data.get('ph_no')
    
        if phone and len(phone) != 10: 
            raise forms.ValidationError("Enter valid phone number")
    
        return phone