from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, authenticate
from django.db import transaction
from django.core.exceptions import ValidationError

from .models import User, Company, Customer


# A custom date input widget to ensure the browser renders a date picker.
class DateInput(forms.DateInput):
    input_type = 'date'


# A validator to ensure that a user cannot register with an email that already exists in the database.
def validate_email(value):
    # In case the email already exists in an email input in a registration form, this function is fired
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            value + " is already taken.")


# A form for creating a new customer account.
class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    date_of_birth = forms.DateField(
        widget=DateInput(attrs={'placeholder': 'Date of Birth'})
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['password2'].help_text = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].help_text = ''

    # The save method is wrapped in a transaction to ensure that both the user and the customer are created successfully.
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


# A form for creating a new company account.
class CompanySignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        validators=[validate_email],
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    field = forms.ChoiceField(
        choices=Company._meta.get_field('field').choices,
        widget=forms.Select(attrs={'placeholder': 'Field'})
    )

    class Meta(UserCreationForm.Meta):
        model = User

    def __init__(self, *args, **kwargs):
        super(CompanySignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        self.fields['password2'].help_text = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].help_text = ''

    # The save method is wrapped in a transaction to ensure that both the user and the company are created successfully.
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


# A form for logging in a user.
class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password'}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autocomplete'] = 'off'
