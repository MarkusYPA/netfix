from django.shortcuts import render
from datetime import date

from users.models import User, Company, Customer
from services.models import Service, ServiceRequest



# Renders the profile page for a customer.
def customer_profile(request, name):
    # Retrieve the User and Customer objects based on the username.
    user = User.objects.get(username=name)
    customer = Customer.objects.get(user=user)

    # Calculate the customer's age.
    today = date.today()
    age = today.year - customer.date_of_birth.year - ((today.month, today.day) < (customer.date_of_birth.month, customer.date_of_birth.day))

    # Retrieve all service requests made by this customer, ordered by date.
    requested_services = ServiceRequest.objects.filter(customer=customer).order_by("-request_date")

    # Render the profile page with customer details and their requested services.
    return render(request, 'users/profile.html', {'user': user, 'customer': customer, 'requested_services': requested_services, 'user_age': age})


# Renders the profile page for a company.
def company_profile(request, name):
    # Retrieve the User and Company objects based on the username.
    user = User.objects.get(username=name)
    company = Company.objects.get(user=user)

    # Retrieve all services offered by this company, ordered by date.
    services = Service.objects.filter(
        company=company).order_by("-date")

    # Render the profile page with company details and their offered services.
    return render(request, 'users/profile.html', {'user': user, 'company': company, 'services': services})

