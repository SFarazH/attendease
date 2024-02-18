from django import forms
from django.forms import TextInput, PasswordInput

sem = (
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
)


class LoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'GEMS ID (demo@rknec.edu)'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',  'placeholder': 'GEMS password'}))
    

class semForm(forms.Form):
    semester = forms.ChoiceField(choices=sem, widget=forms.Select(attrs={'class': 'form-control'}))