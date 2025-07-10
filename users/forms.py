from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


class DateInput(forms.DateInput):
    input_type = 'date'


def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    date_of_birth = forms.DateField(widget=DateInput)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            customer = Customer.objects.create(
                user=user, date_of_birth=self.cleaned_data.get('date_of_birth'))
            customer.save()
        return user


class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, validators=[validate_email])
    field = forms.ChoiceField(choices=Company._meta.get_field('field').choices)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_company = True
        user.email = self.cleaned_data.get('email')
        if commit:
            user.save()
            company = Company.objects.create(
                user=user, field=self.cleaned_data.get('field'))
            company.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
