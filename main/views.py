from django.shortcuts import render
from django.contrib.auth import logout as django_logout
from services.models import Service
from django.db.models import Count


# Renders the home page.
def home(request):
    # Get the top 3 most requested services, including ties.
    # First, get the count of requests for each service.
    services_with_counts = Service.objects.annotate(num_requests=Count('servicerequest'))

    # Order by the number of requests in descending order.
    sorted_services = services_with_counts.order_by('-num_requests')

    # Get the top 3 services based on request count.
    top_3_services = []
    if sorted_services.exists():
        # Get the request count of the 3rd service (or last if less than 3 services exist)
        if sorted_services.count() >= 3:
            third_service_count = sorted_services[2].num_requests
        else:
            third_service_count = sorted_services.last().num_requests

        # Include all services that have a request count greater than or equal to the 3rd service's count
        for service in sorted_services:
            if service.num_requests >= third_service_count:
                top_3_services.append(service)
            elif len(top_3_services) >= 3: # Stop if we already have 3 and the current service has fewer requests
                break

    return render(request, "main/home.html", {'top_services': top_3_services})


# Logs out the current user and renders the logout page.
def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
