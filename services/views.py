from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from users.models import Company, Customer, User

from .models import Service, ServiceRequest # Import ServiceRequest
from .forms import CreateNewService, RequestServiceForm
from django.db.models import Count


def service_list(request):
    services = Service.objects.all().order_by("-date")
    return render(request, 'services/list.html', {'services': services})


def index(request, id):
    service = Service.objects.get(id=id)
    return render(request, 'services/single_service.html', {'service': service})


def create(request):
    return render(request, 'services/create.html', {})


@login_required
def create(request):
    if not request.user.is_company:
        return redirect('/')

    company = Company.objects.get(user=request.user)
    service_choices = Service._meta.get_field('field').choices

    if company.field != 'All in One':
        service_choices = [(choice, label) for choice, label in service_choices if choice == company.field]

    if request.method == 'POST':
        form = CreateNewService(request.POST, choices=service_choices)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price_hour = form.cleaned_data['price_hour']
            field = form.cleaned_data['field']

            Service.objects.create(
                company=company,
                name=name,
                description=description,
                price_hour=price_hour,
                field=field
            )
            return redirect('/services')
    else:
        form = CreateNewService(choices=service_choices)
    return render(request, 'services/create.html', {'form': form})


def service_field(request, field):
    # search for the service present in the url
    field = field.replace('-', ' ').title()
    services = Service.objects.filter(
        field=field)
    return render(request, 'services/field.html', {'services': services, 'field': field})


def request_service(request, id):
    return render(request, 'services/request_service.html', {})


@login_required
def request_service(request, id):
    if not request.user.is_customer:
        return redirect('/')

    service = Service.objects.get(id=id)
    customer = Customer.objects.get(user=request.user)

    if request.method == 'POST':
        form = RequestServiceForm(request.POST)
        if form.is_valid():
            address = form.cleaned_data['address']
            service_time = form.cleaned_data['service_time']

            ServiceRequest.objects.create(
                customer=customer,
                service=service,
                address=address,
                service_time=service_time
            )
            return redirect('/services')
    else:
        form = RequestServiceForm()
    return render(request, 'services/request_service.html', {'form': form, 'service': service})


def most_requested_services(request):
    services = Service.objects.annotate(
        num_requests=Count('servicerequest')
    ).order_by('-num_requests')[:10] # Top 10 most requested services
    return render(request, 'services/most_requested.html', {'services': services})
