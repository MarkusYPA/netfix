"""netfix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^
, views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^
, Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from . import views as v
from services import views as services_views

# The urlpatterns list routes URLs to views.
urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),
    # Include URLs from the 'main' app
    path('', include('main.urls')),
    # Include URLs from the 'services' app
    path('services/', include('services.urls')),
    # Include URLs from the 'users' app (for registration)
    path('register/', include('users.urls')),
    # URL for customer profiles
    path('customer/<slug:name>', v.customer_profile, name='customer_profile'),
    # URL for company profiles
    path('company/<slug:name>', v.company_profile, name='company_profile'),
    # URL for displaying most requested services
    path('most_requested/', services_views.most_requested_services, name='most_requested_services'),
]

# Serve static files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
