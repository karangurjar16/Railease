from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegistrationForm(UserCreationForm):
  
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']

