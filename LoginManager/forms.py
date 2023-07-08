from dataclasses import fields
import email
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from LoginManager.models import Account
from django.contrib.auth import get_user_model

User = get_user_model()

class registrationform(UserCreationForm):
    email = forms.EmailField(max_length=260, help_text="Enter a valid email address.")
    class meta:
        model = get_user_model()
        fields = ('email','username','password1','password2')
        
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.get(email = email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} already exists on the system.")

        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = Account.objects.get(username = username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Username {username} already exists on the system.")












