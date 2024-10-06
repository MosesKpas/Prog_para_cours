from django import forms
from .models import Livre
from django import forms
from django.contrib.auth.models import User


class LivreForm(forms.ModelForm):
    class Meta:
        model = Livre
        fields = ['titre', 'auteur', 'prix']
class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password']
    password = forms.CharField(widget=forms.PasswordInput)
