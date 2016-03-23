import string
import random

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm

from mailer.utils.helpers import get_object_or_None


class RegisterForm(ModelForm):

    email = forms.EmailField(required=True, widget=forms.TextInput())
    password = forms.CharField(widget=(forms.PasswordInput()))
    confirm_password = forms.CharField(widget=(forms.PasswordInput()))

    class Meta:
        model = User
        fields = ['confirm_password', ]

    def clean_email(self):

        email = self.cleaned_data['email']

        check_email = get_object_or_None(User, email=email)

        if check_email:
            raise forms.ValidationError(
                "A user associated with this email address already exists")

        return email

    def clean_password(self):

        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if not password == confirm_password:
            raise forms.ValidationError("Password mismatch")

        elif len(password) < 6:
            raise forms.ValidationError("Password is too short (6 symbols)")

        return password

    def save(self):

        data = self.cleaned_data
        username = ''.join(random.choice(string.ascii_lowercase + string.digits)for x in range(16))
        new_user = User.objects.create_user(
            username=username,
            email=data['email'], 
            password=data['password'],
            )

        return new_user


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.TextInput())
    password = forms.CharField(
        required=True, widget=forms.PasswordInput(render_value=False))

    def clean(self):

        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user and user.is_active:
                return self.cleaned_data

        raise forms.ValidationError("Invalid login details")