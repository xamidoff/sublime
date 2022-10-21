from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms

from .models import *



class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Foydalanuvchi ismi'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parol'
    }))


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parol'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parolni tasdiqlash'
    }))

    class Meta:
        model = User
        fields = ('username',)
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Foydalanuvchi ismi'
            })
        }

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['text', ]

        widgets = {
            'text': forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': '...'
            })
        }


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'name', 'email'
        ]

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            })
        }

class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippinAddress
        fields = [
            'address', 'city', 'state', 'zipcode'
        ]

        widgets = {
            'address': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }