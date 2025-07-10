from django.shortcuts import render
from django.contrib.auth import logout as django_logout


# Renders the home page.
def home(request):
    return render(request, "main/home.html", {})


# Logs out the current user and renders the logout page.
def logout(request):
    django_logout(request)
    return render(request, "main/logout.html")
