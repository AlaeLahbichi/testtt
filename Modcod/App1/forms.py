from django import forms
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'placeholder': 'Votre email',
    }))
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Votre nom d\'utilisateur',
    }))
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Mot de passe',
        'id' : "password",
    }))
    
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirmez le mot de passe',
        'id' : "password",
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')
