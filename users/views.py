from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import CreateView
from django.contrib import messages # Import messages

from .forms import CustomerSignUpForm, CompanySignUpForm, UserLoginForm
from .models import User


# Renders the main registration page where the user can choose to sign up as a customer or a company.
def register(request):
    return render(request, 'users/register.html')


# A class-based view for handling the customer sign-up process.
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/register_customer.html'

    # Adds the user_type to the context so the template can render the correct form.
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    # This method is called when the form is valid. It saves the user and logs them in.
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful!') # Add success message
        return redirect('/')


# A class-based view for handling the company sign-up process.
class CompanySignUpView(CreateView):
    model = User
    form_class = CompanySignUpForm
    template_name = 'users/register_company.html'

    # Adds the user_type to the context so the template can render the correct form.
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'company'
        return super().get_context_data(**kwargs)

    # This method is called when the form is valid. It saves the user and logs them in.
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Registration successful!') # Add success message
        return redirect('/')


# A function-based view for handling the user login process.
def LoginUserView(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                # We need to get the username from the email address to authenticate the user.
                user_obj = User.objects.get(email=email)
                user = authenticate(request, username=user_obj.username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Login successful!') # Add success message
                    return redirect('/')
                else:
                    form.add_error(None, 'Invalid email or password')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid email or password')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})
