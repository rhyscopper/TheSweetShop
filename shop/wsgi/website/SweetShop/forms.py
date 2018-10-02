from django import forms
from django.contrib.auth.models import User

#sets the user form for registration


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(max_length=30)
    address = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'email', 'password','phone','address']
