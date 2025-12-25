# main/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm

class CustomRegistrationForm(UserCreationForm):
    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Enter a username'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm your password'
        })

        self.fields['password'].help_text = None