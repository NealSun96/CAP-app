from django.shortcuts import render


def home(request):
    return render(request, "index.html", {})


def courses(request, key=""):
    return render(request, "courses.html", {"key": key})


def dashboard(request, key="", id=""):
    return render(request, "dashboard.html", {"key": key, "id": id})
