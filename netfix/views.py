from django.shortcuts import render
from datetime import date

from users.models import User, Company, Customer
from services.models import Service, ServiceRequest


def home(request):
    return render(request, 'users/home.html', {'user': request.user})


def customer_profile(request, name):
    user = User.objects.get(username=name)
    customer = Customer.objects.get(user=user)
    today = date.today()
    age = today.year - customer.date_of_birth.year - ((today.month, today.day) < (customer.date_of_birth.month, customer.date_of_birth.day))
    requested_services = ServiceRequest.objects.filter(customer=customer).order_by("-request_date")
    return render(request, 'users/profile.html', {'user': user, 'customer': customer, 'requested_services': requested_services, 'user_age': age})


def company_profile(request, name):
    user = User.objects.get(username=name)
    company = Company.objects.get(user=user)
    services = Service.objects.filter(
        company=company).order_by("-date")

    return render(request, 'users/profile.html', {'user': user, 'company': company, 'services': services})
